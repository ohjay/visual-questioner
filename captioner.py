"""
Much of this code has been borrowed or adapted from
https://github.com/tensorflow/models/blob/master/research/im2txt/im2txt/run_inference.py.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import yaml
import tensorflow as tf
from im2txt import configuration
from im2txt import inference_wrapper
from im2txt.inference_utils import vocabulary
from preprocess_utils import preprocess_input
from im2txt.inference_utils import caption_generator

class Captioner:
    def __init__(self, sess, checkpoint_path, vocab_file_path):
        self.sess = sess
        config = yaml.load(open('config.yaml', 'r'), Loader=yaml.FullLoader)
        self.preprocess_options = config['preprocess']

        # Build the inference graph.
        g = tf.get_default_graph()
        with g.as_default():
            model = inference_wrapper.InferenceWrapper()
            restore_fn = model.build_graph_from_config(
                configuration.ModelConfig(), checkpoint_path)
        
        # Create the vocabulary.
        self.vocab = vocabulary.Vocabulary(vocab_file_path)

        restore_fn(sess)
        self.generator = caption_generator.CaptionGenerator(model, self.vocab)

    def caption(self, image_path):
        with tf.gfile.GFile(image_path, 'rb') as f:
            image = f.read()
        captions = self.generator.beam_search(self.sess, image)
        if len(captions) == 0:
            return ''
        sentence = captions[0].sentence[1:-1]
        sentence = ' '.join([self.vocab.id_to_word(w) for w in sentence])
        return preprocess_input(sentence, self.preprocess_options)

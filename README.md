# Project 1: Generative Text

Owen Jow, owen@eng.ucsd.edu

## Abstract

For the most part, ML systems exhibit an infantile understanding of the world. They are typically trained to operate only
within a specific domain, and are not equipped to provide deep analyses on most topics. So why are we asking them questions
(see, e.g., the field of visual question answering)? You would think they should be asking _us_ questions. And this is the
idea I hope to promote. Just as you wouldn't expect a young child to know all the answers, just as teachers around the world
encourage their students to ask productive questions, I propose that we take a similar attitude toward our young machines
and train them to _ask questions_ rather than _provide answers_. I plan to use visual imagery as stimuli to prompt these questions.

In one sentence, my goal is to induce the computer to ask meaningful questions about user-provided images.

In order to realize this goal, I use a captioning system to generate a textual description of the image, and then use a GPT-2
model to produce a question corresponding to that description. The GPT-2 model is fine-tuned to predict questions corresponding
to answers; I reverse the order of questions and answers in the training data so that questions follow their associated answers.

## Model/Data

- You can download the trained model from [Google Drive](https://drive.google.com/file/d/1LnOzIRPLEZcJGp0GNMQZSIEPwC8A8Qe-/view?usp=sharing).<br>
It was created using the default config file and the following commands:
```
python3 gen_nq_data.py nq/v1.0-simplified_simplified-nq-train.jsonl -o nq_data_50k.txt -l 50000
python3 train_gpt2_questioner.py -d nq_data_50k.txt -s 300
```
- The original source of my training data is Google's [Natural Questions dataset](https://ai.google.com/research/NaturalQuestions).
It is processed and written to a `.txt` file by `gen_nq_data.py` (see the [Data Generation section](#data-generation)).

## Code

There are a lot of files, but you will only need to interact with a few of them.
Those front-facing files are described below. Note that I have only tested the code with Python 3.6/3.7.
Also, you may want to take a look at the [usage writeup](USAGE.md).

### Setup
As setup, you will need to initialize the submodules, install dependencies, and download external
models and data. The following command, tested on an Ubuntu 18.04 machine and the ECE 188 Jupyterhub
environment, encapsulates all of these actions (as well as data generation – see the subsequent section).
It will install the dependencies in a Python 3 virtual environment called `visual-questioner-env`.
```
./setup.sh
```

### Data Generation
Here, "data generation" means reading the [Natural Questions](https://ai.google.com/research/NaturalQuestions)
JSON Lines data, preprocessing it, and outputting it as a `.txt` file that can be used to fine-tune the GPT-2 model.
`./setup.sh` will automatically do this for you. However, you may wish to regenerate the data with different
configuration settings. In that case, you can edit `config.yaml` as desired and then run the following command:
```
python3 gen_nq_data.py <path_to_v1.0-simplified_simplified-nq-train.jsonl>
```
By default, the setup script will save `v1.0-simplified_simplified-nq-train.jsonl` to the `nq/` folder.

### Training
- `train_gpt2_questioner.ipynb`
- `train_gpt2_questioner.py`

To train (i.e. fine-tune) the GPT-2 model, you can either run the `train_gpt2_questioner` notebook
or `python3 train_gpt2_questioner.py`. Both should do the same thing, but on Jupyterhub the notebook seems to be faster.

### Evaluation
- `questioner.ipynb`
- `questioner_cli.py`
- `questioner_gui.py`

To run the questioner, you have three options. There is a notebook (`questioner.ipynb`) and a CLI app (`questioner_cli.py`).
However, if integration with TTS piques your interest, you will want to run the GUI (`python3 questioner_gui.py [--voice]`).
As far as I am aware, you can only do this locally (i.e. not on Jupyterhub). The GUI comes closest to the full
artistic vision for the project, in which the program would ask its questions aloud and in a childlike voice.

## Results

Full disclosure: my results are cherry-picked.<br>
For each image, I generated 100 questions and selected the most coherent ones.

- [A `.txt` file containing examples of generated questions.](saved_questions.txt)
- [An HTML page depicting the generated questions alongside their associated images.](https://owenjow.xyz/visual-questioner)

<hr>

[![](https://user-images.githubusercontent.com/8358648/67179922-cce45d80-f38c-11e9-89c8-7f4a4154c808.gif)](https://user-images.githubusercontent.com/8358648/67179922-cce45d80-f38c-11e9-89c8-7f4a4154c808.gif)

<hr>

Here is a recording of the GUI in action.

[![Visual Questioner Demo](https://i.imgur.com/4w60PAx.png)](https://www.youtube.com/watch?v=xI02ViXsUk8)

## Technical Notes

- pip dependencies are listed in [`requirements.txt`](requirements.txt).
- As previously mentioned, the project has been tested with Python 3.6 on Ubuntu 18.04 and Python 3.7 on Jupyterhub.
- To run the speech synthesizer, pass the `--voice` flag to `questioner_gui.py`. You will need a GPU.

## Extensions

I had a few other ideas that I didn't get around to implementing.

#### Visual Attention
In the questioner interface, I thought it would be interesting to highlight what the
computer is looking at, according to attention from the captioning model. The code from the
[TensorFlow captioning tutorial](https://www.tensorflow.org/tutorials/text/image_captioning)
would have allowed easy access to this information.

#### Better Question Generation
(My full project proposal idea.) At each step of the GPT-2 sequence generation process, I would

1. Generate an embedding of the image, using either an intermediate stage of a captioning system or an autoencoder.
2. Concatenate the embedding along the feature dimension to the "token + position" embedding of the GPT-2 input pipeline.
3. Use this as the input to predict the next word of a question.

The output would be a question because I would include a discriminator to distinguish questions from non-questions,
and train that discriminator alongside the GPT-2 question generator in a GAN framework (so that the GPT-2 generator
would ultimately learn to only output question-type sentences). Additionally, in architecting the image encoder, I
would apply attention over the image so that the GPT-2 model would be able to attend to precise visual sectors while
generating a question. The final piece of the puzzle, which would encourage the questions to be relevant (in the
English language) to the images themselves, would be cycle consistency: if information were preserved after going
from image to question, we ought to be able to return successfully from question to [the relevant part of] the image.
The discriminator corresponding to the "question -> image" direction would not only measure the image reconstruction
loss, but also caption the resulting image and enforce that the caption was from the same distribution as captions
from the same part of the original image.

## References

- Papers
  - [Language Models are Unsupervised Multitask Learners](https://d4mucfpksywv.cloudfront.net/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)
- Repositories
  - [`gpt-2-simple`](https://github.com/minimaxir/gpt-2-simple)
  - [`im2txt`](https://github.com/tensorflow/models/tree/master/research/im2txt)
  - [`Real-Time-Voice-Cloning`](https://github.com/CorentinJ/Real-Time-Voice-Cloning)
- Datasets
  - [Natural Questions](https://ai.google.com/research/NaturalQuestions)

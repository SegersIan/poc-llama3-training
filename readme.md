# [POC] Llama3 Training

The idea here is to experiment how I can use LLama3 to train it on data of my own and then use this.

## Structure

* `learning-data/` is the folder where I place any training data.
* `source/` is the folder where I place the code for training a new model.
* `temp/` is the folder that I use to create temporary, intermediate files.
* `output/` is the folder where I output any new trained model

## Prequisites

* Install latest [python3](https://www.python.org/downloads/) (this was developed against `v3.12.4`)
* Install [Ollama])(https://ollama.com/)

## Flow 1: Train from Markdown Files

1. [Manual] Copy any markdown files into the `learning-data/` folder.
2. [Script] Transform all markdown files into a single text file for easy consumption.
  * `cd source/`
  * `python3 convert-markdown-to-text.py`

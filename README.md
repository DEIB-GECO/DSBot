# DSBot

DSBot is a system designed for dataset QA. The user uploads a tabular dataset (e.g., a CSV file) and express a natural language question/statement (e.g., "Show me clusters in my data"). 

DSBot elaborates the question to produce and execute a data science analysis to provide an answer to the user's question.

## Description

## Installation
In order to correctly install and run the DSBot, please start by downloading the latest source from this GitHub repository:
> git clone https://github.com/DEIB-GECO/DSBot.git

Then _cd_ into the newly created _DSBot_ folder. By convenience we suggest to create a virtual environment. For example using conda:
> conda create -n dsbot python=3.7
>
> conda activate dsbot
>
> pip install -r requirements.txt

## Train / Import the model
> cd DSBot

To build the vocabulary:

> rm wf/run/example.vocab.*
> 
>  onmt_build_vocab -config wf/en_wf.yaml -n_sample 10000

To train the model:
- join the files 'split_glove_**.txt' in a single file 'glove_new.txt'
> cd wf
> 
> cat split_glove50/* > glove_new_50.txt
> 
> cd ..
> 
> onmt_train -config wf/en_wf.yaml   

#Executing the application

## Executing RASA

### Prerequisite 
Install [Docker](https://www.docker.com/get-started) on your system

### Execution 
If you need to train the model (either because it is the first time you are installing DSBot or you changed data/nlu.yml
file), move in the main folder of DSBot and execute:

> docker-compose up

The above methods both train the model and deploy the RASA API.

If you already have a trained model, you can skip the training by executing (in the main folder of DSBot):

> docker compose start rasa

## Executing the backend
In a new Terminal
> cd DSBot
> 
> python app.py

## Executing the frontend
In a new terminal Window
> cd frontend
>
Only the first time install npm:
> npm install 

Run in development mode:
> npm run dev

Go to localhost:3000 to run the application

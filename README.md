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

# Installing the Frontend

## Creating RASA image
1. Install [Docker desktop](https://www.docker.com/products/docker-desktop) on your device


## Training RASA model
1. Open project directory on an IDE
2. Open docker compose file
3. Ensuring that the docker container is not running:
   - in VSCode right click on docker compose file and click on "compose down"
   - in PYCharm click on the stop button next to the control panel in the lower part of the screen
   - in terminal go to DSBoot root folder (the one containing docker-compose.yml file) and execute
     >docker container ls  
     
        and verify that rasa docker is not listed (i.e., running). It is running, execute
     >docker-compose -f "docker-compose.yml" down
4. Go on docker-compose.yml file. If uncommented, **comment** the following lines
    > command: >   
    >      run  
    >      --enable-api  
    >      -m 'models/<model-name>.tar.gz'
5. **Uncomment** the following lines
    >  entrypoint: /bin/bash  
    >    tty: true
6. Save the file
7. Compose the docker:
   - in VSCode right click on docker compose file and click on "compose up" 
   - in PYCHarm click on the green arrow next to Rasa line in docker compose file
   - in the terminal execute
     >docker-compose -f "docker-compose.yml" up -d --build
8. Open a shell in the container
   - in VSCode go to docker extension, right click on the container and click on "attach shell"
   - in PYCharm right click on the container running and click "new terminal"
   - in the terminal execute
        > docker exec -it <container_name> bash
     
     where <container_name> is the name of the container shown in the terminal when built. It should be dsbot_rasa_1
9. Execute in the terminal the following command:
    > rasa train nlu
10. When the training is complete, a confirmation message will appear in the terminal as the following:
    >Your Rasa model is trained and saved at '/app/models/<model-name>.tar.gz'.
11. Copy the model name and modify it in the line commented at point 4:
    >-m 'models/<model-name>.tar.gz'
12. Compose down the docker running
    - in VSCode right click on docker compose file and click on "compose down"
    - in PYCharm click on the stop button next to the control panel in the lower part of the screen
    - in terminal, digit ctrl-p ctrl-q to exit the bash, then execute
        >docker-compose -f "docker-compose.yml" down

#Executing the application

## Executing RASA
1. Open docker compose file
2. Ensuring that the docker container is not running:
   - in VSCode right click on docker compose file and click on "compose down"
   - in PYCharm click on the stop button next to the control panel in the lower part of the screen
3. If commented, **uncomment** the following lines:
    > command: >   
    >      run  
    >      --enable-api  
    >      -m 'models/<model-name>.tar.gz'
4. If uncommented, **comment** the following lines:
    >  entrypoint: /bin/bash    
    >    tty: true
5. Save the file
6. Compose the docker:
   - in VSCode right click on docker compose file and click on "compose up" 
   - in PYCHarm click on the green arrow next to Rasa line in docker compose file
   - in the terminal execute
     >docker-compose -f "docker-compose.yml" up -d --build


Rasa is up and running!

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

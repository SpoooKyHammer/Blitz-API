# ***Blitz API***

Blitz API is a RESTful service for the Blitz application.

## Requirements
- [Python v3.11](https://www.python.org/downloads/) <br>
- [Poetry v1.7.1](https://python-poetry.org/) <br>
- [Docker](https://docs.docker.com/)

## Installation
- To download the **PIFuHD** model run the following script <br>
```
sh blitz_api/ext/tasks/models/pifuhd/scripts/download_trained_model.sh
```

- To download the **lightweight-human-pose-estimation.pytorch** model run the following commands
 ```
 cd blitz_api/ext/tasks/models/lightweight-human-pose-estimation.pytorch/
 wget https://download.01.org/opencv/openvino_training_extensions/models/human_pose_estimation/checkpoint_iter_370000.pth
 ```

## API Documentation
Api documentation can be found in the following endpoint of the 
application once deployed.
> `/docs`

## Commands
**Execute these commands inside project directory.**

Install project dependencies
> `poetry install`

To run the application
> `poetry run flask --app ./blitz_api/ run` 

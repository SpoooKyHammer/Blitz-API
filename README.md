
# ***Blitz API***

Blitz API is a RESTful service for the Blitz application.

## Requirements
- Minimum of 16 GiB RAM and a CPU with 10 cores 
- [Docker](https://docs.docker.com/)

## Technologies used
- [Python v3.11](https://www.python.org/downloads/)
- [Poetry v1.7.1](https://python-poetry.org/)
-  [Celery](https://docs.celeryq.dev/en/stable/index.html) (Task Queue)
-  [Redis](https://redis.io/) (Broker and Datastore for Celery)
- [PIFuHD](https://github.com/facebookresearch/pifuhd)
- [lightweight-human-pose-estimation](https://github.com/Daniil-Osokin/lightweight-human-pose-estimation.pytorch)

## API Documentation
Api documentation can be found in the following endpoint of the 
application once deployed.
> `/docs`

## Run Application from the pre-built image
Install docker and docker-compose, ignore this step if already installed.
```
sudo apt install docker docker-compose -y
```

Create a directory for this project.
```
mkdir blitz_api && cd blitz_api/
```

Create the following two files inside this directory (Note: that the file names need to match the specified)
- `docker-compose.yml` copy the contents of [docker-compose.prod.yml](https://github.com/SpoooKyHammer/Blitz-API/blob/main/docker-compose.prod.yml) into this file.
- `nginx.conf` copy the contents of [nginx.conf](https://github.com/SpoooKyHammer/Blitz-API/blob/main/nginx.conf) into this file.

Docker login to the remote registry where our image is currently located
```
sudo docker login anicreate.azurecr.io
```

Pull the image and run the containers
```
sudo docker-compose up -d
```

## Run Application by locally building the image
Install docker and docker-compose, ignore this step if already installed.
```
sudo apt install docker docker-compose -y
```

Clone the github repository.
```
git clone https://github.com/SpoooKyHammer/Blitz-API.git
```

After cloning, cd into the directory and the first thing you should do is install the pre-trained model that our project depends on. (Note these commands are to be executed from the root directory of the project).
- To download the **PIFuHD** model run the following command. <br>
```
cd blitz_api/ext/tasks/models/pifuhd/ && sh scripts/download_trained_model.sh
```

- To download the **human_pose_estimation** model run the following command.
 ```
 cd blitz_api/ext/tasks/models/human_pose_estimation/ && wget https://download.01.org/opencv/openvino_training_extensions/models/human_pose_estimation/checkpoint_iter_370000.pth
 ```
 
We will use docker-compose to automatically build the image and run the container.
```
sudo docker-compose up -d
```

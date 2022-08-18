# __Fast API: Running multiple uvicorn servers for local development__

Lets assume that we have two separate FastAPI apps in single repository. Lets call them `app1` and `app2`. With the minimal example, the directory structure of this case will look like this,


```bash
.
├── app1                      # FastAPI app 1
│   ├── main.py               # Entrypoint for app 1
│   └── requirements.txt      # Requirements for app 1
├── app2                      # FastAPI app 2
│   ├── main.py               # Entrypoint for app 2
│   └── requirements.txt      # Requirements for app 2
├── data                      # Data for app 1 and app 2
│   ├── sample_data.csv       # Sample csv file
│   └── sample_html.html      # Sample html file
├── database1.db              # SQLite database for app 1
├── database2.db              # SQLite database for app 2
├── docker-compose.yml        # Docker compose file
├── Dockerfile                # Dockerfile for the project
└── README.md                 # README file
```

## __Running application in local:__

Now, for local development if we need to start two servers, we can run the following command:

```bash
uvicorn app1.main:app --host 0.0.0.0 --port 8001 & uvicorn app2.main:app --host 0.0.0.0 --port 8002
```

__Note:__ Here, I am not using `--reload` flag intentionally. If we do that, for change in DB, data directory or in readme the app with reload. This is not required. 


Validate all the endpoints are working for both the apps or not using the following command,

```bash
curl -X 'POST' \
  'http://0.0.0.0:8001/app1/heroes/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 0,
  "name": "app1",
  "secret_name": "hero1",
  "age": 1
}' && \
curl -X 'POST' \
  'http://0.0.0.0:8002/app2/heroes/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 0,
  "name": "app2",
  "secret_name": "hero2",
  "age": 2
}'
```

If this returns expected response, then we can be sure that the create hero endpoints are working fine. Post this we can check csv download is working or not using the following commands,

```bash
curl -X 'GET' \
  'http://0.0.0.0:8001/app1/get_csv' \
  -H 'accept: application/json' && \
curl -X 'GET' \
  'http://0.0.0.0:8002/app2/get_csv' \
  -H 'accept: application/json'
```

To kill the process usually hit `ctrl + c`. __Note:__ Even after doing this, it may happen that the application keeps running in background. To ensure that the application is not running in background, we can use the following command,

```bash
sudo kill -9 `sudo lsof -t -i:8001`
```

or


```bash
sudo kill -9 $(sudo lsof -t -i:8001)
```

Replicate the same for the all the ports if required.

## __Creating docker images and running app using docker-compose__

Here is how we can parameterize docker image building process. After running this, we can run each docker container individually or run the as docker-compose.

```bash
app_id=1
docker build --build-arg "app_id=${app_id}" -t myapp:${app_id} .
app_id=2
docker build --build-arg "app_id=${app_id}" -t myapp:${app_id} .
```

To check the content of a docker image run `docker ps`. Copy the container name, replace in the command below. Run the below command, SSH into the docker image and now you should be able see all the files present in the docker image.

```bash
docker exec -it ms_local-app2-1 /bin/bash
```

To run the application using `docker-compose` run the following commands,

```bash
docker-compose up
```

Validate all the endpoints are working for both the apps or not using the following command,

```bash
curl -X 'POST' \
  'http://0.0.0.0:8001/app1/heroes/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 0,
  "name": "app1",
  "secret_name": "hero1",
  "age": 1
}' && \
curl -X 'POST' \
  'http://0.0.0.0:8002/app2/heroes/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 0,
  "name": "app2",
  "secret_name": "hero2",
  "age": 2
}'
```

If this returns expected response, then we can be sure that the create hero endpoints are working fine. Post this we can check csv download is working or not using the following commands,

```bash
curl -X 'GET' \
  'http://0.0.0.0:8001/app1/get_csv' \
  -H 'accept: application/json' && \
curl -X 'GET' \
  'http://0.0.0.0:8002/app2/get_csv' \
  -H 'accept: application/json'
```

__Note:__ In this setup the DB will be inside a container. If you want to have consistent data in your local and inside the docker-compose setup. You need to move the local db from project root to the `data` directory. This is already being copied inside the docker image. Also you need to change the DB path in `main.py`. 

__Note:__ Do not use the same docker image for production. It will have the data directory inside the docker image. Ideally it has to be mounted using kubernetes or docker-compose. Also, the current setup will have DBs inside the container itself. But when we have some real data the DB's can be separated as docker container and we can use the same.
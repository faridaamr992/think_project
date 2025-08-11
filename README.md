# think_project

Implementation for hybrid search (Full_text , Semantic) using MongoDB and Qdrant 

## Requirements 

- Python 3.9 or later

#### Install Dependencies

```bash
sudo apt update
sudo apt install ibpq-dev gcc python3-dev
```

#### Install Python using MiniConda 

1) Download and Install MiniConda from [here](https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
)

2) Create a new environment using the following command:
```bash
$ conda create -n mini-rag python=3.9
```

3) Activate the environment:
```bash
$ conda activate mini-rag
```
## Installation

### Install the required packages 

```bash
$ pip install -r requirements.txt
```
### Setup the envirnment variables 

```bash
$ cp .env.example .env
```
Set your envirnment variables in the `.env` file like `LLM_API_KEY` value.

## Run the FastAPI server 

```bash
$ uvicorn app.main:app --reload --host 0.0.0.0
```

## Run Docker Compose Services

```bash
$ sudo ~/.docker/cli-plugins/docker-compose \
  -f docker/docker-compose.yml \
  -f docker/qdrant/docker-compose.qdrant.yml \
  up -d --build

```

## Swagger Testing 

- Open link from [here](http://127.0.0.1:8000/docs) after uvicorn run

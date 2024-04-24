# Python rest api study

### Config virtual env

### Install pyenv
See guide [pyenv](https://github.com/pyenv/pyenv)

### Create environment 

```bash
 $ pyenv install 3.12.2
 $ pyenv virtualenv 3.12.2 api-products-3.12.2
```

### Install dependencies

```bash
 $ pip install -r requirements.txt
```
### config ENVS
- Create file .env in root, and set evns

| KEY             | VALUE            |
|-----------------|------------------|
| MONGO_DB_URI    | YOUR_URI_MONGO   |
| DB_NAME         | YOUR_DB_NAME     |
| COLLECTION_NAME | COLLECTION_USERS |


### Start

```bash
 $ python -m flask --app src/main run --port=8000
```

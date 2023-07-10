# E-Wallet

### Required tools
Make sure you have installed following tools:

- python >= 3.11
- [pyenv](https://github.com/pyenv/pyenv)
- [poetry](https://python-poetry.org/)
- [pre-commit](https://pre-commit.com/)
- docker >= 24.0.2
- docker compose >= 2.19.1

### Setting up the project

#### Clone the repository (clone with SSH)
`git@github.com:greatlaki/e-wallet.git`

#### Set a local python 3.11.* version
`pyenv local 3.11.*`<br>
#### Install poetry
`pip install poetry`<br>
#### Create a `pyproject.toml`
`poetry init`<br>
#### Create new poetry virtualenv
`poetry env use 3.11.*`<br>
#### Install dependencies
`poetry install`

#### Install pre commit hooks
`pre-commit install`

Go to the folder where you cloned the project. Add variables to the dotenv file
### Variables of the dotenv file

### Django settings

| Name          | Sample                 |
|---------------|------------------------|
| SECRET_KEY    | django-insecure-8x92vy |
| DEBUG         | False                  |
| ALLOWED_HOSTS | localhost              |
| RUN_CELERY    | False                  |


### Settings of the PostgreSQL

| Name              | Sample            |
|-------------------|-------------------|
| POSTGRES_DB       | postgres_db       |
| POSTGRES_USER     | postgres_user     |
| POSTGRES_PASSWORD | postgres_password |
| POSTGRES_HOST     | 127.0.0.1         |
| POSTGRES_PORT     | 5432              |

### Docker
Then run the following command in the same directory as the `docker-compose.yml` file to start the container.
`docker compose up`

### Sending email
To use sending email, you should set up RUN_CELERY=True. Also, run redis by the a command

`docker run -d -p 6379:6379 redis`

### To run tests
`poetry run pytest`

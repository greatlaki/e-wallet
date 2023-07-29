# E-Wallet

[![codecov](https://codecov.io/gh/greatlaki/e-wallet/branch/Refactoring/Readme/graph/badge.svg?token=YBOI2S1VWE)](https://codecov.io/gh/greatlaki/e-wallet)

### About (need to add smth about the project)
...
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

### Docker
Then run the following command in the same directory as the `docker-compose.yml` file to start the container.
`docker compose up`

### Sending email
To use sending email, you should set up RUN_CELERY=True. Also, run redis by the command

`docker run -d -p 6379:6379 redis`

### To run tests
`poetry run pytest`

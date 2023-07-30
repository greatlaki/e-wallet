# E-Wallet

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/greatlaki/e-wallet/main.svg)](https://results.pre-commit.ci/latest/github/greatlaki/e-wallet/main)
[![E-Wallet CI](https://github.com/greatlaki/e-wallet/actions/workflows/ci.yml/badge.svg)](https://github.com/greatlaki/e-wallet/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/greatlaki/e-wallet/branch/main/graph/badge.svg?token=YBOI2S1VWE)](https://codecov.io/gh/greatlaki/e-wallet)

### About
The E-Wallet project is an application for managing electronic wallets using a REST API.
The system allows users to create their wallets, top them up, check their balance, withdraw funds,
and perform wallet-to-wallet transactions.

## Configuration
Configuration is stored in `.env`, for examples see `.env.example`

## Installing on a local machine
This project requires python 3.11. Python virtual environment should be installed and activated.
 Dependencies are managed by [poetry](https://python-poetry.org/) with requirements stored in `pyproject.toml`.

Install requirements:

```bash
poetry install
```

### Docker
Then run the following command in the same directory as the `docker-compose.yml` file to start the container.
`docker compose up -d`

### Sending email
To use sending email, you should set up RUN_CELERY=True. Also, run redis by the command

`docker run -d -p 6379:6379 redis`

Testing:
```bash
# run lint
make lint

# run unit tests
make test
```

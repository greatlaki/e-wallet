# E-Wallet

### Setting up the project

#### Clone the repository
`git@github.com:greatlaki/e-wallet.git`

#### Set local python
`pyenv local 3.11.4`<br>
#### Install poetry
`pip install poetry`<br>
#### Create new poetry virtualenv
`poetry env use 3.11.4`<br>
#### Install dependencies
`poetry install`

Go to the folder where you cloned the project. Add variables to the dotenv file
### Variables of the dotenv file

### Django settings

| Name          | Sample                 |
|---------------|------------------------|
| SECRET_KEY    | django-insecure-8x92vy |
| DEBUG         | False                  |
| ALLOWED_HOSTS | localhost              |
| RUN_CELERY    | False                  |


### Settings of the SQL

| Name              | Sample            |
|-------------------|-------------------|
| POSTGRES_DB       | postgres_db       |
| POSTGRES_USER     | postgres_user     |
| POSTGRES_PASSWORD | postgres_password |
| POSTGRES_HOST     | 127.0.0.1         |
| POSTGRES_PORT     | 5432              |

### Then run the following command in the same directory as the `docker-compose.yml` file to start the container.
`docker compose up`

### Sending email
<p>To use sending email, you should set up RUN_CELERY=True. Also, run redis by the a command</p>

`docker run -d -p 6379:6379 redis`

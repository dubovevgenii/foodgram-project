# foodgram-project

![Actions Status](https://github.com/dubovevgenii/foodgram-project/workflows/foodgram-project%20workflow/badge.svg)

Test link: http://130.193.45.248

This is an online service where users can publish recipes, subscribe to publications of other users, add recipes they like to the favorites list, and download a summary list of products needed to prepare one or more selected dishes before going to the store.

## Getting Started

These instructions will get you a copy of the project up and running on remote machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Be sure Docker is installed on remote system. Visit [official project site](https://docs.docker.com/engine/install/) for more information.


### Installing

To clone project to your environment run

```
git clone https://github.com/dubovevgenii/foodgram-project.git
```

### Deployment

To get the env running please follow the next steps.

After cloning from git create .env file in folder with docker-compose.yaml.
The file must consist

```
DB_NAME=<Database name>
POSTGRES_USER=<Database user>
POSTGRES_PASSWORD=<Database user password>
DB_HOST=db
DB_PORT=5432
```

Move the following files to remote machine:
* nginx folder;
* .env;
* docker-compose.yaml.

by execution the commands from project folder:

```
scp .env docker-compose.yaml Dockerfile <user_name>@<IP:/home/user_name>
scp -r nginx <user_name>@<IP:/home/user_name>
```

To github workflow add secrets for:
* DOCKER_USERNAME - Dockerhub username;
* DOCKER_PASSWORD - password for Dockerhub account;
* HOST - IP-host address of remote machine;
* SSH_KEY - SSH public key of remote machine;
* USER - username for SSH connection;
* TELEGRAM_TOKEN - bot token;
* TELEGRAM_TO - ID of telegram account.


At remote host do the following.

Run

```
sudo docker ps
```

and find ID of praktikum_web_1 container. After that execute

```
sudo docker exec -it <CONTAINER ID> bash
```

Collect static files

```
python manage.py collectstatic
```

Migrate

```
python manage.py makemigrations recipes
python manage.py migrate
```

Create superuser

```
python manage.py createsuperuser
```

Fill the database with initial test data

```
python manage.py loaddata fixtures.json
```

## Built With

* [Django](https://www.djangoproject.com/) - Web framework
* [Django REST framework](https://www.django-rest-framework.org/) - Web REST API framework
* [PostgreSQL](https://hub.docker.com/layers/postgres/library/postgres/12.4/images/sha256-9ac69ab75fd982b72064780473e1cb169884ca14c8c77ce598de53b945dcf070?context=explore) - Database Management
* [Nginx](https://hub.docker.com/layers/nginx/library/nginx/1.19.6/images/sha256-1ebd1e5add2316db67542aca3ff282f055124e86898f7d6d9a88e4ca6192422c?context=explore) - Web server
* [Docker](https://www.docker.com/) - Containerizing the application

## Authors

* **Evgenii Dubov** - [foodgram-project](https://github.com/dubovevgenii/foodgram-project)


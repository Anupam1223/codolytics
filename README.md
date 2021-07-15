# BACKEND REQUIREMENTS
  * Docker 
  * Docker Compose 
  * poetry for python package and managing environment 


# BACKEND SETUP LOCALLY
1. git clone --recursive git@gitlab.com:codolytics/api-codolytics.git
    Check if gitdataminer package exist in our main app folder(dashboard/app/app). If it does not have
    source code inside it then run `git submodule update --init --recursive`

2. Ask developer for env file which should be place adjacent to backend folder i.e just where the
   docker-compose.yml file is. 

3. Start the stack with Docker Compose:
    ```python
    docker-compose up -d
    ```
4. Now you can open your browser and interact with these URLs:

    #### Backend API - http://localhost:8888/graphql/

    #### PGAdmin, PostgreSQL web administration: http://localhost:5050

    **Note**: To check the logs while docker is building multiple services which will require considerable
    amount of time you can run 
    ```python
    docker-compose logs
    ```
    To check the logs of specific service you can run
    ```python
    docker-compose logs service_name
    ```
    e.g
    ```python
    docker-compose logs backend
    ```

NOTE: If you encountered any kind of issue, then please write it down the problem and solution either by creating an issue or wiki so that it will help other developers who faced similar issue. Your considerate nature is highly
appreciable.

## GENERAL WORKFLOW
By default, the dependencies are managed with Poetry.

From **./backend/app/** you can install all the dependencies with:

```python
poetry install
```

```python
poetry shell
```

# FILE STRUCTURE
    SQLAlchemy models are in ./backend/app/app/models
    Pydantic schemas are in ./backend/app/app/schemas
    CRUD(CREATE, READ, UPDATE, DELETE) operation in ./backend/app/app/crud
    GRAPHQL implementation in ./backend/app/app/graphql
    Dependency injections in ./backend/app/app/deps
    Error utils in ./backend/app/app/errors
    Validations in ./backend/app/app/validation
    Dataloader for batching and caching requests in ./backend/app/app/loaders


## DOCKER COMPOSE OVERRIDE 

During development, you can change Docker Compose settings that will only affect the local development environment, in the file docker-compose.override.yml.


## LIST OF CONTAINERS OR SERVICE 

The list of containers that would be created are:

   * backend (8888 port of host is mapped to container 80)
   * db (port 5432)
   * pgadmin (port 5050)
   * nginx
   * certbot for automatically renewing certificate



## REBUILD IMAGE

   ```
   docker-compose up -d --build --no-deps service_name
   ```
   e.g ``` docker-compose up -d --build --no-deps backend ```

## GET INSIDE CONTAINER

   ```
   docker-compose exec service_name bash
   ```

   e.g ```docker-compose exec db bash``` will allow me to enter inside database service

# MIGRATION EXAMPLE 

 Most commonly we will have to do the migration and for migration there are two ways
 * With one command you can directly use alembic
 ```
 docker-compose exec backend bash alembic revision --autogenerate -m "Add column 
 repo_url to Repo model"
 ```
 * Or you can first go in backend container and then run alembic
 ```
 docker-compose exec backend bash
 ```
 ```
 alembic revision --autogenerate -m "Add column repo_url to Repo model"
 ```


Connect to the database using psql inside db container:
    First you have to be inside db container and as aforementioned to get inside container you
    have to execute the service as ``` docker-compose exec db bash ```. Now you are inside the
    db container where you can use postgres related functionality.

    To connect to the database you can run ``` psql -U postgres app ``` where based on
    environment variable setup for postgres service the user for the database is postgres itself
    and app is the name of database. 

Connect to the database using psql outside db container:
    ``` psql -h localhost -p 5432 -U postgres app ```
    The reason behind the port 5432 is db container maps host's 5432 port to container's 5432 port
    which has been defined in ### docker-compose.override.yml ### as
    ```
        db:
          ports:
            - "5432:5432"
    ``` .
    Previously said, you can change however you like but only on docker-compose.override.yml file




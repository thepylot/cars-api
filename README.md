[![Build Status](https://travis-ci.com/raszidzie/cars-api.svg?branch=main)](https://travis-ci.com/raszidzie/cars-api)
# Cars API
Endpoints for car makes and models

## Getting Started
This project works on **Python 3+** and Django 2+.

Build the project by following command:

```
docker-compose build
````

and run the containers:

```
docker-compose up
```

Finally, navigate to http://localhost:8000/api

## Endpoints
The endpoints are:
* ```/api/cars```
Retrieves the list of created cars and allows to add a new car if the requested data exists in External API
* ```/api/rate```
Creates a new rate for a particular car object
* ```/api/popular```
Retrieves a list of popular cars based on number of ratings

## Testing
You can run all tests by following command:

```docker-compose run app sh -c "python manage.py test"```

to run linting tests as well update the command like below:

```docker-compose run app sh -c "python manage.py test && flake8"```

## Live Preview on Heroku
You can visit the link below too see it in production:
https://car-api-app.herokuapp.com/api/

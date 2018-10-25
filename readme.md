# Code Challenge:

## Develop two separate programs that will:

### 1st Program:
Process CSV files and send each row/data to a message queue*. An example CSV file is attached.

### 2nd Program:
Consume the messages that are sent by the 1st program and insert them into a database table**. There can only be one record with the same email address. Imagine this program will be running on multiple servers or even on the same server with multiple processes at the same time.

* Can be any production-ready distributed system such as redis, rabbitmq, sqs, or even kafka.

** Can be any modern relational database but the solution is better to be independent of the database server.

Tips And Tricks:

- Pay attention to the details in the description.
- Develop the programs as you are developing it for a production system in a real-life scenario.
- Any programming language can be used.

## Simple Documentation

There is 1 API endpoint

/api/v1/upload/csv/ --> POST
to accept a csv file then it will initiate a celery task to read this file and save the data

### Installation

All the required packages are listed in requirements.txt file.

```
pip install -r requirements.txt
```

I used django2.0, RESTFramework, celery, redis and postgresql for the database.

you need to update finCompareChallenge.settings.py with your postgresql database and redis server credentials


```
python manage.py migrate
python manage.py runserver
```

to run celery
```
celery --app=finCompareChallenge.celery:app worker --loglevel=INFO --pool=eventlet
```

example api request
```
curl -X POST --header "Content-Type:multipart/form-data;charset=UTF-8" -F file=@/home/ramadan/Downloads/sample.csv http://localhost:8000/api/v1/upload/csv/
```
## Running the tests

There are about 18 test case that provide 100% code coverage. You can run them using the command belew.

```
python manage.py test
```

## Authors

* **Ramadan K.Mostafa**
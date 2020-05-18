# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.
## API Reference
### Getting Started
- Base URL: The basic URL for trivia_app API is : ``` http://127.0.0.1:5000/api/ ```

### GET /categories
- Get all the categories
- Example: ``` curl http://127.0.0.1:5000/api/categories ```
```
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ]
}
```
## GET /questions
- It will return Categories, Questions, Total_Questions
- You have to specify The required query parameter, which is ***page***
- If you did not specify the required query parameter you will get a ***Bad Request***
### GET /questions?page={page_number}
- If the page number is not found, you will get ***Not Found*** . please refer to [Error Handling](https://github.com/YoHaNoMe/Trivia_App#error-handling) section
- Example: ``` curl http://127.0.0.1:5000/api/questions?page=1 ```
```
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ],
  "questions": [
    {
      "answer": "This is answer",
      "category": "Entertainment",
      "difficulty": 3,
      "id": 7,
      "question": "First question from React"
    },
    {
      "answer": "alberto",
      "category": "Geography",
      "difficulty": 1,
      "id": 10,
      "question": "My question"
    },
    {
      "answer": "alberot2",
      "category": "Art",
      "difficulty": 4,
      "id": 11,
      "question": "Another question"
    },
    {
      "answer": "And here is the answer",
      "category": "Entertainment",
      "difficulty": 5,
      "id": 15,
      "question": "I added this question?"
    }
  ],
  "status_code": 200,
  "success": true,
  "total_questions": 4
}
```
### GET /questions?search={search_item}
- If the search item doesn't match any question, you will get the expected result except that the ***questions*** and of course ***total_questions*** will be empty
- Example: ``` curl http://127.0.0.1:5000/api/questions?search="f" ```
```
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ],
  "questions": [
    {
      "answer": "This is answer",
      "category": "Entertainment",
      "difficulty": 3,
      "id": 7,
      "question": "First question from React"
    }
  ],
  "status_code": 200,
  "success": true,
  "total_questions": 1
}
```
## DELETE /questions/<question_id>
- Delete an existing question
- If the question id is wrong it will return ***Not Found***
- If the question somehow cannot be removed from database it return ***Not processable***
- Example: ``` curl http://127.0.0.1:5000/api/questions/12 ```
```
{
  "question_deleted_id": 12,
  "success": true
}
```

## POST /questions
- Create new question
- If you didn't specify question, answer, category_id and difficulty in the request body, you will get ***Bad Request***
- If the category isn't found, you will get ***Not Found***
- Example: ``` curl -X POST -H "Content-Type: application/json" -d '{"question": "This is question", "answer": "This is answer", "category_id": 1, "difficulty": 5}' http://127.0.0.1:5000/api/questions ```
```
{
  "question_id": 16,
  "status_code": 201,
  "success": true
}
```

## GET /categories/<category_id>/questions
- Get all questions that related to specific category
- If the category isn't found, you will get ***Not Found***
- Example: ``` curl http://127.0.0.1:5000/api/categories/2/questions ```
```
{
  "questions": [
    {
      "answer": "alberot2",
      "category": "Art",
      "difficulty": 4,
      "id": 11,
      "question": "Another question"
    }
  ],
  "status_code": 200,
  "success": true,
  "total_questions": 1
}
```
## GET /quizzes
- Get a random question from specific category that you **HAVE** to specify in query parameters
- If you didn't specify ``` category ``` in the query parameter, you will get ***Bad request***. *Note: if* ```category``` *is 0, you will get a random question from all categories*
- If you want to get a new random question you have to specify ``` prev_question``` in the query parameter, if you didn't specify ``` prev_question``` you will still get a random question but you may get the same question twice
- If the given category isn't found **OR** doesn't have any questions, you will get ***Not Found***
- Example: ``` curl http://127.0.0.1:5000/api/quizzes?category=1 ```
```
{
  "question": {
    "answer": "This is answer",
    "category": "Science",
    "difficulty": 5,
    "id": 16,
    "question": "This is question"
  },
  "status_code": 200,
  "success": true
}
```
- Example: ``` curl http://127.0.0.1:5000/api/quizzes?category=1&prev_question=16&prev_question=18 ```
```
{
  "question": {
    "answer": "This is another answer",
    "category": "Science",
    "difficulty": 5,
    "id": 20,
    "question": "This is another question"
  },
  "status_code": 200,
  "success": true
}
```
- Example when you don't have any questions to get: ``` curl http://127.0.0.1:5000/api/quizzes?category=1&prev_question=16&prev_question=18&prev_question=20 ```
```
{
  "question": null,
  "status_code": 200,
  "success": true
}
```
## Error Handling
```
{
  "message": "Not Found",
  "status_code": 404,
  "success": false
}
```
- 400: Bad Request
- 404: Not Found
- 422: Not Processable


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

# Full Stack API Final Project

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Tasks

There are `TODO` comments throughout project. Start by reading the READMEs in:

1. [`./frontend/`](./frontend/README.md)
2. [`./backend/`](./backend/README.md)

We recommend following the instructions in those files in order. This order will look familiar from our prior work in the course.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository]() and [Clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

## About the Stack

We started the full stack application for you. It is desiged with some key functional areas:

### Backend

The `./backend` directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in app.py to define your endpoints and can reference models.py for DB and SQLAlchemy setup.

### Frontend

The `./frontend` directory contains a complete React frontend to consume the data from the Flask server. You will need to update the endpoints after you define them in the backend. Those areas are marked with TODO and can be searched for expediency.

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API.

[View the README.md within ./frontend for more details.](./frontend/README.md)

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
- If the page number is not found, you will get ***Not Found*** . please refer to Error Handling section
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

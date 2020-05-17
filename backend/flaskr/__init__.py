import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs (Completed)
  '''
  cors = CORS(app, resources={r'/*': {'origins': '*'}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow (Completed)
  '''

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PATH,DELETE,OPTIONS')
      return response

  '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories. (Completed)
  '''
  @app.route('/api/categories')
  def get_categories():
      categories = [category.format() for category in Category.query.all()]
      return jsonify({'categories': categories})


  '''
  @TODO: (Completed)
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''

  # Questions Pagination | RETURN (total_questions, paginated_questions)
  def page_paginate(page):
      start= (page - 1) * QUESTIONS_PER_PAGE
      end= start + QUESTIONS_PER_PAGE
      questions = Question.query.order_by(Question.id).all()
      return len(questions), [question.format() for question in questions[start:end]]


  @app.route('/api/questions')
  def get_questions():
      questions = []
      total_questions = 0

      if 'search' in request.args: # if the user want to search for question
          search_item = request.args.get('search', '', type=str)
          questions_raw = Question.query.filter(Question.question.ilike('%{}%'.format(search_item))).all()
          questions = [question.format() for question in questions_raw]
          total_questions = len(questions)
      elif 'page' in request.args: # if the user want to get questions by page
          page = request.args.get('page', 1, type=int)
          total_questions, questions = page_paginate(page)
      else:
          abort(400)

      return jsonify({
          'questions': questions,
          'total_questions': total_questions,
          'categories': [category.format() for category in Category.query.all()],
          'success': True,
          'status_code': 200
      })

  '''
  @TODO: (Completed)
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
  @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
      question = Question.query.get(question_id)

      if not question: # Check if the question is not found
          abort(404)

      try: # Database error handler
          question.delete()
      except:
          abort(422)

      return jsonify({
          'success': True,
          'question_deleted_id': question_id
      })
  '''
  @TODO: (Completed)
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
  @app.route('/api/questions', methods=['POST'])
  def create_question():
      question = request.get_json()['question']
      answer = request.get_json()['answer']
      category_id = request.get_json()['category_id']
      difficulty = request.get_json()['difficulty']
      if not (question and answer and category_id and difficulty):
          abort(400)

      # Get Category by id
      category = Category.query.get(category_id)

      if not category: # Return 404 if category is not found
          abort(404)

      print('Quesion: {} | answer: {} | category_id: {} | difficulty: {}'.format(question, answer, category_id, difficulty))
      try:
          question_obj = Question(question, answer, category_id, difficulty)
          category.questions.append(question_obj)
          question_obj.insert()
      except:
          abort(422)

      # Successfully created question
      return jsonify({
      'success': True,
      'question_id': question_obj.id,
      'status_code': 201
      })


  '''
  @TODO: (Completed)
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''

  '''
  @TODO: (Completed)
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
  @app.route('/api/categories/<int:category_id>/questions')
  def get_category_questions(category_id):
      category = Category.query.get(category_id)
      if not category:
          abort(404)

      questions = [question.format() for question in category.questions]
      return jsonify({
        'questions': questions,
        'status_code': 200,
        'success': True,
        'total_questions': len(questions)
      })



  '''
  @TODO: (Completed)
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''

  # There is no previous question
  def load_first_random_question(questions):
      random_question = random.choice(questions)
      return random_question

  # Load n_th question (there is previous question and i want to retrieve onther one)
  def load_n_th_random_question(questions, prev_questions):
      prev_questions = [int(prev_q) for prev_q in prev_questions]

      # Check if at least on of previous questions ids is correct
      is_exist = Question.query.filter(Question.id.in_(prev_questions)).first()
      if not is_exist:
          abort(404)

      # Execlude the previous question
      next_questions = []
      for question in questions:
          if question.id in prev_questions:
              print(question.id)
              continue

          next_questions.append(question)

      random_question = None
      if next_questions:
          random_question = random.choice(next_questions)

      return random_question

  @app.route('/api/quizzes')
  def generate_random_question():
      random_question = None
      questions = None
      if 'category' in request.args: # Get questions by category

          # Get questions related to specific category or all
          if int(request.args['category']) == 0:
              questions = Question.query.all()
              print(len(questions))
          else:
              category = Category.query.get(request.args['category'])
              # Check if category is not found
              if not category:
                  abort(404)
              questions = category.questions


          if not questions: # Check if there is no questions
              abort(404)

          if 'prev_question' in request.args: # If there is previous_question
              prev_questions = request.args.getlist('prev_question')
              random_question = load_n_th_random_question(questions, prev_questions)
          else: # if there is only category in query parameter (it is first question)
              random_question = load_first_random_question(questions)

          if random_question: # There is question to retrieve | format question
              random_question = random_question.format()

          return jsonify({
          'success': True,
          'status_code': 200,
          'question': random_question
          })


      # If there is no category in query parameters
      abort(400)



  '''
  @TODO: (Completed)
  Create error handlers for all expected errors
  including 404 and 422.
  '''
  def get_error_msg(status_code, error):
      return jsonify({
        'success': False,
        'status_code': status_code,
        'message': error
      })

  @app.errorhandler(404)
  def not_found(e):
      return get_error_msg(404, 'Not Found'), 404

  @app.errorhandler(422)
  def unprocessable(e):
      return get_error_msg(422, 'Cannot be processed'), 422

  @app.errorhandler(400)
  def bad_request(e):
      return get_error_msg(400, 'Bad Request'), 400

  return app

application = create_app()

if __name__ == '__main__':
    application.run()

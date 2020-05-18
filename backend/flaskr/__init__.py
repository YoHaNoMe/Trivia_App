#!/usr/bin/python
# -*- coding: utf-8 -*-

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

    cors = CORS(app, resources={r'/*': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,PATH,DELETE,OPTIONS')
        return response

    @app.route('/api/categories')
    def get_categories():
        categories = [category.format() for category in Category.query.all()]
        return jsonify({'categories': categories})

    # Questions Pagination | RETURN (total_questions, paginated_questions)

    def page_paginate(page):
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = Question.query.order_by(Question.id).all()
        return (
            len(questions),
            [question.format() for question in questions[start:end]]
        )

    @app.route('/api/questions')
    def get_questions():
        questions = []
        total_questions = 0

        # if the user want to search for question
        if 'search' in request.args:
            search_item = request.args.get('search', '', type=str)
            questions_raw = Question.query
            .filter(Question.question.ilike('%{}%'.format(search_item)))
            .all()
            questions = [question.format() for question in questions_raw]
            total_questions = len(questions)
        elif 'page' in request.args:

            # if the user want to get questions by page
            page = request.args.get('page', 1, type=int)
            (total_questions, questions) = page_paginate(page)
        else:
            abort(400)

        return jsonify({
            'questions': questions,
            'total_questions': total_questions,
            'categories': [
                            category.format()
                            for category in Category.query.all()
                          ],
            'success': True,
            'status_code': 200,
            })

    @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)

        if not question:  # Check if the question is not found
            abort(404)

        try:  # Database error handler
            question.delete()
        except:
            abort(422)

        return jsonify({'success': True,
                       'question_deleted_id': question_id})

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

        if not category:  # Return 404 if category is not found
            abort(404)

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
            'total_questions': len(questions),
            })

    # There is no previous question

    def load_first_random_question(questions):
        random_question = random.choice(questions)
        return random_question

    # Load n_th question(there is previous question)

    def load_n_th_random_question(questions, prev_questions):
        prev_questions = [int(prev_q) for prev_q in prev_questions]

        # Check if at least on of previous questions ids is correct
        is_exist = Question.query
        .filter(Question.id.in_(prev_questions))
        .first()

        if not is_exist:
            abort(404)

        # Execlude the previous question
        next_questions = []
        for question in questions:
            if question.id in prev_questions:
                print question.id
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
        if 'category' in request.args:  # Get questions by category

            # Get questions related to specific category or all
            if int(request.args['category']) == 0:
                questions = Question.query.all()
                print len(questions)
            else:
                category = Category.query.get(request.args['category'])

                # Check if category is not found

                if not category:
                    abort(404)
                questions = category.questions

            if not questions:  # Check if there is no questions
                abort(404)
            # If there is previous_question
            if 'prev_question' in request.args:
                prev_questions = request.args.getlist('prev_question')
                random_question = load_n_th_random_question(
                    questions,
                    prev_questions
                    )
            else:
                # first question
                random_question = load_first_random_question(questions)

            # There is question to retrieve | format question
            if random_question:
                random_question = random_question.format()

            return jsonify({'success': True, 'status_code': 200,
                           'question': random_question})

        # If there is no category in query parameters
        abort(400)

    def get_error_msg(status_code, error):
        return jsonify({'success': False, 'status_code': status_code,
                       'message': error})

    @app.errorhandler(404)
    def not_found(e):
        return (get_error_msg(404, 'Not Found'), 404)

    @app.errorhandler(422)
    def unprocessable(e):
        return (get_error_msg(422, 'Cannot be processed'), 422)

    @app.errorhandler(400)
    def bad_request(e):
        return (get_error_msg(400, 'Bad Request'), 400)

    return app


application = create_app()

if __name__ == '__main__':
    application.run()

import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres:///{}".format(self.database_name)
        setup_db(self.app, self.database_path)

        self.new_valid_question = {
            'question': 'This is a question?',
            'answer': 'Answer to question',
            'category_id': 4,
            'difficulty': 2
        }

        self.new_invalid_404_question = {
            'question': 'This is a question?',
            'answer': 'Answer to question',
            'category_id': 100,
            'difficulty': 2
        }

        self.new_invalid_400_question = {
            'question': '',
            'answer': 'Answer to question',
            'category_id': 1,
            'difficulty': 2
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_create_new_question(self):
        res = self.client().post('/api/questions', json=self.new_valid_question)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['status_code'], 201)
        self.assertTrue(data['question_id'])


    def test_create_new_question_with_error_404(self):
        res = self.client().post('/api/questions', json=self.new_invalid_404_question)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['status_code'], 404)
        self.assertTrue(data['message'])

    def test_create_new_question_with_error_400(self):
        res = self.client().post('/api/questions', json=self.new_invalid_400_question)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['status_code'], 400)
        self.assertTrue(data['message'])


    def test_get_question(self):
        res = self.client().get('/api/questions?page=1')
        data = json.loads(res.data)
        self.assertEqual(data['status_code'], 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['categories']), 6)
        self.assertTrue(data['questions'])

    def test_get_question_with_wrong_query_parameters(self):
        res = self.client().get('/api/questions?wrong="wrong"')
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertTrue(data['message'])
        self.assertEqual(data['status_code'], 400)

    def test_get_all_questions_related_to_specific_category(self):
        res = self.client().get('api/categories/100/questions')
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['status_code'], 404)
        self.assertTrue(data['message'])

    def test_delete_question(self):
        res = self.client().delete('/api/questions/100')
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['status_code'], 404)
        self.assertTrue(data['message'])



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

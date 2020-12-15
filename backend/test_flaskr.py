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
        DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
        DB_USER = os.getenv('DB_USER', 'postgres')
        DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
        DB_NAME = os.getenv('DB_NAME', 'trivia_test')
        self.database_path = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
        self.sample_question = {
            'question': 'who are you?',
            'answer': 'i am the one',
            'difficulty': 9,
            'category': '2'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        new_category = Category('science')
        new_category.insert()
        new_category = Category('art')
        new_category.insert()

        categories_after_insertion = Category.query.all()
        response = self.client().get(f'/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(categories_after_insertion), len(data['categories']))
        self.assertTrue(data['success'])

    def test_get_questions(self):
        new_category = Category('science')
        new_category.insert()
        for _ in range(15):
            new_question = Question(question=self.sample_question['question'], answer=self.sample_question['answer'],
                            category=self.sample_question['category'], difficulty=self.sample_question['difficulty'])
            new_question.insert()
        questions = Question.query.all()
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(10, len(data['questions']))
        self.assertEqual(len(questions), data['total_questions'])
        self.assertTrue(data['success'])

    def test_delete_question(self):
        new_question = Question(question=self.sample_question['question'], answer=self.sample_question['answer'],
                            category=self.sample_question['category'], difficulty=self.sample_question['difficulty'])
        new_question.insert()
    
        questions_before_deletion = Question.query.all()
        response = self.client().delete(f'/questions/{new_question.id}')
        data = json.loads(response.data)

        question = Question.query.filter_by(id=new_question.id).one_or_none()
        self.assertIsNone(question)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted_id'], new_question.id)

        questions_after_deletion = Question.query.all()
        self.assertEqual(
            len(questions_after_deletion), len(questions_before_deletion) - 1)

    def test_add_question(self):
        questions_before_insertion = Question.query.all()

        response = self.client().post('/questions', json=self.sample_question)
        data = json.loads(response.data)

        questions_after_insertion = Question.query.all()

        question = Question.query.filter_by(id=data['created_id']).one_or_none()

        self.assertIsNotNone(question)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

        self.assertTrue(
            len(questions_after_insertion) == len(questions_before_insertion) + 1)
        
        return question

    def test_error_400_if_add_question_missing_params(self):
        questions_before_insertion = Question.query.all()

        response = self.client().post('/questions', json={
            'question': 'who are you?',
            'category': '2'
        })

        data = json.loads(response.data)

        questions_after_insertion = Question.query.all()

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])

        self.assertTrue(
            len(questions_after_insertion) == len(questions_before_insertion))

    def test_search_questions(self):
        new_question = Question(question='whose laptop is this?', answer='smart ans',
                            category=self.sample_question['category'], difficulty=self.sample_question['difficulty'])
        new_question.insert()

        response = self.client().get('/questions/apto')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['questions'][0]['answer'], 'smart ans')
        self.assertEqual(len(data['questions']), 1)
        new_question.delete()

    def test_404_if_search_results_are_empty(self):
        new_question = Question(question='whose shisha is this?', answer='smart ans',
                            category=self.sample_question['category'], difficulty=self.sample_question['difficulty'])
        new_question.insert()

        response = self.client().get('/questions/tootie')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
        new_question.delete()

    def test_get_questions_by_category(self):
        response = self.client().get('/categories/2/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertNotEqual(len(data['questions']), 0)

        print(data['current_category'])
        self.assertEqual(data['current_category'], '2')

    def test_quizzes(self):
        response = self.client().post('/quizzes', 
            json={'previous_questions': [3, 4, 5],
            'quiz_category': {'type': 'science', 'id': '2'}})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], '2')
        self.assertNotEqual(data['question']['id'], 3)
        self.assertNotEqual(data['question']['id'], 4)
        self.assertNotEqual(data['question']['id'], 5)


if __name__ == "__main__":
    unittest.main()
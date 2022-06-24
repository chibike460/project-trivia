import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

from dotenv import load_dotenv
load_dotenv()

database_user = os.getenv('DATABASE_USER')
test_database_name = os.getenv('TEST_DATABASE_NAME')
database_path = "postgresql://{}@{}/{}".format(database_user, 'localhost:5432', test_database_name)

new_question = {
    'question': 'Who is the best basketbal player of all time?',
    'answer': 'Michael Jordan',
    'category': 6,
    'difficulty': 1
}


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = test_database_name
        self.database_path = database_path
        setup_db(self.app, self.database_path)

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
    @Todo: Test to get categories - Success
    """
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    """
    @Todo: Test to get categories - Failure
    """
    def test_get_categories_failure(self):
        res = self.client().get("/categories/10000")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")
    
    """
    @Todo: Test to get questions - Success
    """
    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])

    """
    @Todo: Test to get questions per page - Success
    """
    def test_get_questions_per_page(self):
        res = self.client().get("/questions?page=1")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])

    """
    @Todo: Test to get questons per page - Failure (pagination value is invalid)
    """
    def test_404_get_questions_per_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

    """
    @Todo: Test to delete a question - Success
    """
    def test_delete_question(self):
        res = self.client().delete("/questions/3")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    """
    @Todo: Test to delete a question - Failure (id out of range)
    """
    def test_404_delete_question(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

    """
    @Todo: Test to create a new question - Success
    """
    def test_create_question(self):
        res = self.client().post("/questions", json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])
        self.assertTrue(data["answer"])
        self.assertTrue(data["category"])
        self.assertTrue(data["difficulty"])

    """
    @Todo: Test create a new question  - Failure
    """
    def test_404_create_question(self):
        res = self.client().post("/questions", json={"question": "Who is the best basketball player of all time?", "answer": "Michael Jordan"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable")

    """
    @Todo Test get questions by category - Success
    """

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/6/questions')

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    """
    @Todo: Test get questions by category - Failure (category out of range)
    """
    def test_404_if_category_not_found(self):
        res = self.client().get('/categories/10000/questions')

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    """
    @Todo: Test get questions by search term - Success
    """
    def test_get_questions_by_search_term(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'invent'})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])

    """
    @Todo Test get questions by search term - Failure ("searchTearm"  is wrongly spelt e.g "search" instead of "searchTerm")
    """
    def test_400_if_searchTerm_wrongly_spelt(self):
        res = self.client().post('/questions/search', json={'searc': 'invent'})

        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

    """
    @Todo Test get questions by search term - Failure ("searchTearm"  is empty or has substring not found in any question)
    """
    def test_404_if_searchTerm_is_empty(self):
        res = self.client().post('/questions/search', json={'searchTerm': ''})

        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')
    
    """
    @Todo Test to play game - Success
    """
    def test_play_game(self):
        body = {
            'previous_questions': [2, 4, 6],
            'quiz_category': {
                'id': 2
            }
        }
        res = self.client().post('/quizzes', json=body)
        
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

    """
    @Todo Test to play game - Failure (e.g: quiz_category is not in the request body or provided a value)
    """
    def test_404_if_quiz_category_not_found(self):
        body = {
            'previous_questions': [2, 4, 6],
            'quiz_category': {
                # 'id': 12349293
            }
        }
        res = self.client().post('/quizzes', json=body)
        
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")
    





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
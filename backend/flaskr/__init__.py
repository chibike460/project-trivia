import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys

from itsdangerous import json

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PATCH,PUT,POST,DELETE,OPTIONS')
        return response

    def paginate_questions(request, selection):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions

    """
    @Todo: Create endpoint to get categories
    """
    @app.route("/categories")
    def get_categories():
        try:
            all_categories = Category.query.order_by(Category.id).all()
            categories = {
                category.id: category.type for category in all_categories}
            return jsonify({
                "success": True,
                "categories": categories
            })
        except BaseException:
            abort(422)

    """
    @Todo: Create endpoint to get questions
    """
    @app.route('/questions')
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        categories = Category.query.all()

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": len(selection),
            "categories": {category.id: category.type for category in categories},
            "current_category": None
        })

    """
    @Todo: Create endpoint to delete question using a question ID.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            question.delete()
            return jsonify({
                "success": True,
                "deleted": question_id,
                "message": "Question deleted",
                "total_questions": len(Question.query.all())
            })
        except BaseException:
            abort(404)

    """
    @Todo: Create endpoint to create new questions
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        if not (new_question and new_answer and new_category and new_difficulty):
            abort(422)
        try:
            question = Question(
                question=new_question,
                answer=new_answer,
                category=new_category,
                difficulty=new_difficulty)
            question.insert()
            question = Question.query.filter(
                Question.id == question.id).one_or_none()
            question = question.format()
            question["success"] = True
            return jsonify(question)
        except BaseException:
            abort(422)

    """
    @Todo: Create endpoint to handle GET requests for questions based on category
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        category = Category.query.get(category_id)
        selection = Question.query.filter(
            Question.category == category_id).all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0 or not category:
            abort(404)

        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": len(selection),
            "current_category": category.type
        })

    """
    @Todo: Create endpoint to handle GET requests for questions based on search term
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm', None)
        selection = Question.query.filter(
            Question.question.ilike(f'%{search_term}%')).all()
        current_questions = paginate_questions(request, selection)
        if search_term is None:
            abort(400)
        elif len(current_questions) == 0 or search_term == "":
            abort(404)
        current_category_type = Category.query.filter(
            Category.id == selection[0].category).one_or_none().type
        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": len(selection),
            "current_category": current_category_type
        })

    """
    @Todo: Create endpoint to play game with random questions
    """
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_questions():
        body = request.get_json()
        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)
        
        try:
            if quiz_category['id'] == 0:
                selection = Question.query.all()
            else:
                selection = Question.query.filter(
                    Question.category == quiz_category['id']).all()
            quiz_questions = [question.format() for question in selection]
            quiz_questions = [
                question for question in quiz_questions if question['id'] not in previous_questions]
            random.shuffle(quiz_questions)
            return jsonify({"success": True, "question": quiz_questions[0] if len(
                quiz_questions) > 0 else None, })
        except BaseException:
            abort(404)

    """
    @Todo: Create error handlers for all expected errors
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        }), 500

    return app

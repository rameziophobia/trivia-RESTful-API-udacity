import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)
  
  CORS(app, resources={'/': {'origins': '*'}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                          'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                          'GET,PUT,POST,DELETE,OPTIONS')
    return response

  @app.route('/categories')
  def get_categories():
    '''
    An endpoint to handle GET requests 
    for all available categories.
    '''
    categories = {cat.id:cat.type for cat in Category.query.all()}
    
    if not len(categories):
      abort(404)
    
    return jsonify({
      'success': True,
      'categories': categories
    })


  @app.route('/questions')
  def get_questions():
    '''
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 
    '''

    questions = Question.query.all()

    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    paged_questions = questions[start:end]
    paged_questions = [question.format() for question in paged_questions]

    categories = {cat.id:cat.type for cat in Category.query.all()}
    
    if not categories or not questions:
      abort(404)

    return jsonify({
        'success': True,
        'questions': paged_questions,
        'total_questions': len(questions),
        'current category': questions[start].category,
        'categories': categories
    })


  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    '''
    An endpoint to DELETE question using a question ID. 
    '''

    try:
      question = Question.query.filter_by(id=id).one_or_none()

      if not question:
        abort(404)

      question.delete()

      return jsonify({
        'success': True,
        'deleted_id': id
    })

    except:
      abort(400)


  @app.route('/questions', methods=['POST'])
  def add_question():
    '''
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
    '''

    request_body = request.get_json()

    question_body = request_body.get('question')
    answer = request_body.get('answer')
    difficulty = request_body.get('difficulty')
    category = request_body.get('category')


    if not question_body or not difficulty or \
      not category or not answer:
      abort(400)

    try:
        question = Question(question=question_body, answer=answer,
                            difficulty=difficulty, category=category)
        question.insert()

        return jsonify({
            'success': True,
            'created_id': question.id,
            'question_created': question.question
        })

    except:
        abort(422)
    pass


  @app.route('/questions/<string:search_term>', methods=['GET'])
  def search_questions(search_term):
    '''
    Create a GET endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
    '''
    search_results = Question.query.filter(
        Question.question.ilike(f'%{search_term}%')).all()

    if not search_results:
        abort(404)

    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    paged_questions = search_results[start:end]
    paged_questions = [question.format() for question in paged_questions]

    return jsonify({
        'success': True,
        'questions': paged_questions,
        'total_questions': len(search_results)
    })


  @app.route('/categories/<string:id>/questions')
  def get_questions_by_category(id):
    '''
    GET endpoint to get questions based on category. 
    '''

    try:
      questions = Question.query.filter_by(category=id).all()
      
      if not questions:
        abort(404)

      page = request.args.get('page', 1, type=int)
      start = (page - 1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE
      paged_questions = questions[start:end]
      paged_questions = [question.format() for question in paged_questions]
      
      return jsonify({
        'success': True,
        'questions': paged_questions,
        'total_questions': len(questions),
        'current_category': questions[start].category
    })

    except:
      abort(400)


  @app.route('/quizzes', methods=['POST'])
  def quizzes():
    '''
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
    '''

    request_body = request.get_json()
    previous_questions = request_body.get('previous_questions')
    category = request_body.get('quiz_category')

    if not category or previous_questions is None:
      print(category, previous_questions)
      abort(400)

    category_id_for_all_questions = 0
    if category['id'] == category_id_for_all_questions:
        questions = Question.query.all()
    else:
        questions = Question.query.filter_by(category=category['id']).all()

    if not questions:
      abort(422)

    if len(previous_questions) == len(questions):
      return jsonify({
          'success': True
      })

    unanswered_questions = [question for question in questions if question.id not in previous_questions]

    new_question = random.choice(unanswered_questions)

    return jsonify({
        'success': True,
        'question': new_question.format()
    })

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "bad request"
      }), 400

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable_entity(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "unprocessable entity"
      }), 422
  
  return app

    
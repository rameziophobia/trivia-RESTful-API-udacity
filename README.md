# Full Stack Trivia API Project
A trivia quiz game with starter code provided by udacity.  
the task it to create a RESTful API to support the trivia game along with its test suite and documentation.

Game features

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

## Getting Started

Developers using this project should already have Python3, pip, node, and npm installed. the complete instructions for the backend and frontend are in their respective READMEs along with running instructions.
* [`Frontend`](./frontend/README.md)
* [`Backend`](./backend/README.md)
## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
python test_flaskr.py
```
Omit the dropdb command the first time you run tests.

## API Reference

### Getting Started

* Base URL: Currently this application is only hosted locally. The backend is hosted at `http://127.0.0.1:5000/`
* Authentication: This version does not require authentication or API keys.

### Error Handling

Errors are returned as JSON in the following format:<br>

    {
        "success": False,
        "error": ###,
        "message": "error message"
    }

The API will return three types of errors:

* 400 – bad request
* 404 – resource not found
* 422 – unprocessable

### Endpoints

#### GET /categories

* General: Returns the list of categories.
* Sample: `curl http://127.0.0.1:5000/categories`<br>

        {
            "categories": {
                "1": "Science",
                "2": "Art",
                "3": "Geography",
                "4": "History",
                "5": "Entertainment",
                "6": "Sports"
            },
            "success": true
        }


#### GET /questions

* General:
  * Returns the list of questions.
  * paginated in pages of 10s.
  * returns category of first question returned
  * returns list of categories
  * returns total number of questions available
* Sample: `curl http://127.0.0.1:5000/questions`  

        {
            "categories": {
                "1": "Science",
                "2": "Art",
                "3": "Geography",
                "4": "History",
                "5": "Entertainment",
                "6": "Sports"
            },
            "current category": 4,
            "questions": [
                {
                    "answer": "Maya Angelou",
                    "category": 4,
                    "difficulty": 2,
                    "id": 5,
                    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
                },
                {
                    "answer": "Muhammad Ali",
                    "category": 4,
                    "difficulty": 1,
                    "id": 9,
                    "question": "What boxer's original name is Cassius Clay?"
                },
                {
                    "answer": "Apollo 13",
                    "category": 5,
                    "difficulty": 4,
                    "id": 2,
                    "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
                },
                {
                    "answer": "Tom Cruise",
                    "category": 5,
                    "difficulty": 4,
                    "id": 4,
                    "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
                },
                {
                    "answer": "Edward Scissorhands",
                    "category": 5,
                    "difficulty": 3,
                    "id": 6,
                    "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
                },
                {
                    "answer": "Brazil",
                    "category": 6,
                    "difficulty": 3,
                    "id": 10,
                    "question": "Which is the only team to play in every soccer World Cup tournament?"
                },
                {
                    "answer": "Uruguay",
                    "category": 6,
                    "difficulty": 4,
                    "id": 11,
                    "question": "Which country won the first ever soccer World Cup in 1930?"
                },
                {
                    "answer": "George Washington Carver",
                    "category": 4,
                    "difficulty": 2,
                    "id": 12,
                    "question": "Who invented Peanut Butter?"
                },
                {
                    "answer": "Lake Victoria",
                    "category": 3,
                    "difficulty": 2,
                    "id": 13,
                    "question": "What is the largest lake in Africa?"
                },
                {
                    "answer": "The Palace of Versailles",
                    "category": 3,
                    "difficulty": 3,
                    "id": 14,
                    "question": "In which royal palace would you find the Hall of Mirrors?"
                }
            ],
            "success": true,
            "total_questions": 21
        }

#### DELETE /questions/\<int:id\>

* General:
  * Deletes a question by id using url parameters.
  * Returns id of deleted question upon success.
* Sample: `curl http://127.0.0.1:5000/questions/3 -X DELETE`  

        {
            "deleted": 3, 
            "success": true
        }

#### POST /questions

* General:
  * Creates a new question using JSON request parameters.
  * Returns JSON object with newly created question, as well as paginated questions.
* Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{
            "question": "why are we still here?",
            "answer": "just to suffer",
            "difficulty": 1,
            "category": "2"
        }'`  

        {
            "created": 43, 
            "question_created": "why are we still here?", 
            "success": true
        }


#### GET /questions/<string:search_term>

* General:
  * uses the search_term in the url params to query the questions
  * Returns the matching paginated questions.
  * returns the number of matching questions.
* Sample: `curl http://127.0.0.1:5000/questions/which`<br>

        {
            "questions": [
                {
                    "answer": "Agra", 
                    "category": 3, 
                    "difficulty": 2, 
                    "id": 15, 
                    "question": "The Taj Mahal is located in which Indian city?"
                },
                {
                    "answer": "Scarab", 
                    "category": 4, 
                    "difficulty": 4, 
                    "id": 23, 
                    "question": "Which dung beetle was worshipped by the ancient Egyptians?"
                }
            ], 
            "success": true, 
            "total_questions": 2
        }

#### GET /categories/\<string:id\>/questions

* General:
  * uses the category id in the url params to return all of that categories' questions
  * Returns paginated questions for that category.
  * returns the number of matching questions.
* Sample: `curl http://127.0.0.1:5000/categories/1/questions`  

        {
            "current_category": "Science", 
            "questions": [
                {
                    "answer": "The Liver", 
                    "category": 1, 
                    "difficulty": 4, 
                    "id": 20, 
                    "question": "What is the heaviest organ in the human body?"
                }, 
                {
                    "answer": "Alexander Fleming", 
                    "category": 1, 
                    "difficulty": 3, 
                    "id": 21, 
                    "question": "Who discovered penicillin?"
                }, 
                {
                    "answer": "Blood", 
                    "category": 1, 
                    "difficulty": 4, 
                    "id": 22, 
                    "question": "Hematology is a branch of medicine involving the study of what?"
                }
            ], 
            "success": true, 
            "total_questions": 3
        }

#### POST /quizzes

* General:
  * the endpoint used to play the game
  * Uses the following request body parameters
    * category
    * previously answered questions.
  * Returns JSON object with random question that were'nt previously answered.
* Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [3, 4, 5],
                                            "quiz_category": {"type": "Entertainment", "id": "5"}}'`<br>

        {
            "question": {
                    "answer": "Apollo 13",
                    "category": 5,
                    "difficulty": 4,
                    "id": 2,
                    "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
            }, 
            "success": true
        }

## Authors

Ramez Noshy -- readme, test_flaskr.py, flaskr/__init__.py  
The fronend, all other boilerplate code and the project structure was provided by Udacity

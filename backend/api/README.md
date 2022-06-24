# API Reference

## **Introduction**

### **Getting Started**
- Base URL: Trivia app can only be run locally and is not hosted. This means there is no base url. Backend, this app.lication is hosted at, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### **Error Handling**
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 404,
    "message": "Resource not found"
}
```
The API will return five error types when requests fail. They include:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 
- 500: Internal Server Error
- 405: Method Not Allowed

### **Endpoints Library** 
#### _GET **/categories**_
- General:
    - Fetches a dictionary of categories in which the keys are the ids and the values are the corresponding string of the category.
    - Request Arguments: None
    - Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.
- Sample: `curl http://127.0.0.1:5000/categories`

```  
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
```

#### _GET **/questions**_
- General:
    - Returns a list of questions, success value, total number of questions, categories and current category.
    - Results are paginated in groups of 10. Includes a request argument ("_page_") to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions`

```  
 {
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
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
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 19
}

```

#### _DELETE **/questions/{question_id}**_
- General:
    - Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value, total questions (updated after deletion), and message.
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/16?page=2`
```
 {
  "deleted": 16,
  "message": "Question deleted",
  "success": true,
  "total_questions": 18
}

```

#### _POST **/questions**_
- General:
    - Creates a new question, which will require the question and answer text, category, and difficulty score. 
    - Returns the id of the created question, success value, total questions, and question list based on current page number to update the frontend. 
- Sample: `curl http://127.0.0.1:5000/questions?page=2 -X POST -H "Content-Type: application/json" -d '{"question":"Under whose administration in Nigeria did things go from bad to incredibly stupid, ecnomically?", "answer":"Mohammed Buhari", "category":"4", "difficulty":"3"}'`
```
{
  "answer": "Mohammed Buhari",
  "category": 4,
  "difficulty": 3,
  "id": 37,
  "question": "Under whose administration in Nigeria did things go from bad to incredibly stupid, ecnomically?",
  "success": true
}

```

#### _POST **/questions/search**_
- General:
    - Get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
- Sample: `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "Nigeria"}'`

```
{
  "current_catergoy": "History",
  "questions": [
    {
      "answer": "Mohammed Buhari",
      "category": 4,
      "difficulty": 3,
      "id": 37,
      "question": "Under whose administration in Nigeria did things go from bad to incredibly stupid, ecnomically?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```


#### _GET **/categories/{category_id}/questions**_
- General:
    - Returns a list of questions based on category, success value, total number of questions in that category, categories and current category.
    - Results are paginated in groups of 10. 
- Sample: `curl http://127.0.0.1:5000/categories/4/questions`
```
{
  "current_category": "History",
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
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    },
    {
      "answer": "Mohammed Buhari",
      "category": 4,
      "difficulty": 3,
      "id": 37,
      "question": "Under whose administration in Nigeria did things go from bad to incredibly stupid, ecnomically?"
    }
  ],
  "success": true,
  "total_questions": 5
}

```

#### _POST **/quizzes**_
- General:
    - Get questions to play the quiz.This endpoint takes category and previous question parameters and return a random questions within the given category,
      if provided, and that is not one of the previous questions. 
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": [2, 4, 6], "quiz_category": {"id": "2"}}' http://localhost:5000/quizzes`
```
{
  "question": {
    "answer": "One",
    "category": 2,
    "difficulty": 4,
    "id": 18,
    "question": "How many paintings did Van Gogh sell in his lifetime?"
  },
  "success": true
}
```
# Trivia App

Tivia is a web application that allows users to play trivia games and feeds off a RestfulAPI from the backend..

![Image of Trivia App](./Trivia%20img.png)

This application has the functionality to:

1. Display questions - both all questions and by category. Questions show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

The codebase follows Pep8 style guidelines.

## Getting Started

[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine.

### Trivia - Backend

The [backend](./backend/) directory contains a completed Flask, SQLAlchemy server and Test file to test all API endpoints (success and failure cases).

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/) directory contains a React frontend to consume the data from the Flask server.
The frontend is built using [create-react-app](https://create-react-app.dev/) and the [React Router](https://reacttraining.com/react-router/web/guides/quick-start) library.

#### The Frontend README reveals the following:

1. End points and HTTP methods expected to be consumed?
2. Request format needed by frontend - does it expect certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

Please note that the above scripts should only be changed if you know what you're doing.

> View the [Frontend README](./frontend/README.md) for more details.

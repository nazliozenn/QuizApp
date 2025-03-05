from fastapi import FastAPI, HTTPException, Depends, Request, Form, Response
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from typing import List
import uvicorn
import random

# Initialize FastAPI app
app = FastAPI(
    title="Quiz App",
    description="A simple quiz application API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./quiz.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Updated SQLAlchemy model setup
class Base(DeclarativeBase):
    pass

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, index=True)
    correct_answer = Column(String)
    option1 = Column(String)
    option2 = Column(String)
    option3 = Column(String)
    option4 = Column(String)

# Create database tables
Base.metadata.create_all(bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root route
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Quiz App API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .container { max-width: 800px; margin: 0 auto; }
                h1 { color: #333; }
                .endpoint { margin: 20px 0; padding: 10px; background: #f5f5f5; border-radius: 5px; }
                .button {
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #1976d2;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 10px 0;
                }
                .button:hover {
                    background-color: #1565c0;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Welcome to Quiz App</h1>
                <div class="endpoint">
                    <h2>Available Options:</h2>
                    <ul>
                        <li><a href="/start-quiz" class="button">Start Quiz</a></li>
                        <li><a href="/api/questions">View All Questions</a></li>
                        <li><a href="/api/add-sample-questions">Add Sample Questions</a></li>
                    </ul>
                </div>
            </div>
        </body>
    </html>
    """

# API Routes
@app.get("/api/questions", response_class=HTMLResponse)
async def list_questions(db: Session = Depends(get_db)):
    questions = db.query(Question).all()
    
    # Create an HTML response
    html_content = """
    <html>
        <head>
            <title>Quiz Questions</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .container { max-width: 800px; margin: 0 auto; }
                .question-card { 
                    border: 1px solid #ddd; 
                    padding: 20px; 
                    margin: 20px 0; 
                    border-radius: 5px;
                    background-color: #f9f9f9;
                }
                .options { margin-left: 20px; }
                .correct-answer { color: green; font-weight: bold; }
                .no-questions { 
                    text-align: center; 
                    color: #666; 
                    margin: 40px 0;
                }
                .back-link {
                    display: inline-block;
                    margin-bottom: 20px;
                    color: #1976d2;
                    text-decoration: none;
                }
                .back-link:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <a href="/" class="back-link">← Back to Home</a>
                <h1>Quiz Questions</h1>
    """
    
    if not questions:
        html_content += """
                <div class="no-questions">
                    <h2>No questions available</h2>
                    <p>Click <a href="/api/add-sample-questions">here</a> to add sample questions.</p>
                </div>
        """
    else:
        for i, question in enumerate(questions, 1):
            html_content += f"""
                <div class="question-card">
                    <h3>{i}. {question.question_text}</h3>
                    <div class="options">
                        <p>A) {question.option1}</p>
                        <p>B) {question.option2}</p>
                        <p>C) {question.option3}</p>
                        <p>D) {question.option4}</p>
                    </div>
                    <p class="correct-answer">Correct Answer: {question.correct_answer}</p>
                </div>
            """
    
    html_content += """
            </div>
        </body>
    </html>
    """
    return html_content

@app.get("/api/add-sample-questions", response_class=HTMLResponse)
async def add_sample_questions(db: Session = Depends(get_db)):
    sample_questions = [
        {
            "question_text": "What is the capital of France?",
            "correct_answer": "Paris",
            "option1": "Paris",
            "option2": "London",
            "option3": "Berlin",
            "option4": "Madrid"
        },
        {
            "question_text": "Which planet is known as the Red Planet?",
            "correct_answer": "Mars",
            "option1": "Venus",
            "option2": "Mars",
            "option3": "Jupiter",
            "option4": "Saturn"
        },
        {
            "question_text": "What is 2 + 2?",
            "correct_answer": "4",
            "option1": "3",
            "option2": "4",
            "option3": "5",
            "option4": "6"
        },
        {
            "question_text": "Who painted the Mona Lisa?",
            "correct_answer": "Leonardo da Vinci",
            "option1": "Vincent van Gogh",
            "option2": "Pablo Picasso",
            "option3": "Leonardo da Vinci",
            "option4": "Michelangelo"
        },
        {
            "question_text": "What is the largest ocean on Earth?",
            "correct_answer": "Pacific Ocean",
            "option1": "Atlantic Ocean",
            "option2": "Indian Ocean",
            "option3": "Pacific Ocean",
            "option4": "Arctic Ocean"
        },
        {
            "question_text": "Which element has the chemical symbol 'Au'?",
            "correct_answer": "Gold",
            "option1": "Silver",
            "option2": "Gold",
            "option3": "Copper",
            "option4": "Aluminum"
        },
        {
            "question_text": "What is the capital of Japan?",
            "correct_answer": "Tokyo",
            "option1": "Seoul",
            "option2": "Beijing",
            "option3": "Tokyo",
            "option4": "Bangkok"
        },
        {
            "question_text": "Who wrote 'Romeo and Juliet'?",
            "correct_answer": "William Shakespeare",
            "option1": "Charles Dickens",
            "option2": "Jane Austen",
            "option3": "Mark Twain",
            "option4": "William Shakespeare"
        },
        {
            "question_text": "What year did World War II end?",
            "correct_answer": "1945",
            "option1": "1943",
            "option2": "1944",
            "option3": "1945",
            "option4": "1946"
        },
        {
            "question_text": "Which programming language was created by Guido van Rossum?",
            "correct_answer": "Python",
            "option1": "Java",
            "option2": "Python",
            "option3": "C++",
            "option4": "JavaScript"
        },
        {
            "question_text": "What is the square root of 144?",
            "correct_answer": "12",
            "option1": "10",
            "option2": "11",
            "option3": "12",
            "option4": "14"
        },
        {
            "question_text": "Which animal is known as the 'King of the Jungle'?",
            "correct_answer": "Lion",
            "option1": "Tiger",
            "option2": "Lion",
            "option3": "Elephant",
            "option4": "Gorilla"
        },
        {
            "question_text": "What is the hardest natural substance on Earth?",
            "correct_answer": "Diamond",
            "option1": "Gold",
            "option2": "Iron",
            "option3": "Diamond",
            "option4": "Platinum"
        },
        {
            "question_text": "Who invented the telephone?",
            "correct_answer": "Alexander Graham Bell",
            "option1": "Thomas Edison",
            "option2": "Alexander Graham Bell",
            "option3": "Nikola Tesla",
            "option4": "Albert Einstein"
        },
        {
            "question_text": "What is the main component of the Sun?",
            "correct_answer": "Hydrogen",
            "option1": "Oxygen",
            "option2": "Carbon",
            "option3": "Helium",
            "option4": "Hydrogen"
        }
    ]
    
    # Clear existing questions first
    db.query(Question).delete()
    
    for q_data in sample_questions:
        question = Question(**q_data)
        db.add(question)
    
    db.commit()

    return """
    <html>
        <head>
            <title>Adding Sample Questions</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; text-align: center; }
                .container { max-width: 800px; margin: 0 auto; }
                .message { 
                    padding: 20px;
                    background-color: #e8f5e9;
                    border-radius: 5px;
                    margin: 20px 0;
                }
                .redirect-message {
                    margin-top: 20px;
                    color: #666;
                }
            </style>
            <meta http-equiv="refresh" content="2;url=/api/questions" />
        </head>
        <body>
            <div class="container">
                <div class="message">
                    <h2>15 Sample Questions Added Successfully!</h2>
                </div>
                <div class="redirect-message">
                    <p>Redirecting to questions list...</p>
                    <p>Click <a href="/api/questions">here</a> if you're not redirected automatically.</p>
                </div>
            </div>
        </body>
    </html>
    """

@app.post("/api/questions")
async def create_question(
    question_text: str = Form(...),
    correct_answer: str = Form(...),
    option1: str = Form(...),
    option2: str = Form(...),
    option3: str = Form(...),
    option4: str = Form(...),
    db: Session = Depends(get_db)
):
    question = Question(
        question_text=question_text,
        correct_answer=correct_answer,
        option1=option1,
        option2=option2,
        option3=option3,
        option4=option4
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return {"message": "Question created successfully", "question": question}

@app.get("/start-quiz", response_class=HTMLResponse)
async def start_quiz(db: Session = Depends(get_db)):
    questions = db.query(Question).all()
    if not questions:
        return """
        <html>
            <head>
                <title>Quiz App - No Questions</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; text-align: center; }
                    .container { max-width: 800px; margin: 0 auto; }
                    .message { padding: 20px; background-color: #fff3e0; border-radius: 5px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="message">
                        <h2>No questions available</h2>
                        <p>Please <a href="/api/add-sample-questions">add some questions</a> first.</p>
                    </div>
                </div>
            </body>
        </html>
        """
    
    # Shuffle questions and select first 5 (or all if less than 5)
    quiz_questions = random.sample(questions, min(5, len(questions)))
    
    html_content = """
    <html>
        <head>
            <title>Take Quiz</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .container { max-width: 800px; margin: 0 auto; }
                .question-card { 
                    border: 1px solid #ddd; 
                    padding: 20px; 
                    margin: 20px 0; 
                    border-radius: 5px;
                    background-color: #f9f9f9;
                }
                .option-label {
                    display: block;
                    padding: 10px;
                    margin: 5px 0;
                    cursor: pointer;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                }
                .option-label:hover {
                    background-color: #e3f2fd;
                }
                .submit-btn {
                    background-color: #1976d2;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                }
                .submit-btn:hover {
                    background-color: #1565c0;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Quiz Time!</h1>
                <form action="/submit-quiz" method="post">
    """
    
    for i, question in enumerate(quiz_questions, 1):
        options = [
            (question.option1, "A"),
            (question.option2, "B"),
            (question.option3, "C"),
            (question.option4, "D")
        ]
        
        html_content += f"""
            <div class="question-card">
                <h3>{i}. {question.question_text}</h3>
                <input type="hidden" name="question_{i}_id" value="{question.id}">
                <input type="hidden" name="correct_{i}" value="{question.correct_answer}">
        """
        
        for option, letter in options:
            html_content += f"""
                <label class="option-label">
                    <input type="radio" name="answer_{i}" value="{option}" required>
                    {letter}) {option}
                </label>
            """
        
        html_content += "</div>"
    
    html_content += """
                <button type="submit" class="submit-btn">Submit Quiz</button>
                </form>
            </div>
        </body>
    </html>
    """
    return html_content

@app.post("/submit-quiz", response_class=HTMLResponse)
async def submit_quiz(request: Request):
    form_data = await request.form()
    total_questions = len([k for k in form_data.keys() if k.startswith("question_")]) 
    correct_answers = 0
    
    results = []
    for i in range(1, total_questions + 1):
        user_answer = form_data.get(f"answer_{i}")
        correct = form_data.get(f"correct_{i}")
        is_correct = user_answer == correct
        if is_correct:
            correct_answers += 1
        results.append({
            "user_answer": user_answer,
            "correct_answer": correct,
            "is_correct": is_correct
        })
    
    score_percentage = (correct_answers / total_questions) * 100
    
    return f"""
    <html>
        <head>
            <title>Quiz Results</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .container {{ max-width: 800px; margin: 0 auto; }}
                .result-card {{ 
                    border: 1px solid #ddd;
                    padding: 20px;
                    margin: 20px 0;
                    border-radius: 5px;
                    text-align: center;
                }}
                .score {{
                    font-size: 24px;
                    color: {('#4caf50' if score_percentage >= 70 else '#f44336')};
                    font-weight: bold;
                }}
                .button {{
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #1976d2;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 10px 5px;
                }}
                .button:hover {{
                    background-color: #1565c0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="result-card">
                    <h1>Quiz Results</h1>
                    <p class="score">Your Score: {score_percentage:.1f}%</p>
                    <p>Correct Answers: {correct_answers} out of {total_questions}</p>
                    <div>
                        <a href="/start-quiz" class="button">Take Another Quiz</a>
                        <a href="/" class="button">Back to Home</a>
                    </div>
                </div>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

Ultimate Quiz Game
This is a console-based Python quiz game that features:
    -Category selection from 10 topics
    -Difficulty levels (Easy, Medium, Hard)
    -Text-to-Speech (TTS) support (optional)
    -10-second timer for each question
    -Automatic fallback to local questions if the online API fails
    -Retry options after each game

Features:

1.Categories:
    General Knowledge
    Science and Nature
    Computers
    Mythology
    Sports
    Geography
    History
    Vehicles
    Music
    Video Games

2.Difficulty:
    Easy
    Medium
    Hard

3.TTS (Text-to-Speech):
    Game will ask if you want TTS enabled.
    If enabled and supported on your system, questions and options will be read aloud.

4.Timer:
    You get 10 seconds to answer each question.
    If you fail to answer in time, the correct answer will be shown automatically.

5.Question Sources:
    Primary: Open Trivia DB API
    Fallback: Local file local_questions.json (must be present in the same directory).

6.Scoring System:
    Your final score is shown along with a performance rating:
    Below Average
    Average
    Above Average
    Extraordinary
    !!!God!!!

Requirements
Python 3.x
Required Python packages:
  -requests
  -inputimeout
  -pyttsx3

Install them via pip:
```pip install requests inputimeout pyttsx3```

How to Run
Make sure you have Python 3 installed.
Install the required modules.
Keep a file named local_questions.json in the same folder (for fallback).

Run the program:
```python quiz_game.py```

Important Notes
If TTS initialization fails, the game will continue without voice prompts.
If API fetch fails, the game will automatically switch to local questions.
The local_questions.json must be structured according to categories (same names as listed above).
If both API and local loading fail, the program will exit gracefully.
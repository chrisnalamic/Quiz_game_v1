import pyttsx3 as tts
import sys
import requests as rq
import random
import html
from inputimeout import inputimeout,TimeoutOccurred

tts_availability = True
try:
    engine = tts.init()
except Exception as e:
    print(f"Text-To-Speech not available on this system: {e}")
    tts_availability = False

def speak(text, use_tts):
    if use_tts:
        try:
            engine.say(text)
            engine.runAndWait()
        except:
            pass

def ask_tts():
    while True:
        tts_choice = input("\nDo you want Text To Speech on? Yes or No? ").strip().upper()
        if tts_choice == 'YES':
            return True
        elif tts_choice == 'NO':
            return False
        else:
            print("\nType yes or no!!!")

class QuizGame:
    def __init__(self, qna, use_tts):
        self.qna = qna
        self.score = 0
        self.use_tts = use_tts

    def play(self):
        print("You willl have 10 seconds for each question.\n")
        speak("You willl have 10 seconds for each question",self.use_tts)
        for index, values in enumerate(self.qna['results'], 1):
            incorrect_options = values['incorrect_answers']
            correct_option = html.unescape(values['correct_answer'])
            all_options = [html.unescape(opt) for opt in incorrect_options] + [correct_option]
            random.shuffle(all_options)

            question = html.unescape(values['question'])

            print(f"\n{index}. {question}")
            speak(f"Question {index}. {question}", self.use_tts)

            for i, v in enumerate(all_options, 1):
                print(f"    {i}: {v}")
                speak(f"Option {i}: {v}", self.use_tts)
            
            print("Enter your answer (1-4)")
            while True:
                speak("Enter your answer from one to four", self.use_tts)
                try:
                    submit=inputimeout(prompt=" ",timeout=10)
                    if submit.isdigit():
                        submit = int(submit) - 1
                        if 0 <= submit < len(all_options):
                            if all_options[submit] == correct_option:
                                print("Correct!")
                                speak("Correct!", self.use_tts)
                                self.score += 1
                            else:
                                print(f"Wrong! The correct answer is: {correct_option}")
                                speak(f"Wrong! The correct answer is {correct_option}", self.use_tts )
                            break
                        else:
                            print("Select 1-4 only.")
                            speak("Select one to four only", self.use_tts)
                    else:
                        print("Enter a number only.")
                        speak("Enter a number only", self.use_tts)

                except TimeoutOccurred:
                    print("Oops! Ran out of Time")
                    print(f"The correct answer is: {correct_option}")
                    speak(f"The correct answer is {correct_option}", self.use_tts)
                    print("Moving to the next question...")
                    speak("Moving to the next question",self.use_tts)
                    break

    def result(self):
        try:
            percentage = (self.score / 15) * 100
            print(f"\nYou got {self.score} correct.")
            speak(f"You got {self.score} correct.", self.use_tts)

            print(f"You got {percentage:.2f}% of the questions right! You are:")
            speak(f"You got {percentage:.2f} percent right. You are", self.use_tts)

            if percentage <= 30:
                level = "Below Average"
            elif percentage <= 50:
                level = "Average"
            elif percentage <= 70:
                level = "Above Average"
            elif percentage <= 90:
                level = "Extraordinary!"
            else:
                level = "!!!God!!!"

            print(level)
            speak(level, self.use_tts)

        except Exception as e:
            print(f"Error calculating results: {e}")
            speak("There was an error calculating your results", self.use_tts)

    def again(self):
        while True:
            speak("Do you want to try again? Say Yes for Same Quiz, Menu for categories, or No for quitting", self.use_tts)
            choice = input("\nTry again? (Yes/Same Quiz, Menu/Main Menu, No/Quit): ").strip().upper()
            if choice == 'YES':
                self.play()
                self.result()
            elif choice == 'MENU':
                main()
            elif choice == 'NO':
                print("Thank you for playing!!!")
                speak("Thank you for playing", self.use_tts)
                sys.exit()
            else:
                print("Enter yes, menu or no.")
                speak("Enter yes, menu or no", self.use_tts)

def category_selection(use_tts):
    print("\nWelcome to the Ultimate Quiz Game Version 4")
    speak("Welcome to the Ultimate Quiz Game Version 4", use_tts)

    categories = [
        "Film", "General Knowledge", "Science and Nature", "Computers", "Mathematics",
        "Mythology", "Sports", "Geography", "History", "Art", "Celebrity",
        "Politics", "Vehicles", "Animals", "Gadgets", "Music", "Video Games"
    ]

    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")
        speak(f"{i}. {cat}", use_tts)
    print("0. Quit")
    speak("Enter 0 to quit", use_tts)

    category_ids = ['1', '9', '17', '18', '19', '20', '21', '22', '23', '25', '26', '24', '28', '27', '30', '12', '15']

    while True:
        choice = input("Enter: ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 0 <= idx <= 17:
                if idx == 0:
                    print("\nThank you for your time.")
                    speak("Thank you for your time", use_tts)
                    sys.exit()
                else:
                    print(f"\nYou've selected {categories[idx-1]}")
                    speak(f"You've selected {categories[idx-1]}", use_tts)
                    return category_ids[idx-1]
        print("\nEnter a valid number (0-17).")
        speak("Enter a valid number between zero and seventeen", use_tts)

def difficulty_selection(use_tts):
    print("\nSelect a difficulty:" \
          "\n1. Easy" \
          "\n2. Medium" \
          "\n3. Hard" \
          "\n4. Change Category" \
          "\n0. Quit")
    speak("Select a difficulty. One for easy, two for medium, three for hard, four for change category, or zero to quit.", use_tts)

    while True:
        choice = input("Enter: ").strip()
        if choice.isdigit():
            difficulty = int(choice)
            if difficulty == 1:
                return "easy"
            elif difficulty == 2:
                return "medium"
            elif difficulty == 3:
                return "hard"
            elif difficulty == 4:
                return category_selection(use_tts)
            elif difficulty == 0:
                print("\nThank you for playing.")
                speak("Thank you for playing", use_tts)
                sys.exit()
        print("\nEnter a valid number (0-4).")
        speak("Enter a valid number between zero and four", use_tts)

def main():
    use_tts = tts_availability and ask_tts()
    category = category_selection(use_tts)
    difficulty = difficulty_selection(use_tts)

    url = f"https://opentdb.com/api.php?amount=15&category={category}&difficulty={difficulty}&type=multiple"

    try:
        response = rq.get(url, timeout=10)
        if response.status_code == 200:
            qna = response.json()
            if qna["response_code"] == 0:
                quiz = QuizGame(qna, use_tts)
                quiz.play()
                quiz.result()
                quiz.again()
            else:
                print(f"\nCould not retrieve questions for this category at {difficulty}.")
                speak("Could not retrieve questions. Try again later.", use_tts)
        else:
            print("Failed to fetch questions. Try again later.")
            speak("Failed to fetch questions. Try again later.", use_tts)
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("An error occurred while retrieving questions.", use_tts)

if __name__ == "__main__":
    main()

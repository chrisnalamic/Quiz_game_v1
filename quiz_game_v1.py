import pyttsx3 as tts
import sys
import requests as rq
import random
import html
from inputimeout import inputimeout,TimeoutOccurred
import json

categories = [
         "General Knowledge", "Science and Nature", "Computers",
        "Mythology", "Sports", "Geography", "History", 
         "Vehicles", "Music", "Video Games"
    ]

#Initializing tts if possible in the system
tts_availability = True
try:
    engine = tts.init()
except Exception as e:
    print(f"Text-To-Speech not available on this system: {e}")
    tts_availability = False

#Function that is used to Read the text out if tts is enabled by user and possible in the system
def speak(text, use_tts):
    global tts_availability
    if use_tts:
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"(TTS Error: {e}. Disabling TTS for this session.)")
            tts_availability = False

#Function that asks user to either enable or disable tts if initialization is sucessful
def ask_tts():
    while True:
        tts_choice = input("\nDo you want Text To Speech on? Yes or No? ").strip().upper()
        if tts_choice == 'YES':
            return True
        elif tts_choice == 'NO':
            return False
        else:
            print("\nType yes or no!!!")

#this fucntion will help to load the local questions in case of API or network failure
def load_local_questions(use_tts):
    try:
        with open("local_questions.json","r") as file:
            local_file=json.load(file)
        return local_file
    except Exception as e:
        print(f"Error occured while loading local questions: {e}")
        speak(f"Error occured while loading local questions",use_tts)
        return None

def local_process(use_tts,idx):
    qna=load_local_questions(use_tts)
    quiz = QuizGame(qna[f"{categories[idx-1]}"], use_tts)
    quiz.play()
    quiz.result()
    quiz.again()


#The actual quiz game starts within the class
class QuizGame:
    #initialization of the class object, qna stores the question and answer data in a dictionery
    def __init__(self, qna, use_tts):
        self.qna = qna
        self.score = 0
        self.use_tts = use_tts
    
    #function that will facilitate the quiz_game playing mechanics
    def play(self):
        self.score=0
        print("You will have 10 seconds for each question.\n")
        speak("You will have 10 seconds for each question",self.use_tts)

        #invisible timer, set to 10 seconds with the help of inputimeout module
        for index, values in enumerate(self.qna['results'], 1):
            incorrect_options = values['incorrect_answers']
            correct_option = html.unescape(values['correct_answer'])
            all_options = [html.unescape(opt) for opt in incorrect_options] + [correct_option]
            #html.unescape used which helps rewrite the codes into symbols they are originally supposed to be 
            random.shuffle(all_options)

            question = html.unescape(values['question'])

            #printing the questions and answer options
            print(f"\n{index}. {question}")
            speak(f"Question {index}. {question}", self.use_tts)

            for i, v in enumerate(all_options, 1):
                print(f"    {i}: {v}")
                speak(f"Options {i}: {v}", self.use_tts)
            
            #taking in user input and adjusting the score accordingly
            print("Enter your answer (1-4)")
            speak("Enter your answer from one to four", self.use_tts)
            while True:
                try:
                    submit=inputimeout(prompt="",timeout=10)
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
                    speak("Oops! Ran out of Time",self.use_tts)
                    print(f"The correct answer is: {correct_option}")
                    speak(f"The correct answer is {correct_option}", self.use_tts)
                    print("Moving to the next question...")
                    speak("Moving to the next question",self.use_tts)
                    break

    #displaying what the user got in that particular quiz session
    def result(self):
        try:
            percentage = (self.score / len(self.qna['results'])) * 100
            print(f"\nYou got {self.score} correct.")
            speak(f"You got {self.score} correct.", self.use_tts)

            print(f"You got {percentage:.2f}% of the questions right! You are:")
            speak(f"You got {percentage:.2f} percent of the questions right. You are", self.use_tts)

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

    #providing user with different option to play again or to quit
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

#function that facilitates the selection of category 
def category_selection(use_tts):
    print("\nWelcome to the Ultimate Quiz Game")
    speak("Welcome to the Ultimate Quiz Game", use_tts)

    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")
        speak(f"{i}. {cat}", use_tts)
    print("0. Quit")
    speak("Enter 0 to quit", use_tts)

    category_ids = ['9', '17', '18', '20', '21', '22', '23', '28', '12', '15']

    while True:
        choice = input("Enter: ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 0 <= idx <= len(categories):
                if idx == 0:
                    print("\nThank you for your time.")
                    speak("Thank you for your time", use_tts)
                    sys.exit()
                else:
                    print(f"\nYou've selected {categories[idx-1]}")
                    speak(f"You've selected {categories[idx-1]}", use_tts)
                    return category_ids[idx-1],idx
        print(f"\nEnter a valid number (0-{len(categories)}).")
        speak(f"Enter a valid number between zero and {len(categories)}", use_tts)

#function that facilitates the selection of difficulty level
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
                main()
                sys.exit()
            elif difficulty == 0:
                print("\nThank you for playing.")
                speak("Thank you for playing", use_tts)
                sys.exit()
        print("\nEnter a valid number (0-4).")
        speak("Enter a valid number between zero and four", use_tts)

#main function which the program will seek to access first because of if__name__="__main__": main()
def main():
    use_tts = tts_availability and ask_tts()
    category, idx= category_selection(use_tts)
    difficulty = difficulty_selection(use_tts)

    url = f"https://opentdb.com/api.php?amount=15&category={category}&difficulty={difficulty}&type=multiple"

    try:
        print("Trying to fetch online questions...")
        speak("Trying to fetch online questions",use_tts)
        response = rq.get(url, timeout=10)
        if response.status_code != 200:
            speak("Bad HTTP status code",use_tts)
            raise Exception("Bad HTTP status code.")

        qna = response.json()
        if qna["response_code"] != 0:
            speak("API response_code indicates no questions",use_tts)
            raise Exception("API response_code indicates no questions.")
    
        # No problems, start the quiz
        quiz = QuizGame(qna, use_tts)
        quiz.play()
        quiz.result()
        quiz.again()

    except Exception as e:
        print(f"Error during online fetching: {e}. Switching to local questions instead.")
        speak("Error during online fetching, Switching to local questions instead.", use_tts)
        try:
            local_process(use_tts, idx)
        except Exception as local_err:
            print(f"Local questions error: {local_err}. Exiting program.")
            speak("Local questions error. Exiting program.", use_tts)
            sys.exit()

if __name__ == "__main__":
    main()

from flask import Flask, request, render_template, redirect, flash, session
from random import randint, choice, sample
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)

app.config['SECRET_KEY'] = "kgjslkgfj"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

satisfaction = surveys.surveys["satisfaction"]

@app.route('/')
def home_page():
    
    return render_template('home.html', title = satisfaction.title, instructions = satisfaction.instructions)


current_page = 0


@app.route('/start', methods = ["POST", "GET"])
def start():
    if request.method == "POST":
        session["responses"] = []
    return redirect("/question/0")


@app.route('/question/<number>')
def question_page(number):
    
    if int(number) != current_page:
        flash("You are trying to access an invalid question")
        return redirect("/question/" + str(current_page))  

    if int(number) < len(satisfaction.questions):
        current_question = satisfaction.questions[int(number)]   
        return render_template('question.html', question=current_question.question, choices=current_question.choices)
    else:
        return redirect('/thank_you')

@app.route('/answer')
def answer():
    answer = request.args["answer"]
    responses = session["responses"]
    responses.append(answer)
    session["responses"] = responses
    global current_page
    current_page +=1
    return redirect("/question/" + str(current_page))


@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html') 




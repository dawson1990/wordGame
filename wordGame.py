from flask import Flask, render_template, session, request
import random
import time


app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template('welcomepage.html', title='The Word Game', header='The Word Game')


@app.route('/thewordgame', methods=['POST'])
def game_start():
    wordsList = []
    fileInput = []
    sourceWords = []
    with open("words.txt", 'r') as w:
        for line in w:
            fileInput.append(line[:-1])
        for item in fileInput:
            wordsList.append(item.lower())
        for word in wordsList:
            if len(word) >= 7:
                sourceWords.append(word)
        session['startTime'] = time.time()
        print(session['startTime'])
        session['randomword'] = random.choice(sourceWords)
    return render_template('inputboxes.html', title='The Word Game', header=session['randomword'])


@app.route('/results', methods=['POST'])
def process_answer():
    session['endtime'] = round(time.time() - session['startTime'], 2)
    fileInput = []
    userInput = []
    wordsList = []
    answers = []
    invalidWords = []
    with open("words.txt", 'r') as w:
        for line in w:
            if len(line) >= 3:
                fileInput.append(line[:-1])
    for item in fileInput:
        wordsList.append(item.lower())
    for k, v in request.form.items():
        userInput.append(v)
    for item in userInput:
        answers.append(item.lower())
    print(answers)
    if validate_has_empty_answer(answers):
        return render_template('results.html', title='The Word Game',
                               header='Sorry, you did not enter seven answers')
    if duplicate_answers(answers):
        return render_template('results.html', title='The Word Game',
                               header='Sorry, you had duplicate answers')
    for item in answers:
        if validate_character_count(answers):
            return render_template('results.html', title='The Word Game',
                                   header='Sorry, you cannot use same letter multiple times')
        if validate_answer_not_source(answers):
            return render_template('results.html', title='The Word Game',
                                   header='Sorry, you cannot use source word as answer')
        if validate_length_of_words(answers):
            return render_template('results.html', title='The Word Game',
                                   header='Sorry, not all words entered were of valid length')
        else:
            if validate_answer_sourceword(answers):
                for item in answers:
                    if validate_answer_overall(answers, wordsList):
                        return render_template('completePage.html', title='The Word Game', header='Well Done',
                                               time=session['endtime'])
                    else:
                        invalidWords.append(item)
                        return render_template('results.html', title='The Word Game',
                                               header='Hard Luck, one of your answers was not a word',
                                               list=invalidWords)
            else:
                invalidWords.append(item)
                return render_template('results.html', title='The Word Game',
                                       header='Hard Luck, one of your answers was not in the source word',
                                       list=invalidWords)


@app.route('/scoreboard', methods=['POST'])
def process_scoreboard():
    userScore = []
    allScores = []
    userScore.append(session['endtime'])
    for k, v in request.form.items():
        userScore.append(v)
    with open("results.txt", 'a') as w:
        print(userScore, file=w)
    with open("results.txt", 'r') as w:
        for line in w:
            allScores.append(line[:-1])
        allScores.sort()
        counter = 0
        with open("results.txt", 'r') as w:
            for line in w:
                if not line == str(userScore):
                    counter = counter + 1
        position = counter
        return render_template('scoreboard.html', title='The Word Game', header='Scoreboard', list=allScores, position=position)


def duplicate_answers(answers):
    return not len(set(answers)) is 7


def validate_has_empty_answer(answers):
    for item in answers:
        if ' ' in item or " " in item:
            return True
        else:
            return False


def validate_answer_overall(answers, wordsList):
    for item in answers:
        if item in wordsList:
            return True
        else:
            return False


def validate_character_count(answers):
    for item in answers:
        for char in item:
            if item.count(char) > session['randomword'].count(char):
                return True


def validate_answer_sourceword(answers):
    listSource = list(session['randomword'])
    for item in answers:
        word = str(item)
        listWord = list(word)
        for element in listWord:
            if element in listSource:
                return True
            else:
                return False


def validate_answer_not_source(answers):
    source = str(session['randomword'])
    for item in answers:
        word = str(item)
        if word == source:
            return True
        else:
            return False


def validate_length_of_words(answers):
    for item in answers:
        if len(item) <= 2 or len(item) > len(session['randomword']):
            return True
        else:
            return False


if __name__ == '__main__':
    app.config["SECRET_KEY"] = "THISISMYSECRETKEY"
    app.run(debug=True)















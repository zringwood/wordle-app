from flask import Flask, render_template, request
from wtforms import Form, StringField, SubmitField, validators
import json, os
from WordleGuessesGenerator import Puzzle
app = Flask(__name__)

class WordleValidation(Form):
    answer = StringField('Puzzle Answer',[validators.Length(min=5,max=5)])
    button = SubmitField('Submit',[])

@app.route('/', methods = ['GET', 'POST'])
def processinput():
    guesses = None
    form = WordleValidation(request.form)
    if request.method == 'POST' and form.validate():
        text = form.answer.data.lower()
        
        puzzle = Puzzle(text)
        #You only get six guesses for wordle puzzles so this is all fixed. 
        guesses = ["","","","","",""]
        for i in range(6) :
            nxt = f"{puzzle.nextGuess()}"
            if guesses.count(nxt) == 0:
                guesses[i] = nxt
    return render_template('inputpage.html', output=guesses, form=form)

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')

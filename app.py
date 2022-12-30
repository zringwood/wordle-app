from flask import Flask, render_template, request
from WordleGuessesGenerator import Puzzle
app = Flask(__name__)

@app.route('/', methods = ['POST','GET'])
def openpage():
    guesses = None
    if request.method == 'POST':
        text = request.form['puzzleanswer']
        print(text)
        puzzle = Puzzle(text)
        #You only get six guesses for wordle puzzles so this is all fixed. 
        guesses = ["","","","","",""]
        for i in range(6) :
            nxt = f"{puzzle.nextGuess()}"
            if guesses.count(nxt) == 0:
                guesses[i] = nxt
    return render_template('inputpage.html', output=guesses)

app.run()

#This class generates guesses for Wordle puzzles.
import json

#The puzzle class encapsulates one wordle puzzle. 
class Puzzle():
    def __init__(self, answer):
        self.answer = answer
        #Two Dimensional Array containing the probabilities of each letter being in a given position
        #It's an array because it has to be mutable. Indexing can be done with the ord() function
        self.prob = []
        with open("probabilities.txt",'r') as file :
            self.prob = json.load(file)
        self.legalGuesses = []
        with open("legalguesses.txt",'r') as file:
            self.legalGuesses = json.load(file)
    #Helper method for cleanly accessing probabilities
    def getProb(self,char, index):
        return self.prob[ord(char.lower())-ord('a')][index]
    #Defines value of a word by multiplying the probability of every letter
    #Multiplying the values makes it so a 0 probabality is possible
    #The value is raised to the power of the number of unique letters in the word
    def getValue(self,word):
        value = 1
        power = 1
        for i in range(len(word)):
            if word.count(word[i]) == 1:
                power += 1
            value *= self.getProb(word[i], i)
        return pow(value,power)
    #Returns the most likely word based on current probabilites
    def getBestWord(self):
        best = "QQQQQ"
        for word in self.legalGuesses:
            if self.getValue(word) > self.getValue(best) :
                best = word
        return best
    #Takes a word and returns a string of R, Y and G representing red yellow and green
    #Can't handle double letters yet. 
    def guess(self, word):
        result = ""
        for i in range(len(word)):
            if word[i] == self.answer[i]:
                result += "G"
            elif self.answer.count(word[i]) > 0:
                result += "Y"
                
            else:
                result += "R"
        return result
    #Takes a word and a string of R Y and G and adjust the probabilities accordingly. 
    def adjustProb(self, guess, results):
        for i in range(len(guess)):
            if results[i] == 'R':
                #grey
                #different results if the letter is duplicated
                if(guess.count(guess[i]) == 1):
                    self.prob[ord(guess[i].lower())-ord('a')] = [0,0,0,0,0]
                else:
                    self.prob[ord(guess[i].lower())-ord('a')][i] = 0
            elif results[i] == 'Y':
                #yellow
                for j in range(len(self.prob[ord(guess[i].lower())-ord('a')])):
                    self.prob[ord(guess[i].lower())-ord('a')][j] *= 10
                self.prob[ord(guess[i].lower())-ord('a')][i] = 0
            elif results[i] == 'G':
                #green
                save = self.prob[ord(guess[i])-ord('a')][i]
                for array in self.prob :
                    array[i] = 0
                self.prob[ord(guess[i])-ord('a')][i] = save
    #Returns the next guess given the best word and the current answer. 
    def nextGuess(self):
        word = self.getBestWord()
        self.adjustProb(word,self.guess(word))
        return word

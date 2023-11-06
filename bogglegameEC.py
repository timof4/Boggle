"""Implements the logic of the game of boggle."""

from graphics import GraphWin
from boggleboard import BoggleBoard
from boggleletter import BoggleLetter
from brandom import randomize



class BoggleGame:

    __slots__ = [ "_validWords", "_board", "_foundWords", "_selectedLetters", "_score", "_maxScore", "_scoreDict" ]

    def __init__(self, win):
        """
        Create a new Boggle Game and load in our lexicon.
        """
        # set up the set of valid words we can match
        self._validWords = self.__readLexicon()
        

        # init other attributes here.
        self._scoreDict={4:1,5:2,6:3,3:1,7:5}
        self._score=0
        self._maxScore=0
        self._board=BoggleBoard(win)
        self._foundWords=[]
        self._selectedLetters=[]
        self._validWords=[]
        self._validWords=self.__readLexicon()

    def __readLexicon(self, lexiconName='bogwords.txt'):
        """
        A helper method to read the lexicon and return it as a set.
        """
        validWords = set()
        with open(lexiconName) as f:
          for line in f:
            validWords.add(line.strip().upper())

        return validWords
    
    def endWord(self):
        """
        A helper method to reset the board to have no letters selected
        """
        self._selectedLetters=[]
        self._board.setStringToLowerText('')
        self._board.resetColors()

    
    def doOneClick(self, point):
        """
        Implements the logic for processing one click.
        Returns True if play should continue, and False if the game is over.
        """
        # These steps are one way to think about the design, although
        # you are free to do things differently if you prefer.

        # step 1: check for exit button and return False if clicked
        if self._board.inExit(point):
            return False
        # step 2: check for reset button and reset board, found words, score and selected letters
        elif self._board.inReset(point):
            self._board.reset()
            self._selectedLetters=[]; self._score=0; self._foundWords=[]
        # step 3: check if click is on a cell in the grid
        elif self._board.inGrid(point):
            # get BoggleLetter at point
            letter=self._board.getBoggleLetterAtPoint(point)

            # if this is the first letter in a word being constructed,
            # add letter and display it on lower text of board, make letter blue
            if self._selectedLetters==[]:
                self._selectedLetters.append(letter)
                self._board.setStringToLowerText(letter.getLetter())
                letter.setLetterColor(True)

            # else if adding a letter to a non-empty word, make sure it's adjacent, and not already selected,
            # and update state
            elif self._selectedLetters[len(self._selectedLetters)-1].isAdjacent(letter) and letter not in self._selectedLetters:
                #Set previous letters to green, and current to blue
                [let.setLetterColor(False) for let in self._selectedLetters]; letter.setLetterColor(True)

                #Add the letter to list of selected letters and update lower text
                self._selectedLetters.append(letter)
                self._board.setStringToLowerText(''.join([letter.getLetter() for letter in self._selectedLetters]))
            
            # else if clicked on same letter as last time, end word and check for validity
            elif self._selectedLetters[len(self._selectedLetters)-1]==letter:
                currentWord=''.join([letter.getLetter() for letter in self._selectedLetters])
                if currentWord.upper() in self._validWords and currentWord not in self._foundWords:
                    #Add current word to the list and score, display list, and end word
                    self._foundWords.append(currentWord)
                    self._score+=self._scoreDict.get(len(currentWord),11)
                    self._board.setStringToTextArea('\n'.join(self._foundWords))
                self.endWord()
            # else if clicked anywhere else, reset the state to an empty word.
            else:
                self.endWord()
        if self._score>self._maxScore:
            self._maxScore=self._score
        #Display current score and max score
        self._board.setStringToUpperText('Current Score: {}, Max Score: {}'.format(self._score,self._maxScore))
        # return True to indicate we want to keep playing
        return True

if __name__ == '__main__':

    # When you are ready to run on different boards,
    # insert a call to randomize() here.  BUT you will
    # find it much easier to test your code without
    # randomizing things!
    randomize()
    win = GraphWin("Boggle", 400, 400)
    game = BoggleGame(win)
    
    keepGoing = True
    while keepGoing:
        point = win.getMouse()
        keepGoing = game.doOneClick(point)

from tkinter import messagebox
from pathlib import Path
import random
from logzero import logger

from other.json.JsonFile import readJsonFileSchema
from other.firebase.firestore import storageQuestionPortail

from display.quiz.choice1 import displayChoice1
from display.quiz.choice2 import displayChoice2
from display.score import displayScore

paths = Path(__file__).parent.resolve()



class portail:
    """
        Classe qui permet de gérer le déroulement de la partie avec le portail (Portail)
    """

    def __init__(self, master, numberQuestion, token):
        self.numberQuestion = numberQuestion
        self.master = master
        self.token = token
        self.playerScore = 0
        self.errorQuestion = []

        self.readFile = readJsonFileSchema(paths / '../../data/question.json').get()
        if self.readFile == []:
            self.error()

        self.start()
        self.play()


    def start(self):
        logger.info("Play Portail Game")

        self.listeType, self.readQuestion, self.question = [], [], []
        for data in self.readFile:
            if data["type"] == "choice1" or data["type"] == "choice2":
                self.readQuestion.append(data)
                self.listeType.append(data["type"])

        self.randomList = random.sample(range(0, len(self.listeType)), min(self.numberQuestion, len(self.listeType)))
        self.currentQuestionIndex = 0

        for i in range(len(self.randomList)):
            self.question.append(self.readQuestion[self.randomList[i]])
        
        self.randomList = random.sample(range(0, len(self.question)), min(self.numberQuestion, len(self.question)))

        storageQuestionPortail(self.token, self.question, self.randomList, [0] * min(len(self.randomList), 10))
        

    def play(self):
        function = {
            "choice1": self.Choice1,
            "choice2": self.Choice2
        }

        if self.currentQuestionIndex > 0:
            self.playerScore += self.display.get()
            if self.display.get() <= 0:
                self.errorQuestion.append(self.readFile[self.randomList[self.currentQuestionIndex - 1]]["question"])

        if self.currentQuestionIndex < len(self.randomList):
            question_type = self.question[self.randomList[self.currentQuestionIndex]]["type"]
            if question_type in function:
                question_class = function[question_type]
                question_class()
            else:
                self.error()
                
            self.currentQuestionIndex += 1
        else:
            logger.info(f"End quiz, score player: {self.playerScore} ({int((self.playerScore / len(self.randomList)) * 100)} %)")
            displayScore(self.master, int((self.playerScore / len(self.randomList)) * 100), self.errorQuestion)
                    
    
    "------ Fonctions des différentes interfaces du quiz -------------------------------------------------------------------"
    def Choice1(self):
        self.display = displayChoice1(self.master, self.play, 
                                            self.question[self.randomList[self.currentQuestionIndex]]["question"],
                                            self.question[self.randomList[self.currentQuestionIndex]]["choices"],
                                            self.question[self.randomList[self.currentQuestionIndex]]["answer"], 
                                            time=self.question[self.randomList[self.currentQuestionIndex]]["time"],
                                            currentQuestion=self.currentQuestionIndex + 1,
                                            maxQuestion=len(self.randomList),
                                            style=4, token=self.token)
        self.display.grid(row=0, column=0, sticky="nsew")

    def Choice2(self):
        self.display = displayChoice2(self.master, self.play, 
                                            self.question[self.randomList[self.currentQuestionIndex]]["question"],
                                            self.question[self.randomList[self.currentQuestionIndex]]["answer"], 
                                            time=self.question[self.randomList[self.currentQuestionIndex]]["time"],
                                            currentQuestion=self.currentQuestionIndex + 1,
                                            maxQuestion=len(self.randomList),
                                            style=4, token=self.token)
        self.display.grid(row=0, column=0, sticky="nsew")


    def error(self):
        logger.error("Erreur 30")
        self.master.home()
        messagebox.showwarning("Erreur 30", 
                               "Une erreur s'est produite lors de la lecture du fichier de données des questions. Le fichier est peut être mal écrit, contient des erreurs ou est vide.")

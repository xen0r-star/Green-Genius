from tkinter import *
from tkinter import font
from pathlib import Path

from widgets.Image import custom_Image
from widgets.Button import custom_Button
from other.json.JsonFile import addDataJsonFile

paths = Path(__file__).parent.resolve()



class displayScore(Frame):
    """
        Classe de l'écran pour afficher le score final du joueur
    """

    def __init__(self, master, playerScore, errorQuestion = [], user=0, token=""):
        super().__init__(master)
        self.playerScore = playerScore
        self.errorQuestion = errorQuestion[:3]
        self.user, self.token = user, token

        self.config(bg=self.master.color_background)
        self.grid(column=0, row=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=4)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=8)
        self.grid_columnconfigure(0, weight=1)

        self.addComponents()


    def addComponents(self):
        "------ Style de la fenêtre -------------------------------------------------------------------"
        custom_Image(self, image=paths / "../assets/Background.png", 
                     bg=self.master.color_background, 
                     width=700, height=700, 
                     column=0, row=0, rowspan=3)


        "------ Barre de navigation -------------------------------------------------------------------"
        self.navbar = Frame(self)
        self.navbar.grid(column=0, row=0)

        custom_Image(self.navbar, image=paths / "../assets/score/Header_Score.png", 
                     bg=self.master.color_background, 
                     width=571, height=82, 
                     column=0, columnspan=2, row=0)
        
        custom_Button(self.navbar, image=paths / "../assets/Home.png",
                      command=self.master.startGame,
                      bg=self.master.color_second,
                      width=55, height=55,
                      column=1, row=0, sticky=E,
                      padx=(0, 20))
        
        
        self.loopCreate = True

        "------ Affichage du score -------------------------------------------------------------------"
        fontStyle = font.Font(size=55, weight="bold")
        if self.playerScore >= 50:
            custom_Image(self, image=paths / "../assets/score/Frame1.png",
                        text=str(self.playerScore) + " %", font=fontStyle, fg=self.master.color_text,
                        bg=self.master.color_background, 
                        width=240, height=126, 
                        column=0, row=1)
        else:
            custom_Image(self, image=paths / "../assets/score/Frame3.png",
                        text=str(self.playerScore) + " %", font=fontStyle, fg=self.master.color_text,
                        bg=self.master.color_background, 
                        width=240, height=126, 
                        column=0, row=1)
        

        "------ Sauvegarde du score -------------------------------------------------------------------"
        self.speudo = Frame(self, bg=self.master.color_background, width=571, height=10)
        self.speudo.grid(column=0, row=2)

        fontStyle = font.Font(size=27, weight="bold")
        self.entry = Text(self.speudo, bg=self.master.color_fourth, 
                          width=20, height=1, 
                          font=fontStyle, fg=self.master.color_text, insertbackground=self.master.color_text, 
                          highlightthickness=4, highlightbackground="white", highlightcolor="white")
        self.entry.grid(column=0, row=0, ipadx=5)
        self.center_text(None)
        self.entry.bind("<KeyRelease>", self.center_text)

        custom_Button(self.speudo, image=paths / "../assets/score/Valider.png",
                      command=self.saveData,
                      bg=self.master.color_background,
                      width=55, height=55,
                      column=1, row=0, sticky=E,
                      padx=(20, 20))


        "------ Affichage des 3 premières questions incorrectes -------------------------------------------------------"
        self.frame = Frame(self, bg=self.master.color_background, width=571, height=370)
        self.frame.grid(column=0, row=3, sticky=NSEW, padx=64)

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        fontStyle = font.Font(size=15, weight="bold")

        for i in range(len(self.errorQuestion)):
            elementErrorQuestion = Frame(self.frame, bg=self.master.color_second, width=571, height=64, 
                                         highlightthickness=4, highlightbackground="white", highlightcolor="white")
            elementErrorQuestion.grid(row=i, column=0, pady=(0, 10), sticky=EW)

            elementErrorQuestion.grid_columnconfigure(0, weight=1)
            elementErrorQuestion.grid_columnconfigure(1, weight=1)

            custom_Image(elementErrorQuestion, paths / "../assets/score/Error.png", width=50, height=50, bg=self.master.color_second, 
                         row=0, column=0, sticky=W, padx=(10, 5))
            
            if len(self.errorQuestion[i]) > 40:
                label = Label(elementErrorQuestion, text=self.errorQuestion[i][:45] + "...", 
                                font=fontStyle, fg=self.master.color_text, bg=self.master.color_second, justify=RIGHT)
            else:
                label = Label(elementErrorQuestion, text=self.errorQuestion[i], width=38, 
                                font=fontStyle, fg=self.master.color_text, bg=self.master.color_second, justify=RIGHT)
            
            label.grid(row=0, column=1, padx=0, pady=20, sticky="w")
        
        for i in range(len(self.errorQuestion), 3):
            elementErrorQuestion = Frame(self.frame, bg=self.master.color_background, width=571, height=64)
            elementErrorQuestion.grid(row=i, column=0, pady=(0, 10), sticky=EW)


    "Centrer le texte (widget Text)"
    def center_text(self, event): 
        self.entry.tag_configure("center", justify='center')
        self.entry.tag_add("center", "1.0", "end")


    "Sauvegarder les données de l'utilisateur dans le fichier JSON de l'application (Data)"
    def saveData(self):
        addDataJsonFile({
            "name": self.entry.get(1.0, END).replace('\n', ''),
            "score": self.playerScore
        })
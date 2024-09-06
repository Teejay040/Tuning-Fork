import tkinter as tk
from tkinter import messagebox, simpledialog
from threading import Thread
import subprocess
import pi_e_625
import piezo
import program2

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Manipulation and Analysis")
        self.geometry("300x250")


        # Bouton pour lancer le programme 3
        tk.Button(self, text="Start Manipulation", command=self.lancer_programme_3).pack(pady=10)
        
        # Bouton pour lancer le programme 4
        tk.Button(self, text="Start analysis", command=self.lancer_programme_4).pack(pady=10)


    def lancer_programme_3(self):
        # Lancer le script program3.py
        subprocess.Popen(["python", "program3.py"])

    def lancer_programme_4(self):
        # Lancer le script contenant le code du programme 4
        subprocess.Popen(["python", "program4.py"])

if __name__ == '__main__':
    app = Application()
    app.mainloop()

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
        self.title("Contrôle des Dispositifs")
        self.geometry("300x250")

        # Bouton pour mettre la tension à 0V
        tk.Button(self, text="Set to 0V", command=self.mise_a_0v).pack(pady=10)

        # Bouton pour l'initialisation
        tk.Button(self, text="Initialization", command=self.initialisation).pack(pady=10)


    def mise_a_0v(self):
        p = piezo.piezo()
        p.absolute_voltage(0.0)
        messagebox.showinfo("Set to 0V", "The voltage was set to 0V.")

    def initialisation(self):
        datecreate = simpledialog.askstring('Input', 'Enter the date name')
        fichier = simpledialog.askstring('Input', 'Enter the files name')
        
        if datecreate and fichier:
            Thread(target=self.run_program2, args=(datecreate, fichier)).start()
        else:
            messagebox.showwarning("Input Error", "Date name and file name are required!")

    def run_program2(self, datecreate, fichier):
        program2.run_program(datecreate, fichier)



if __name__ == '__main__':
    app = Application()
    app.mainloop()

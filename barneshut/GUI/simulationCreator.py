import tkinter as tk
from tkinter import messagebox
simulationParamsOptions = ["Half Width","Tick Period","Total Duration","Theta","Max Depth"]
simulationParamsData = []


master = tk.Tk()
master.geometry("1000x300")

class Form:
    def __init__(self,fileName,options):
        self.fileName = fileName
        self.options = options
        self.data = []
    
        
    def runForm(self):
        tk.Label(master,text="Simulation Parameters").grid(row=1,column=0)
        for x in range(len(self.options)):
            tk.Label(master,text=self.options[x]).grid(row=2,column=2*x)
            tk.Entry(master).grid(row=2, column=2*x+1)
            self.data.append(tk.Entry(master)) 
            self.data[x].grid(row=2, column=2*x+1)
        tk.Button(master,text='Save', command=self.saveToFile).place(x=10,y=45)
        
    def saveToFile(self):
        file = open(self.fileName,"w")
        for x in range(len(self.options)):
            try:
                intData = int(self.data[x].get().strip())
                file.write(str(intData))
                file.write(",")
            except:
                messagebox.showerror("Error","Incorrect data.")
                file.close()
                break
        file.close()




menu = Form("data.csv",simulationParamsOptions)
menu.runForm()

tk.mainloop()

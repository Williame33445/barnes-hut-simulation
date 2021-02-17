import tkinter as tk

class NumericalForm:
    def __init__(self,options,rowFactor,formName,master):
        self.options = options
        self.rowFactor = rowFactor
        self.formName = formName
        self.entryText = self.emptyStringVarList(len(self.options))
        self.master = master
    
    def get(self, i):
        return float(self.entryText[i].get())
        
    def createForm(self):
        tk.Label(self.master,text=self.formName).grid(row=1+self.rowFactor,column=0)
        for x in range(len(self.options)):
            tk.Label(self.master,text=self.options[x]).grid(row=2+self.rowFactor,column=2*x)
            tk.Entry(self.master,text=self.entryText[x]).grid(row=2+self.rowFactor, column=2*x+1)

    def printHeaders(self):
        line =  ""
        for x in self.options:
            line = line + x + ","
        return line

    def setData(self,data):
        for x in range(len(self.options)):
            self.entryText[x].set(float(data[x]))
        # self.createForm()

    def emptyStringVarList(self,length):
        lst = []
        for x in range(length):
            lst.append(tk.StringVar())
        return lst
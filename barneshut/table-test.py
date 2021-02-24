# Python program to create a table 
   
from tkinter import *

class Table: 
      
    def __init__(self,root):
        
        self.e = []
        self.parameters = ["Mass","PositionX","PositionY","VelocityX","VelocityY"]
        self.rows = 4
        self.columns = len(self.parameters)

        self.createHeader()
        self.createTable()
        
    def createHeader(self):
        for x in range(self.columns):
            label = Label(root,text=self.parameters[x])
            label.grid(row=0,column=x)

    def createTable(self):
        for i in range(self.rows):
            self.e.append([])
            for j in range(self.columns):
                self.e[i].append(Entry(root, width=10, fg='blue', font=('Arial',16,'bold')))
                self.e[i][j].grid(row=i+1, column=j)
                def cellChanged(evt,i=i,j=j): # We have to define this function here to capture the current value of i and j
                    print(evt.widget.get()+','+str(i)+','+str(j))
                self.e[i][j].bind("<FocusOut>",cellChanged)


    def insertLine(self,data,row):
        for x in range(self.columns):
            self.e[row][x].insert(END, data[x])





  

   
# create root window 
root = Tk() 
t = Table(root)
t.insertLine(["1","1","1","1","1"],0)
root.mainloop() 

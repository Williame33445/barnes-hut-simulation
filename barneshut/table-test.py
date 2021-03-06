#need to add python disable entry
   
from tkinter import *
import csv
import math
            
        

class DataPager:
    def __init__(self,allPages,rowsPerPage=5):
        self.pageNumber = 0
        self.rowsPerPage = rowsPerPage 
        self.allPages = allPages
        self.pageData = []

    def refresh(self): 
        pageStart = self.firstRowIndex()
        self.pageData = self.allPages[pageStart:pageStart+self.rowsPerPage]

    def firstRowIndex(self):
        return self.pageNumber*self.rowsPerPage

    def goToPage(self,page):
        self.pageNumber = page
        self.refresh()

    def addBlankData(self,index):
        self.allPages.insert(index + self.firstRowIndex(),["","","","",""])
        self.refresh()

    def deleteIndex(self,index):
        del self.allPages[index + self.firstRowIndex()]
        self.refresh()

    def displayedRowCount(self):
        return len(self.pageData)

        
            

class Table:
    def __init__(self,data,root):
        self.root = root
        
        self.parameters = ["Mass","PositionX","PositionY","VelocityX","VelocityY"]
        self.columns = len(self.parameters)
        
        self.pager = DataPager(data)
        self.e = []

        self.createHeader()
        self.createTable()
        self.createButtons()
        self.refresh()

    def createTable(self):
       self.e = []
       for i in range(self.pager.rowsPerPage):
            self.e.append([])
            for j in range(self.columns):
                self.e[i].append(Entry(self.root, width=10, fg='blue', font=('Arial',16,'bold')))
                self.e[i][j].grid(row=i+1, column=j)
                def cellChanged(evt,i=i,j=j): # We have to define this function here to capture the current value of i and j
                    self.saveDataToMemory(evt,i,j)
                self.e[i][j].bind("<FocusOut>",cellChanged)

    def createHeader(self):
        for x in range(self.columns):
            label = Label(self.root,text=self.parameters[x])
            label.grid(row=0,column=x)

    def createButtons(self):
        def newButton(text,command,row,column):
            b = Button(self.root,text=text,command=command)
            b.grid(row=row,column=column)
            return b
        self.refreshButton = newButton("Refresh",self.refresh,6,1)
        self.previousPageButton = newButton("Previous Page",self.previousPage,6,2)
        self.nextPageButton = newButton("Next Page",self.nextPage,6,3)
        self.addRowButtons = []
        self.deleteRowButtons = []
        for x in range(self.pager.rowsPerPage):
            def addRowToGrid(x=x):
                self.addRow(x)
            def deleteRowFromGrid(x=x):
                self.deleteRow(x)
            self.addRowButtons.append(newButton("+",addRowToGrid,x+1,7))
            self.deleteRowButtons.append(newButton("-",deleteRowFromGrid,x+1,8))
            
    def insertLine(self,rowIndex):
        rowExists = rowIndex < self.pager.displayedRowCount()
        state = "normal" if rowExists else "disabled"
        for c in range(self.columns):
            value = self.pager.pageData[rowIndex][c] if rowExists else ""
            cell = self.e[rowIndex][c]

            cell.config(state="normal")
            cell.delete(0,END)
            cell.insert(0, value)
            cell.config(state=state)


    

    def refresh(self):
        self.pager.refresh()  
        for r in range(self.pager.rowsPerPage):
            self.insertLine(r)

    def saveDataToMemory(self,evt,i,j):
        #need to fix -----------------------------------------
        index = self.pageNumber*5 + i
        self.data[index][j] = evt.widget.get()

    def addRow(self,index):
        self.pager.addBlankData(index)
        self.refresh()

    def deleteRow(self,index):
        self.pager.deleteIndex(index)
        self.refresh()

    def nextPage(self):
        self.pager.pageNumber +=1
        self.refresh()

    def previousPage(self):
        self.pager.pageNumber -=1
        self.refresh()





#create and delete should only come up around enabled entry parts
   
# create root window 
root = Tk() 
t = Table([["1","1","1","1","1"],["2","2","2","2","2"],["2","2","2","2","2"],["2","2","2","2","2"],["2","2","2","2","2"],["2","2","2","2","2"],["2","2","2","2","2"],["2","2","2","2","2"]],root)
root.mainloop() 

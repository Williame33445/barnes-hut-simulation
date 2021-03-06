#need to add python disable entry
   
from tkinter import *
import csv
import math
            
        

class DataPager:
    def __init__(self,allPages,rowsPerPage=5):
        self.pageIndex = 0
        self.rowsPerPage = rowsPerPage 
        self.allPages = allPages
        self.pageData = []

    def refresh(self): 
        pageStart = self.firstRowIndex()
        self.pageData = self.allPages[pageStart:pageStart+self.rowsPerPage]

    def firstRowIndex(self):
        return self.pageIndex*self.rowsPerPage

    def goToPage(self,page):
        self.pageIndex = page
        self.refresh()

    def addBlankData(self,index):
        self.allPages.insert(index + self.firstRowIndex(),["","","","",""])
        self.refresh()

    def deleteIndex(self,index):
        del self.allPages[index + self.firstRowIndex()]
        self.refresh()

    def displayedRowCount(self):
        return len(self.pageData)

    def isLastPage(self):
        return (self.pageIndex+1)*self.rowsPerPage >= len(self.allPages)


        
            

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
                    self.pager.pageData[i][j] = evt.widget.get()
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

    def enabledIf(self,condition):
        return "normal" if condition else "disabled"
            
    def refreshLine(self,rowIndex):
        rowExists = rowIndex < self.pager.displayedRowCount()
        state = self.enabledIf(rowExists)
        for c in range(self.columns):
            value = self.pager.pageData[rowIndex][c] if rowExists else ""
            cell = self.e[rowIndex][c]

            cell.config(state="normal")
            cell.delete(0,END)
            cell.insert(0, value)
            cell.config(state=state)

    def refreshData(self):
        for r in range(self.pager.rowsPerPage):
            self.refreshLine(r)

    def refreshButtons(self):
        previousPageState = self.enabledIf(self.pager.pageIndex > 0)
        self.previousPageButton.config(state=previousPageState)

        nextPageState = self.enabledIf(not self.pager.isLastPage())
        self.nextPageButton.config(state=nextPageState)

        for r in range(self.pager.rowsPerPage):
            addButtonState = self.enabledIf(r <= self.pager.displayedRowCount())
            self.addRowButtons[r].config(state=addButtonState)
            
            deleteButtonState = self.enabledIf(r < self.pager.displayedRowCount())
            self.deleteRowButtons[r].config(state=deleteButtonState)


    def refresh(self):
        self.pager.refresh()  
        self.refreshData()
        self.refreshButtons()

    def addRow(self,index):
        self.pager.addBlankData(index)
        self.refresh()

    def deleteRow(self,index):
        self.pager.deleteIndex(index)
        self.refresh()

    def nextPage(self):
        self.pager.pageIndex +=1
        self.refresh()

    def previousPage(self):
        self.pager.pageIndex -=1
        self.refresh()





#create and delete should only come up around enabled entry parts
   
# create root window 
root = Tk() 
t = Table([["1","1","1","1","1"],["2","2","2","2","2"],["2","2","2","2","2"],["2","2","2","2","2"],["2","2","2","2","2"],["2","2","2","2","2"],["2","2","2","2","2"],["2","2","2","2","2"]],root)
root.mainloop() 

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

    def refresh(self): #refresh
        pageStart = self.firstRowIndex()
        self.pageData = self.allPages[pageStart:pageStart+self.rowsPerPage]

    def storeRow(self,row,changedData): #updateRow
        self.allPages[row+self.firstRowIndex()] = changedData

    def firstRowIndex(self):
        return self.pageNumber*self.rowsPerPage

    def goToPage(self,page):
        self.pageNumber = page
        self.refresh()

    def indexMaxFinder(self): # We shouldn't need this. We should use the length of the pageData array.
        self.refresh()
        if self.pageNumber < math.floor(len(self.allPages)/self.rowsPerPage):
            return self.rowsPerPage
        elif self.pageNumber == math.floor(len(self.allPages)/self.rowsPerPage):
            return (len(self.allPages)%self.rowsPerPage)
        else:
            return 0

    def addBlankData(self,index):
        self.allPages.insert(index + self.firstRowIndex(),["","","","",""])
        self.refresh()

    def deleteIndex(self,index):
        del self.allPages[index + self.firstRowIndex()]
        self.refresh()
        
            

class Table:
    def __init__(self,data,root):
        self.root = root
        
        self.parameters = ["#","Mass","PositionX","PositionY","VelocityX","VelocityY"]
        self.columns = len(self.parameters)
        
        self.pageData = DataPager(data)
        self.e = []

        self.createHeader()
        self.createTable()
        self.createButtons()
        self.refresh()

    def createTable(self):
       self.e = []
       for i in range(self.pageData.rowsPerPage):
            self.e.append([])
            for j in range(self.columns):
                self.e[i].append(Entry(self.root, width=10, fg='blue', font=('Arial',16,'bold')))
                self.e[i][j].grid(row=i+1, column=j)
                self.e[i][j].config(state="disabled")
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
        for x in range(self.pageData.indexMaxFinder()):
            def addRowToGrid(x=x):
                self.addRow(x)
            def deleteRowFromGrid(x=x):
                self.deleteRow(x)
            self.addRowButtons.append(newButton("+",addRowToGrid,x+1,7))
            self.deleteRowButtons.append(newButton("-",deleteRowFromGrid,x+1,8))
            
    def insertLine(self,data,row):
        for x in range(self.columns):
            self.e[row][x].config(state="normal")
            self.e[row][x].delete(0,END)
            self.e[row][x].insert(0, data[x])

    def refresh(self):     
        for x in range(self.pageData.indexMaxFinder()):
            self.insertLine([self.pageData.firstRowIndex()+x] + self.pageData.pageData[x],x)

    def saveDataToMemory(self,evt,i,j):
        #need to fix -----------------------------------------
        index = self.pageNumber*5 + i
        self.data[index][j] = evt.widget.get()

    def addRow(self,index):
        self.pageData.addBlankData(index)
        self.refresh()

    def deleteRow(self,index):
        self.pageData.deleteIndex(index)
        self.refresh()

    def nextPage(self):
        self.pageData.pageNumber +=1
        self.refresh()

    def previousPage(self):
        self.pageData.pageNumber -=1
        self.refresh()





#create and delete should only come up around enabled entry parts
   
# create root window 
root = Tk() 
t = Table([["1","1","1","1","1"],["2","2","2","2","2"],["2","2","2","2","2"],["2","2","2","2","2"],["2","2","2","2","2"],["2","2","2","2","2"],["2","2","2","2","2"],["2","2","2","2","2"]],root)
root.mainloop() 

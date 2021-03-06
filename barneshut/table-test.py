#need to add python disable entry
   
from tkinter import *
import csv
import math

class Data:
    def __init__(self,data):
        self.data = data

    def getRows(self,start,end):
        temp = []
        for x in range(start,end):
            if len(self.data) <= x:
                break
            temp.append([x] + self.data[x])
        return temp
            
        

class DataPager:
    def __init__(self,allPages,rows):
        self.pageNumber = 0
        self.rows = rows #call rowsPerPage
        self.allPages = allPages
        self.pageData = []

    def getPageData(self): #refresh
        pageStart = self.pageNumber*self.rows
        self.pageData = self.allPages.getRows(pageStart,pageStart+self.rows) # [:] list slicing

    def storeRow(self,row,changedData): #updateRow
        self.allPages.data[row+self.pageNumber*self.rows] = changedData

    def goToPage(self,page):
        self.pageNumber = page
        self.getPageData()

    def indexMaxFinder(self): # We shouldn't need this. We should use the length of the pageData array.
        self.getPageData()
        if self.pageNumber < math.floor(len(self.allPages.data)/self.rows):
            return self.rows
        elif self.pageNumber == math.floor(len(self.allPages.data)/self.rows):
            return (len(self.allPages.data)%self.rows)
        else:
            return 0

    def addBlankData(self,index):
        self.allPages.data.insert(index + self.pageNumber*self.rows,["","","","",""])
        self.getPageData()

    def deleteIndex(self,index):
        del self.allPages.data[index + self.pageNumber*self.rows]
        self.getPageData()
        
            

class Table:
    def __init__(self,data,root):
        self.root = root
        
        self.parameters = ["#","Mass","PositionX","PositionY","VelocityX","VelocityY"]
        self.rows = 5
        self.columns = len(self.parameters)
        
        self.pageData = DataPager(Data(data),self.rows)
        self.e = []

        self.createHeader()
        self.createTable()
        self.createButtons()
        self.refreshPage()

    def createTable(self):
       self.e = []
       for i in range(self.rows):
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
        self.refreshButton = newButton("Refresh",self.refreshPage,6,1)
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

    def refreshPage(self):
        self.pageData.getPageData()           
        for x in range(self.pageData.indexMaxFinder()):
            self.insertLine(self.pageData.pageData[x],x)

    def resetPage(self):
        self.refreshPage()

    def saveDataToMemory(self,evt,i,j):
        #need to fix -----------------------------------------
        index = self.pageNumber*5 + i
        self.data[index][j] = evt.widget.get()

    def addRow(self,index):
        self.pageData.addBlankData(index)
        self.resetPage()

    def deleteRow(self,index):
        self.pageData.deleteIndex(index)
        self.resetPage()

    def nextPage(self):
        self.pageData.pageNumber +=1
        self.resetPage()

    def previousPage(self):
        self.pageData.pageNumber -=1
        self.resetPage()





#create and delete should only come up around enabled entry parts
   
# create root window 
root = Tk() 
t = Table([["1","1","1","1","1"],["2","2","2","2","2"],["2","2","2","2","2"],["2","2","2","2","2"],["2","2","2","2","2"],["2","2","2","2","2"],["2","2","2","2","2"],["2","2","2","2","2"]],root)
root.mainloop() 

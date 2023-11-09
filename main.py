#!/usr/bin/env python3

from PyQt5.QtWidgets import QWidget, QApplication,QListWidgetItem, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
import sys, os
import sqlite3




class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        loadUi("main.ui",  self)
        self.calendarWidget.selectionChanged.connect(self.calendarDateChanged)
        self.pushButton_save.clicked.connect(self.saveChanges)
        self.pushButton_add.clicked.connect(self.addBtn)
        self.pushButton_delete.clicked.connect(self.delete_selection)

        self.pushButton_0.clicked.connect(lambda: self.add_numbers(self.pushButton_0.text()))
        self.pushButton_1.clicked.connect(lambda: self.add_numbers(self.pushButton_1.text()))
        self.pushButton_2.clicked.connect(lambda: self.add_numbers(self.pushButton_2.text()))
        self.pushButton_3.clicked.connect(lambda: self.add_numbers(self.pushButton_3.text()))
        self.pushButton_4.clicked.connect(lambda: self.add_numbers(self.pushButton_4.text()))
        self.pushButton_5.clicked.connect(lambda: self.add_numbers(self.pushButton_5.text()))
        self.pushButton_6.clicked.connect(lambda: self.add_numbers(self.pushButton_6.text()))
        self.pushButton_7.clicked.connect(lambda: self.add_numbers(self.pushButton_7.text()))
        self.pushButton_8.clicked.connect(lambda: self.add_numbers(self.pushButton_8.text()))
        self.pushButton_9.clicked.connect(lambda: self.add_numbers(self.pushButton_9.text()))
        self.pushButton_addition.clicked.connect(lambda: self.add_numbers(self.pushButton_addition.text()))
        self.pushButton_subtract.clicked.connect(lambda: self.add_numbers(self.pushButton_subtract.text()))
        self.pushButton_multiply.clicked.connect(lambda: self.add_numbers(self.pushButton_multiply.text()))
        self.pushButton_divide.clicked.connect(lambda: self.add_numbers(self.pushButton_divide.text()))
        self.pushButton_clear.clicked.connect(self.clear_screen)
        self.pushButton_equal.clicked.connect(self.calculate)

        self.pushButton_newEntry.clicked.connect(self.save_journal)
        self.pushButton_journalChanges.clicked.connect(self.updateJournal)

        self.calendarDateChanged()

    #####   Calendar Code   ##### 
    def calendarDateChanged(self):
        dateSelected = self.calendarWidget.selectedDate().toPyDate().strftime("%m-%d-%y")
        self.updateListWidget(dateSelected)
        self.showJournal(dateSelected)

    def updateListWidget(self, date):
        self.listWidget.clear()

        try:
            con = sqlite3.connect('tasks.db')
        except sqlite3.OperationalError:
            os.mkdir('tasks.db')
        finally:
            con = sqlite3.connect('tasks.db')
            con.execute("CREATE TABLE IF NOT EXISTS tasks(task text, completed text, date text)")
        
        cursor = con. cursor()
        query = "SELECT task, completed FROM tasks WHERE date = ?"
        row = (date,)
        results = cursor.execute(query, row).fetchall()
        for result in results:
            item = QListWidgetItem(str(result[0]))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            if(result[1] == "YES"):
                item.setCheckState(Qt.Checked)
            elif(result[1] == "NO"):
                item.setCheckState(Qt.Unchecked)
            self.listWidget.addItem(item)
   
    def saveChanges(self):
        date = self.calendarWidget.selectedDate().toPyDate().strftime("%m-%d-%y")
        con = sqlite3.connect("tasks.db")
        cursor = con. cursor()
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            task = item.text()
            if item.checkState() == Qt.Checked:
                query = "UPDATE tasks SET completed = 'YES' WHERE task = ? AND date= ?"
            else:
                query = "UPDATE tasks SET completed = 'NO' WHERE task = ? AND date= ?"

            row = (task, date, )
            cursor.execute(query, row)
        con.commit()

        messageBox = QMessageBox()
        messageBox.setText("Changes Saved!")
        messageBox.setStandardButtons(QMessageBox.Ok)
        messageBox.exec()

    def addBtn(self):
        newTask = self.lineEdit.text()
        newDate = self.calendarWidget.selectedDate().toPyDate().strftime("%m-%d-%y")

        con = sqlite3.connect("tasks.db")
        cursor = con. cursor()
        query = "INSERT INTO tasks(task,completed,date) values(?,?,?)"
        row = (newTask, 'NO', newDate,)
        cursor.execute(query, row)
        con.commit()
        self.lineEdit.clear()
        self.calendarDateChanged()

    def delete_selection(self):
        try:
            items = self.listWidget.selectedItems()
            for item in items:
                con = sqlite3.connect("tasks.db")
                cursor = con. cursor()
                query = "DELETE FROM tasks WHERE task=?"
                row = (item.text(),)
                cursor.execute(query, row)
                con.commit()
                self.listWidget.takeItem(self.listWidget.row(item))
                
                self.calendarDateChanged()
        except Exception as e:
            print(e)
    #####   End Calendar Code   #####

#########################################################################################################################

    #####   Calculator Code   #####
    
    def add_numbers(self, number):
        currentText = self.label_calculator.text()
        self.label_calculator.setText(f'{currentText}{number}')

    def clear_screen(self):
        self.label_calculator.setText("")

    def calculate(self):
        try:
            ans = eval(self.label_calculator.text())
            text = self.label_calculator.text()
            self.label_calculator.setText(f'{text} = {ans}')
        except Exception as e:
            self.label_calculator.setText(f'ERROR\n{e}')

    #####   End Calculator Code   #####

###########################################################################################################################

    #####   Journal Code   #####

    def showJournal(self, date):
        self.textEdit_journal.setText("")
        try:
            con = sqlite3.connect('journal.db')
        except sqlite3.OperationalError:
            os.mkdir('journal.db')
        finally:
            con = sqlite3.connect('journal.db')
            con.execute("CREATE TABLE IF NOT EXISTS thoughts(entry text, date text)")
        try:
            cursor = con. cursor()
            query = "SELECT entry FROM thoughts WHERE date = ?"
            row = (date,)
            results = cursor.execute(query, row)
            text = results.fetchone()[0]
            
            self.textEdit_journal.setText(text)
        except Exception as e:
            return
        
    def save_journal(self):
        text = self.textEdit_journal.toPlainText()
        date = self.calendarWidget.selectedDate().toPyDate().strftime("%m-%d-%y")
        print(date)
        con = sqlite3.connect('journal.db')
        cursor = con. cursor()
        query = "INSERT INTO thoughts(entry, date) values(?,?)"
        row = (text, date,)
        cursor.execute(query, row)
        con.commit()

        messageBox = QMessageBox()
        messageBox.setText("New Entry Added")
        messageBox.setStandardButtons(QMessageBox.Ok)
        messageBox.exec()

    def updateJournal(self):
        text = self.textEdit_journal.toPlainText()
        date = self.calendarWidget.selectedDate().toPyDate().strftime("%m-%d-%y")

        con = sqlite3.connect('journal.db')
        cursor = con. cursor()
        query = "UPDATE thoughts SET entry = ? WHERE date = ?"
        row = (text, date,)
        cursor.execute(query, row)
        con.commit()

        messageBox = QMessageBox()
        messageBox.setText("Updated Entry")
        messageBox.setStandardButtons(QMessageBox.Ok)
        messageBox.exec()



        

    



    #####   End Journal Code   #####


        
        









if __name__ == "__main__":
    app =QApplication(sys.argv)
    window = Window()   
    window.show()
    sys.exit(app.exec())


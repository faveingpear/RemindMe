
import os
import sys
import json
import logging
import random

from config import json_loader

from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QWidget, QLineEdit, QComboBox, QPushButton, QCheckBox, QApplication, QMessageBox, QScrollArea, QVBoxLayout, QFormLayout, QHBoxLayout, QRadioButton
from PyQt5.QtCore import Qt, QTimer, QProcess
from PyQt5.QtGui import QIcon, QPixmap

# put in config json file
REMINDER_PATH = "Reminders.json"

class ReminderScreen(QMainWindow):

    def __init__(self, parent, reminderClassesList):
        super(ReminderScreen, self).__init__(parent)

        self.initui(reminderClassesList)

    def initui(self, remindersList):

        #self.sortBy = QComboBox(self)
        #self.sortBy.addItem("Birthdays")
        #self.sortBy.addItem("Holidays")

        self.scroll = QScrollArea(self)             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()               # The Vertical Box that contains the Horizontal Boxes of  labels and buttons

        for reminder in remindersList:

            parent = QHBoxLayout() # HBoxLayout that will contain all the elements related to a Reminder Class

            reminder.addSelfToViewAll(parent) # Reminder class adding it's elements to the HBoxLayout

            self.vbox.addLayout(parent)

        self.widget.setLayout(self.vbox)

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

        self.setGeometry(100,100,350,400)

        self.show()

class ReminderEdit(QMainWindow):

    def __init__(self, parent, reminder=None):
        super(ReminderEdit, self).__init__(parent)

        self.reminder = reminder

        self.initui()

    def initui(self):
        self.parent = QWidget(self)

        self.reminderLabel = QLabel("Reminder")
        self.reminderEdit = QLineEdit()

        self.dateLabel = QLabel("Date")
        self.dateEdit = QLineEdit()

        self.catagoryLabel = QLabel("Catagory")
        self.catagoryEdit = QLineEdit()

        self.autoRemoveButton = QRadioButton("Auto remove when date passed")

        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.save)

        self.form = QFormLayout()

        self.form.addRow(self.reminderLabel,self.reminderEdit)
        self.form.addRow(self.dateLabel,self.dateEdit)
        
        self.form.addRow(self.catagoryLabel,self.catagoryEdit)
        self.form.addRow(self.autoRemoveButton)
        self.form.addRow(self.saveButton)

        self.parent.setFixedSize(300,300)
        self.setGeometry(100,100,300,300)
        self.parent.setLayout(self.form)

        if self.reminder !=None:
            self.reminderEdit.setText(self.reminder.getReminder())
            self.dateEdit.setText(self.reminder.getDate())
            self.catagoryEdit.setText(self.reminder.getCatagory())

        self.show()

    def save(self):

        if self.reminder == None:
            file = open(REMINDER_PATH, "r")

            reminderData = json.load(file)

            file.close()

            newdate = self.dateEdit.text().split("/")

            newreminder = {
                "reminder":self.reminderEdit.text(),
                "year":newdate[2],
                "catagory":self.catagoryEdit.text(),
                "day":newdate[0],
                "month":newdate[1],
                "id":random.randint(0,10000)
            }

            reminderData.append(newreminder)

            print(reminderData)

            file = open(REMINDER_PATH,"w")

            json.dump(reminderData,file,ensure_ascii = False, indent=4)

            file.close()

            self.close()
        else:
            file = open(REMINDER_PATH, "r")

            reminderData = json.load(file)

            file.close()

            count = 0
            for reminder in reminderData:
                if reminder["id"] == self.reminder.getid():

                    newdate = self.dateEdit.text().split("/")

                    newreminder = {
                        "reminder":self.reminderEdit.text(),
                        "year":newdate[2],
                        "catagory":self.catagoryEdit.text(),
                        "day":newdate[0],
                        "month":newdate[1],
                        "id":self.reminder.getid()
                    }
                    reminderData[count] = newreminder

                    file = open(REMINDER_PATH,"w")

                    json.dump(reminderData,file,ensure_ascii = False, indent=4)

                    file.close()

                    self.close()
            
                count = count + 1
        


class Reminder():

    def __init__(self,parent,day=0,month=0,year=0,reminder="",catagory="",reminderid=0):
        self.day = day
        self.month = month
        self.year = year
        self.reminder = reminder
        self.catagory = catagory
        self.parent = parent
        self.reminderid = reminderid

    def findDaysUntil(self,currentDay,currentMonth,currentYear):
        pass

    def getReminder(self):
        # May add text wrapping
        return self.reminder

    def getDate(self):
        return self.day + "/" + self.month + "/" + self.year

    def getCatagory(self):
        return self.catagory

    def getid(self):
        return self.reminderid

    def edit(self):
        ReminderEdit(self.parent,self)

    def addSelfToViewAll(self,parent):

        self.dateLabel = QLabel()
        self.dateLabel.setText(self.getDate())
        parent.addWidget(self.dateLabel)

        self.reminderLabel = QLabel()
        self.reminderLabel.setText(self.getReminder())
        self.reminderLabel.setWordWrap(True)
        parent.addWidget(self.reminderLabel)

        self.catagoryLabel = QLabel()
        self.catagoryLabel.setText(self.getCatagory())
        parent.addWidget(self.catagoryLabel)

        self.editButton = QPushButton()
        self.editButton.clicked.connect(self.edit)
        self.editButton.setText("Edit")
        parent.addWidget(self.editButton)

class RemindMe(QMainWindow):

    def __init__(self):
        super(RemindMe, self).__init__()

        self.reminderList = []

        self.WIDTH = 300
        self.HEIGHT = 300

        self.initui()

    def initui(self):

        self.setupConfig()

        self.parent = QWidget(self)
        self.vbox = QVBoxLayout()
        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.reminderBox = QWidget()                 # Widget that contains the collection of Vertical Box
        #self.vbox = QVBoxLayout()               # The Vertical Box that contains the Horizontal Boxes of  labels and buttons=

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.reminderBox)

        self.parent.setFixedSize(self.WIDTH,self.HEIGHT)

        self.dateLabel = QLabel()
        self.dateLabel.setAlignment(Qt.AlignCenter)
        self.dateLabel.setText("05/09/2019")
        self.vbox.addWidget(self.dateLabel)

        self.vbox.addWidget(self.scroll)

        self.reminderLabel = QLabel(self.reminderBox)
        self.reminderLabel.setAlignment(Qt.AlignCenter)
        self.reminderLabel.setWordWrap(True)
        self.reminderLabel.setText(self.reminderList[0].getReminder())

        self.viewAllButton = QPushButton()
        self.viewAllButton.clicked.connect(self.viewAll)
        self.viewAllButton.setText("View All")
        self.vbox.addWidget(self.viewAllButton)

        self.newButton = QPushButton()
        self.newButton.clicked.connect(self.newReminder)
        self.newButton.setText("New")
        self.vbox.addWidget(self.newButton)

        self.parent.setLayout(self.vbox)

        self.setGeometry(0, 0, self.WIDTH, self.HEIGHT)
        self.setWindowTitle('RemindMe')

        self.show()

    def newReminder(self):
        newEdit = ReminderEdit(self)

    def setupConfig(self):

        file = open(REMINDER_PATH, "r")

        reminderData = json.load(file)

        file.close()

        for reminder in reminderData:
            self.reminderList.append(Reminder(self,reminder["day"],reminder["month"],reminder["year"],reminder["reminder"],reminder["catagory"],reminder["id"]))

    def viewAll(self):
        self.viewAllScreen = ReminderScreen(self,self.reminderList)

if __name__ == '__main__':
	
	app = QApplication(sys.argv)
	ex = RemindMe()
	sys.exit(app.exec_())
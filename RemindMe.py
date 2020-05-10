
import os
import sys
import json
import logging

from config import json_loader

from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QWidget, QLineEdit, QComboBox, QPushButton, QCheckBox, QApplication, QMessageBox, QScrollArea, QVBoxLayout, QHBoxLayout
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

class Reminder():

    def __init__(self, day=0,month=0,year=0,reminder="",catagory=""):
        self.day = day
        self.month = month
        self.year = year
        self.reminder = reminder
        self.catagory = catagory

    def findDaysUntil(self,currentDay,currentMonth,currentYear):
        pass

    def getReminder(self):
        # May add text wrapping
        return self.reminder

    def getDate(self):
        return self.day + "/" + self.month + "/" + self.year

    def getCatagory(self):
        return self.catagory

    def edit(self):
        pass

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
        pass

    def setupConfig(self):

        self.reminderConfigOption = [
            "day",
            "month",
            "year",
            "reminder",
            "catagory"
        ]

        file = open(REMINDER_PATH, "r")

        reminderData = json.load(file)

        file.close()

        for reminder in reminderData:
            self.reminderList.append(Reminder(reminder[self.reminderConfigOption[0]],reminder[self.reminderConfigOption[1]],reminder[self.reminderConfigOption[2]],reminder[self.reminderConfigOption[3]],reminder[self.reminderConfigOption[4]]))

        print(self.reminderList[0].getCatagory())
        print(self.reminderList[1].getCatagory())

    def viewAll(self):
        self.viewAllScreen = ReminderScreen(self,self.reminderList)

if __name__ == '__main__':
	
	app = QApplication(sys.argv)
	ex = RemindMe()
	sys.exit(app.exec_())

import os
import sys
import json
import logging

from config import json_loader

from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QWidget, QLineEdit, QComboBox, QPushButton, QCheckBox, QApplication, QMessageBox, QScrollArea, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QProcess
from PyQt5.QtGui import QIcon, QPixmap

# put in config json file
REMINDER_PATH = "Reminders.json"

class ReminderScreen(QMainWindow):

    def __init__(self, parent):
        super(ReminderScreen, self).__init__(parent)

        self.initui()

    def initui(self):

        self.sortBy = QComboBox(self)
        self.sortBy.addItem("Birthdays")
        self.sortBy.addItem("Holidays")

        self.scroll = QScrollArea(self)             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()               # The Vertical Box that contains the Horizontal Boxes of  labels and buttons

        for i in range(1,5):
            object = QLabel("TextLabel")
            self.vbox.addWidget(object)

        self.widget.setLayout(self.vbox)

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

        self.scroll.move(60,30)


        self.setGeometry(100,100,300,400)

        self.show()

class Reminder():

    def __init__(self, day=0,month=0,year=0,reminder="",catagory=""):
        self.day = day
        self.month = month
        self.year = year
        self.reminder = reminder

    def findDaysUntil(self,currentDay,currentMonth,currentYear):
        pass

    def getReminder(self):
        # May add text wrapping
        return self.reminder

    def getDate(self):
        return self.day + "/" + self.month + "/" + self.year

class RemindMe(QMainWindow):

    def __init__(self):
        super(RemindMe, self).__init__()

        self.reminderList = []

        self.initui()

    def initui(self):

        self.setupConfig()

        self.dateLabel = QLabel(self)
        self.dateLabel.setAlignment(Qt.AlignCenter)
        self.dateLabel.setText("05/09/2019")

        self.reminderLabel = QLabel(self)
        self.reminderLabel.setAlignment(Qt.AlignCenter)
        self.reminderLabel.move(0,30)
        self.reminderLabel.setText("This is a reminder")

        self.viewAllButton = QPushButton(self)
        self.viewAllButton.clicked.connect(self.viewAll)
        self.viewAllButton.setText("View All")
        self.viewAllButton.move(0,60)

        self.setGeometry(100,100,100,100)

        self.show()

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

        print(self.reminderList[0].getDate())
        print(self.reminderList[1].getDate())

    def viewAll(self):
        self.viewAllScreen = ReminderScreen(self)

if __name__ == '__main__':
	
	app = QApplication(sys.argv)
	ex = RemindMe()
	sys.exit(app.exec_())
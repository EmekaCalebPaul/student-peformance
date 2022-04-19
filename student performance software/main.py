#!/usr/bin/env python
# coding: utf-8

# In[1]:


from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QRadioButton,
                             QMessageBox, QFileDialog, QGroupBox, QLineEdit, QLabel, QGridLayout, QComboBox, QTextEdit)
from PyQt5 import QtGui
from PyQt5.QtCore import QDir
from PyQt5 import QtCore
import sys
from PyQt5.QtGui import QPixmap
import os
import os.path
import qdarkstyle
import re
import pickle
import numpy as np
import pandas as pd


# In[3]:


#----------Create Gui class

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.left = 500
        self.top = 100
        self.width = 500
        self.height = 400
        
        
        
        self.params = {

            'school': '',
            'Medu': '',
            'failures': '',
            'absences':'',
            'G2':'',
        }
        #Create icons
        self.warning = 'images/warning.png'
        self.icon = 'images/icon.png'
        self.errorMessage = 'This Program supports only files with .txt and .docx extensions'
       

        
        self.initGui()
        
    def initGui(self):
        
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle('Metrics AI')
        self.setWindowIcon(QtGui.QIcon(self.icon))
        self.setMinimumSize(QtCore.QSize(self.width, self.height))
        self.setMaximumSize(QtCore.QSize(self.width, self.height))
        self.setFont(QtGui.QFont('Times new roman', 12))
        
        #self.setPixmap(QPixmap(background_image))
        
        
        self.guiLayout()
    
        self.show()
        
        
        
#-------------------Design Layout

    def guiLayout(self):
        
        gridlayout = QGridLayout()
        gridlayout.addWidget(self.feature1Groupbox(), 0,0)
        gridlayout.addWidget(self.feature2Groupbox(), 1,0)
        gridlayout.addWidget(self.feature3Groupbox(),0,1)
        gridlayout.addWidget(self.feature4Groupbox(), 1,1)
        gridlayout.addWidget(self.feature5GroupBox(), 0,2)
        gridlayout.addWidget(self.feature6GroupBox(), 2,2)
        
        
        self.setLayout(gridlayout)
        
        
#------------Create groupboxes        
     #1.   
    def feature1Groupbox(self):
        
        groupbox_feature1 = QGroupBox('School')
        vbox_first = QVBoxLayout()
        
        #create first radio button for first school
        self.first_school = QRadioButton('GP - Gabriel Pereira')
        self.first_school.school_name = {'school': 'GP'}
        self.first_school.clicked.connect(self.get_school_name)
        
        #create second radio button for second school
        self.second_school = QRadioButton('MS - Mousinho da Silveira')
        self.second_school.school_name = {'school': 'MS'}
        self.second_school.clicked.connect(self.get_school_name)

        
        
        vbox_first.addWidget(self.first_school)
        vbox_first.addWidget(self.second_school)
        groupbox_feature1.setLayout(vbox_first)
        return groupbox_feature1



# feaature 1 function:

    def get_school_name(self):
        
        if self.first_school.isChecked():
            self.params.update(self.first_school.school_name)
        else:
            self.params.update(self.second_school.school_name)


    #2.
    def feature2Groupbox(self):
        
        groupbox_feature2 = QGroupBox(" Mother's education")
        vbox_second = QVBoxLayout()
        
        
        #create summarized_text box
        self.mother_education = QComboBox()
        self.mother_education.addItem("--") #
        self.mother_education.addItem("none") #0
        self.mother_education.addItem("primary education") #1
        self.mother_education.addItem("5th-9th grade") #2
        self.mother_education.addItem("secondary education") #3
        self.mother_education.addItem("higher education") #4
        self.mother_education.activated.connect(self.get_Medu)
        #self.mother_education(QtGui.QFont('Times new roman', 12))
    

        vbox_second.addWidget(self.mother_education)
        groupbox_feature2.setLayout(vbox_second)
        return groupbox_feature2


# feture 2 function:

    def get_Medu(self):

        content1 = self.mother_education.currentText()
        value1 = {'Medu': content1}
        self.params.update(value1)


    #3.
    def feature3Groupbox(self):
        
        groupbox_feature3 = QGroupBox('Failures')
        groupbox_feature3.setFlat(True)
        vbox_third = QVBoxLayout()
    
        # to allow only integer:
        self.onlyIntFailures = QtGui.QIntValidator()

        #create original text label
        self.failures = QLineEdit()
        self.failures.setValidator(self.onlyIntFailures)
        self.failures.setPlaceholderText(u'empty')
        self.failures.textChanged.connect(self.get_failures)
        
        
        vbox_third.addWidget(self.failures)
        groupbox_feature3.setLayout(vbox_third)
        return groupbox_feature3



# feature 3 function:

    def get_failures(self):

        content2 = int(self.failures.text())
        value2 = {'failures': content2}
        self.params.update(value2)

        
    #4.
    def feature4Groupbox(self):
        
        groupbox_feature4 = QGroupBox('Absences')
        groupbox_feature4.setFlat(True)
        vbox_fourth = QVBoxLayout()
        
        # to allow only integer:
        self.onlyIntAbsences = QtGui.QIntValidator()

        #create original text label
        self.absences = QLineEdit()
        self.absences.setValidator(self.onlyIntAbsences)
        self.absences.setPlaceholderText(u'empty')
        self.absences.textChanged.connect(self.get_absences)
         
        
        vbox_fourth.addWidget(self.absences)
        groupbox_feature4.setLayout(vbox_fourth)
        return groupbox_feature4


# feature 4 function:

    def get_absences(self):

        content3 = int(self.absences.text())
        value3 = {'absences': content3}
        self.params.update(value3)

    #5.   
    def feature5GroupBox(self):
        
        groupbox_feature5 = QGroupBox('G2')
        vbox_fifth = QVBoxLayout()
        
        
        #create text_to_summarize_box
        self.G2 = QComboBox()
        self.G2.addItem("--")
        self.G2.addItem("0")
        self.G2.addItem("1")
        self.G2.addItem("2")
        self.G2.addItem("3")
        self.G2.addItem("4")
        self.G2.addItem("5")
        self.G2.addItem("6")
        self.G2.addItem("7")
        self.G2.addItem("8")
        self.G2.addItem("9")
        self.G2.addItem("10")
        self.G2.addItem("11")
        self.G2.addItem("12")
        self.G2.addItem("13")
        self.G2.addItem("14")
        self.G2.addItem("15")
        self.G2.addItem("16")
        self.G2.addItem("17")
        self.G2.addItem("18")
        self.G2.addItem("19")
        self.G2.addItem("20")

        self.G2.activated[str].connect(self.get_G2)

        
        vbox_fifth.addWidget(self.G2)
        groupbox_feature5.setLayout(vbox_fifth)
        return groupbox_feature5



# feature 5 function:

    def get_G2(self):

        content4 = int(self.G2.currentText())
        value4 = {'G2': content4}
        self.params.update(value4)
    
    
    #6.
    
    def feature6GroupBox(self):
        
        groupbox_feature6 = QGroupBox("Predict")
        vbox_sixth = QVBoxLayout()
        
        self.predict_button = QPushButton("Predict Performance")
        self.predict_button.clicked.connect(self.predictFunct)
        

        vbox_sixth.addWidget(self.predict_button)
        groupbox_feature6.setLayout(vbox_sixth)
        return groupbox_feature6
  
    
    
#-----------------Action Methods:
        # create an empty dataframe that gets updated
        # create functions to collect values
        # 



    #Sum   
    def predictFunct(self):

        checker = list(self.params.values())

        if checker[0] == '':

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText('empty field: school ')
            msg.setWindowTitle('Warning window')
            msg.setWindowIcon(QtGui.QIcon(self.warning))
            msg.exec()

        elif checker[1] == '' or checker[1] == '--':

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText('empty field: Medu')
            msg.setWindowTitle('Warning window')
            msg.setWindowIcon(QtGui.QIcon(self.warning))
            msg.exec()

        elif checker[2] == '':

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText('empty field: failures')
            msg.setWindowTitle('Warning window')
            msg.setWindowIcon(QtGui.QIcon(self.warning))
            msg.exec()

        elif checker[3] == '':

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText('empty field: absences')
            msg.setWindowTitle('Warning window')
            msg.setWindowIcon(QtGui.QIcon(self.warning))
            msg.exec()


        elif checker[4] == '' or checker[4] == '--':

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText('empty field: G2')
            msg.setWindowTitle('Warning window')
            msg.setWindowIcon(QtGui.QIcon(self.warning))
            msg.exec()



        else:

           
            # create dataframes for prediction
            data = pd.DataFrame([self.params])

            ## control inputs
            data['failures'] = np.where(data['failures']>4, 4, checker[2])
            data['absences'] = np.where(data['absences']>93, 93, checker[3])
            
            # encode data
            return_num = {"GP": 1, "MS": 0, "none": 0, "primary education": 1, "5th-9th grade": 2, 
                "secondary education": 3, "higher education": 4}
            data.replace(return_num, inplace=True)

            # convert data to numpy array
            data = np.array(data)

            # load model
            filename = 'best_model_dt'
            model = pickle.load(open(filename, 'rb'))
            predict = model.predict(data)
            predicted = predict.tolist()[0]

            # decision:

            if predict == 0:

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)

                msg.setText(

                f"""
                =========
                FEATURES:
                =========

            school:  {self.params.get('school')}
            Medu:     {self.params.get('Medu')}
            failures: {self.params.get('failures')}
            absences: {self.params.get('absences')}
            G2:       {self.params.get('G2')}

                =========
                PREDICTION:
                =========

                Student is likely to FAIL.
                
                """
                )
                msg.setWindowTitle('Prediction')
                msg.setWindowIcon(QtGui.QIcon(self.icon))
                msg.exec()

            else:

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)

                msg.setText(

                f"""
                =========
                FEATURES:
                =========

            school:  {self.params.get('school')}
            Medu:     {self.params.get('Medu')}
            failures: {self.params.get('failures')}
            absences: {self.params.get('absences')}
            G2:       {self.params.get('G2')}

                =========
                PREDICTION:
                =========

                Student is likely to PASS.
                
                """
                )
                msg.setWindowTitle('Prediction')
                msg.setWindowIcon(QtGui.QIcon(self.icon))
                msg.exec()

         
            
#-------------Execute App.                    
        
def main():
    App = QApplication(sys.argv)
    dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
    window = Window()
    App.setStyleSheet(dark_stylesheet)
    sys.exit(App.exec_())
    
if __name__ == '__main__':
    main()


#!/usr/bin/env python
# coding: utf-8

# In[1]:


from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QMessageBox, QFileDialog, QGroupBox, QTextEdit, QLabel, QGridLayout)
from PyQt5 import QtGui
from PyQt5.QtCore import QDir
from PyQt5 import QtCore
import sys
from PyQt5.QtGui import QPixmap
import os
import os.path
import docx
from docx import Document
import gensim
from gensim.summarization.summarizer import summarize
import qdarkstyle

import spacy
import re
from collections import Counter


# In[2]:


#----------Create Gui class

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.left = 500
        self.top = 100
        self.width = 700
        self.height = 500
        
        
        #Create icons
        self.icon = 'images/icon.png'
        self.mozilla = 'images/imagemozilla.png'
        self.errorMessage = 'This Program supports only files with .txt and .docx extensions'
        self.number_of_words = '|> Number of words: '
        self.estreading_time = '|> Est. reading Time: '

        
        self.initGui()
        
    def initGui(self):
        
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle('DonaText')
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
        gridlayout.addWidget(self.originalTextGroupbox(), 0,0)
        gridlayout.addWidget(self.summarizedTextGroupbox(), 1,0)
        gridlayout.addWidget(self.originalTextStatGroupbox(),0,1)
        gridlayout.addWidget(self.summarizedTextStatGroupbox(), 1,1)
        gridlayout.addWidget(self.keyWordsTextBox(), 0,2,2,1)
        
        
        self.setLayout(gridlayout)
        
        
#------------Create groupboxes        
     #1.   
    def originalTextGroupbox(self):
        
        groupbox_original_text = QGroupBox('Original Text')
        vbox_first = QVBoxLayout()
        
        #create upload button
        self.upload_button = QPushButton('Upload File')
        self.upload_button.clicked.connect(self.get_text_file)
        
        #create text_to_summarize_box
        self.text_to_summarize_box = QTextEdit()
        self.text_to_summarize_box.setFont(QtGui.QFont('Times new roman', 12))
        
        #create summarize button
        self.summarize_button = QPushButton('Summarize')
        self.summarize_button.clicked.connect(self.summaryFunct)
        
        
        vbox_first.addWidget(self.upload_button)
        vbox_first.addWidget(self.text_to_summarize_box)
        vbox_first.addWidget(self.summarize_button)
        groupbox_original_text.setLayout(vbox_first)
        return groupbox_original_text
    
    #2.
    def summarizedTextGroupbox(self):
        
        groupbox_summarized_text = QGroupBox('Summarized Text')
        vbox_second = QVBoxLayout()
        
        
        #create summarized_text box
        self.summarized_text_box = QTextEdit()
        self.summarized_text_box.setFont(QtGui.QFont('Times new roman', 12))

        vbox_second.addWidget(self.summarized_text_box)
        groupbox_summarized_text.setLayout(vbox_second)
        return groupbox_summarized_text
    
    #3.
    def originalTextStatGroupbox(self):
        
        groupbox_original_text_stat = QGroupBox('Original Text Stat')
        groupbox_original_text_stat.setFlat(True)
        vbox_third = QVBoxLayout()
    
        
        #create original text label
        
        #----word length label
        self.original_word_len = QLabel(self.number_of_words)
        self.original_word_len.setStyleSheet('color: yellow')
        self.original_word_len.setFont(QtGui.QFont('Times new roman', 12))
        
        #--reading time label
        self.original_reading_time = QLabel(self.estreading_time)
        self.original_reading_time.setStyleSheet('color: yellow')
        self.original_reading_time.setFont(QtGui.QFont('Times new roman', 12))
        
        vbox_third.addWidget(self.original_word_len)
        vbox_third.addWidget(self.original_reading_time)
        groupbox_original_text_stat.setLayout(vbox_third)
        return groupbox_original_text_stat
        
    #4.
    def summarizedTextStatGroupbox(self):
        
        groupbox_summarized_text_stat = QGroupBox('Summarized Text Stat')
        groupbox_summarized_text_stat.setFlat(True)
        vbox_fourth = QVBoxLayout()
        
        self.summarized_word_len = QLabel(self.number_of_words)
        self.summarized_word_len.setStyleSheet('color: yellow')
        self.summarized_word_len.setFont(QtGui.QFont('Times new roman', 12))
        
        self.summarized_reading_time = QLabel(self.estreading_time)
        self.summarized_reading_time.setStyleSheet('color: yellow')
        self.summarized_reading_time.setFont(QtGui.QFont('Times new roman', 12))
        
        vbox_fourth.addWidget(self.summarized_word_len)
        vbox_fourth.addWidget(self.summarized_reading_time)
        groupbox_summarized_text_stat.setLayout(vbox_fourth)
        return groupbox_summarized_text_stat
    
    
    
    #5.   
    def keyWordsTextBox(self):
        
        groupbox_keywords_box = QGroupBox('Keywords')
        vbox_fifth = QVBoxLayout()
        
        
        #create text_to_summarize_box
        self.keywords_text_box = QTextEdit()
        self.keywords_text_box.setFont(QtGui.QFont('Times new roman', 12))

        
        vbox_fifth.addWidget(self.keywords_text_box)
        groupbox_keywords_box.setLayout(vbox_fifth)
        return groupbox_keywords_box
  
    
    
#-----------------Action Methods


    #Upload file
    def get_text_file(self):
        
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setFilter(QDir.Files)
        
        
        if dialog.exec_():
            file_name = dialog.selectedFiles()

            if file_name[0].endswith('.txt'):
                with open(file_name[0], 'r', encoding='utf8') as f:
                    data = f.read()
                    
                    #------Original Text Stat (Make a function)
                    num_of_words = len(data.split())
                    estimatedtime  = num_of_words/200
                    reading_time = '{} mins'.format(round(estimatedtime))
                    
                    self.original_word_len.setText(self.number_of_words + ' ' + str(num_of_words))
                    self.original_reading_time.setText(self.estreading_time + ' ' + str(reading_time))
                    self.text_to_summarize_box.setText(data)
                    f.close()
            
            elif file_name[0].endswith('.docx'):
                with open(file_name[0], 'rb') as f:
                    doc = Document(f)
                    para = [para.text for para in doc.paragraphs if para.text]
                    data = ''.join(para)
                    
                    #-------Original Text Stat (Make a function)
                    num_of_words = len(data.split())
                    estimatedtime  = num_of_words/200
                    reading_time = '{} mins'.format(round(estimatedtime))
                    
                    self.original_word_len.setText(self.number_of_words + ' ' + str(num_of_words))
                    self.original_reading_time.setText(self.estreading_time + ' ' + str(reading_time))
                    self.text_to_summarize_box.setText(data)
                    f.close()
            
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(self.errorMessage)
                msg.setWindowTitle('Unsupported File')
                msg.setWindowIcon(QtGui.QIcon(self.icon))
                msg.exec()
                
            #----Keywords generator
            
            
            nlp = spacy.load('en_core_web_md')
            
            keyword = self.text_to_summarize_box.toPlainText()
            nlp_keyword = nlp(keyword)
            
            text =[]
            for word in nlp_keyword:
                tab = re.findall(r'\t+', word.text)       #my code to filter tabs
                space = re.findall(r'\s+', word.text)     #my code to filter whitespace
        
                if word.text != 'n' and not space and not tab and not word.is_stop and not word.is_punct and not word.like_num :
                    text.append(word.lemma_.lower())

                    
            count = Counter(text).most_common(12)
            most_common = [paired for paired in count]
            common_text = str(most_common)
                
            self.keywords_text_box.setText(common_text)
            

        
    #Sum   
    def summaryFunct(self):
        
        if self.text_to_summarize_box.toPlainText() == '':
            
            #----Error message
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText('You have not uploaded a file')
            msg.setWindowTitle('Empty Field')
            msg.setWindowIcon(QtGui.QIcon(self.icon))
            msg.exec()
            
        else:
            
            #----------Source code
            fetch_text = self.text_to_summarize_box.toPlainText()
            summary_gen = summarize(fetch_text)
            summary_iter = [w.strip('\n') for w in summary_gen]
            final_gen_summary = ''.join(summary_iter)
            self.summarized_text_box.setText(final_gen_summary)
            
            #---Summarized Text Stat
            num_of_words = len(final_gen_summary.split())
            estimatedtime  = num_of_words/200
            reading_time = '{} mins'.format(round(estimatedtime))
                    
            self.summarized_word_len.setText(self.number_of_words + ' ' + str(num_of_words))
            
            if estimatedtime < 1:
                reading_time_seconds = estimatedtime/60
                reading_time_seconds_decimal = '{:.2f} secs'.format(reading_time_seconds)
                self.summarized_reading_time.setText(self.estreading_time + ' ' + str(reading_time_seconds_decimal))
            else:
                self.summarized_reading_time.setText(self.estreading_time + ' ' + str(reading_time))
                    
             
            #-----Summarized Text Pop up
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(final_gen_summary)
            msg.setWindowTitle('Summarized Text')
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


# In[ ]:





# In[ ]:





'''
This module contains several customized widgets used by Ergastirio
'''
import PyQt5.QtWidgets as Qt
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import numpy as np
import os

graphics_dir = os.path.join(os.path.dirname(__file__), '../graphics')

class Table(Qt.QTableWidget):
    ''' Interactive table. It has built-in properties 'data' and 'data_headers', and it updates automatically the content of the tables everytime
        this properties are updated.
    '''
    def __init__(self,  *args):
        self._data = []
        self._data_headers = []
        Qt.QTableWidget.__init__(self, *args)
        #self.verticalHeader().setVisible(False)

    @property
    def data_headers(self):
        return self._data_headers
    @data_headers.setter
    def data_headers(self,h):
        self._data_headers = h
        horHeaders = self._data_headers 
        self.setColumnCount(len(self._data_headers))
        self.setHorizontalHeaderLabels(horHeaders)
        self.resizeColumnsToContents()

    @property
    def data(self):
        return self._data
    @data.setter
    def data(self,d):
        self._data = d
        rows = len(self._data)
        self.setRowCount(rows)
        for m,row in enumerate(self._data):
            for n,item in enumerate(row):
                newitem = Qt.QTableWidgetItem(str(row[n]))
                self.setItem(m, n, newitem)  
        self.data_headers = self._data_headers #We need to call this after data is added
        self.resizeRowsToContents()
        self.scrollToBottom()

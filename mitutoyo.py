# pip install PyQt5
# pip install pyqtgraph
# pip install openpyxl


import time
import serial
from serial.tools import list_ports
from PyQt5 import QtWidgets, uic, QtGui,QtCore
from PyQt5.QtWidgets import  QSizePolicy, QFileDialog, QMessageBox
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  
import os
import numpy  
from mitutoyo import mitutoyo
import serial.tools.list_ports
import configparser
import random


def port_find_unique_dev_by_pidvid(pid: int, vid: int):

     found_devices = list(filter(lambda p: p.pid == pid and p.vid == vid, list_ports.comports()))
     print(found_devices)

     return found_devices[0] if len(found_devices) == 1 else None
 
class mitutoyo(object):
 
    def __init__(self,port=''):
 
        if port == "":
            port = str(port_find_unique_dev_by_pidvid(0x4001,0x0fe7)).split(" ")[0]
            print(port)
 
        self.ser = serial.Serial(port=port,baudrate=115200)
 
 
    def answer(self):
 
        f = self.ser.read().decode() # first character 
        a = ""
        c = ""

        while c != '\r':

            c = self.ser.read().decode()
 
            if c != '\r':

                a = a + c
 
        if f == 9:

            print("Error")

        return a
 
    def measurement(self):

        m = 0
        cmd = "1\r".encode()
        self.ser.write(cmd)
        a = self.answer().split('\r')[0]

        if a.startswith('1A'):
         
           m = float(a.replace('1A',""))
 
        return m
 
 
    def info(self):

        cmd = "V\r".encode()
        self.ser.write(cmd)
        a = self.answer()        
 
        return a


if __name__ == '__main__':      

    um = mitutoyo()
    print(um.info())
 
    while True:

        print(um.measurement())
        time.sleep(.4)

 
MITUTOYO_INI = 'mitutoyo.ini'
MITUTOYO_UI = 'mitutoyo.ui'
MAX_POINTS = 200
 
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs):

        super(MainWindow, self).__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi(MITUTOYO_UI, self)
        self.config = configparser.ConfigParser()
        self.config.read(MITUTOYO_INI)
        self.Unit = "mm"
        self.fname = ""
        q = QtWidgets.QAction("Quit", self)     
        q.triggered.connect(self.closeEvent)
        self.centralwidget.setLayout(self.gridLayout_2)
        self.read_settings()
        self.btnStop.setEnabled(False)
        self.graph_settings()
        self.btnFolder.clicked.connect(self.ChangeDataFolder)
        self.ChangeDataFolder()
        self.timer = QtCore.QBasicTimer()
        self.X = []
        self.Y = []
        self.count = 0
        self.btnStart.clicked.connect(self.start_button_measurement)
        self.btnStop.clicked.connect(self.btnStopclicked)
        self.spiSecondsTimer.valueChanged.connect(self.write_settings)
        self.cmbsource.currentIndexChanged.connect(self.write_settings)
        self.dev = mitutoyo(port='COM4')
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def timerEvent(self,e):

      #  try:
 
                result = self.dev.measurement()
                self.lblLastValue.setText(str(round(result,4)) + " " + str(self.Unit))
                self.Y.append(result)
                self.X.append(self.count * self.spiSecondsTimer.value())
 
                if len(self.Y) > MAX_POINTS:

                    self.Y.pop(0)
                    self.X.pop(0)

                self.graphWidget.plot(self.X, self.Y, clear=True, pen=pg.mkPen('r', width=2))
 
                with open(self.fname,'a') as fi:

                    timestr = time.strftime('%Y-%m-%d %H:%M:%S')
                    fi.write(timestr + ',' + str(result) + ',' + self.Unit + '\n')

                self.count = self.count + 1
 
           # except:

       #     print(sys.exc_info())
 
    def read_settings(self):

        interval = self.find_key("Settings","Interval",1)
        self.spiSecondsTimer.setValue(int(interval))
        usedport = self.find_key("Settings","Comport","com4").lower()
        ports = serial.tools.list_ports.comports()
        i = 0

        for port in ports:

            self.cmbsource.addItem(port.name)

            if usedport == port.name.lower():

                self.cmbsource.setCurrentIndex(i)

            i= i + 1

 
    def write_settings(self):
 
        interval = str(self.spiSecondsTimer.value())
        self.write_key("Settings","Interval",interval)
        port = self.cmbsource.currentText()
        self.write_key("Settings","Comport",port)
        self.graph_settings()

    def find_key(self,section,option,default_val):
 
        if self.config.has_option(section,option):

            val = self.config[section][option]

        else:

            val = default_val
 
        return val
 
 
    def write_key(self,section,option,val):
 
        if not self.config.has_section(section):

            self.config.add_section(section)
 
        self.config.set(section,option,val)
 
        with open(MITUTOYO_INI,"w") as configfile:

            self.config.write(configfile)
 
    def ChangeDataFolder(self):
 
        self.datapath = self.find_key("Data","Path","c:/data")
        newfolder = QFileDialog.getExistingDirectory(self, 'Select directory for data',self.datapath) #,options=QFileDialog.DontUseNativeDialog )
 
        if newfolder:

            self.datapath = newfolder
            self.lblFilename.setText(self.datapath)
            self.write_key("Data","Path",self.datapath)
 
    def btnStopclicked(self):
 
        self.timer.stop()
        self.enableUi()
 
    def enableUi(self):
 
        self.spiSecondsTimer.setEnabled(True)
        self.btnStart.setEnabled(True)
        self.btnStop.setEnabled(False)
        self.cmbsource.setEnabled(True)
        self.txtComment.setEnabled(True)

    def disableUi(self):
 
        self.spiSecondsTimer.setEnabled(False)
        self.btnStart.setEnabled(False)
        self.btnStop.setEnabled(True)
        self.cmbsource.setEnabled(False)
        self.txtComment.setEnabled(False)
 
    def closeEvent(self, event):
 
        self.timer.stop()
        event.accept()

    def start_button_measurement(self):
 
        starttime = time.strftime('%Y%m%d_%H%M%S')
        name = self.datapath + "/Mitutoyo_" + starttime
        self.fname = QFileDialog.getSaveFileName(self,"Save measurement", name,  filter=('CSV file (*.csv)'))[0]

        if self.fname:

            self.datapath,filename = os.path.split(self.fname)
            self.start_measurement()

    def start_measurement(self):
 
        self.lblFilename.setText(self.fname)
        self.graph_settings()
        self.disableUi()
        self.save_header()
        interval = self.spiSecondsTimer.value() * 1000
        self.X = []
        self.Y = []
        self.count = 0
        self.timer.start(interval,self)
 
    def save_header(self):

        with open(self.fname,'w') as fi:

            comment = self.txtComment.toPlainText().replace('\n','\n%% ')
            fi.write("%% " + comment + "\n")
            fi.write("%% Interval (s): " + str(self.spiSecondsTimer.value()) + "\n")
            fi.write("Time,Measurements,Unit\n")
 
    def graph_settings(self):
 
        self.graphWidget.clear()
        self.graphWidget.showButtons()
        self.graphWidget.setBackground((240,240,240))
        pen = pg.mkPen('r', width=20)
        axis_pen = pg.mkPen(color=(0, 0, 0), width=3)
        self.graphWidget.showGrid(x=True, y=True, alpha=0.4)
        font = QtGui.QFont('Arial', 10)
        self.graphWidget.setLabel('bottom','Count * ' + str(self.spiSecondsTimer.value()) + "(s)" ,**{'color': '#FFF', 'font-size': '12pt'})
        self.graphWidget.setLabel('left','Weight (' + self.Unit + ")",**{'color': '#FFF', 'font-size': '12pt'})
        axises = ( 'bottom', 'left' )

        for axis in axises:

            self.graphWidget.showAxis(axis)
            self.graphWidget.getAxis(axis).tickFont = font
            self.graphWidget.getAxis(axis).setTextPen(axis_pen)

        Title = "Mitutoyo"
        self.graphWidget.setTitle(Title,**{'color': '#000', 'font-size': '20pt'})
        self.lblFilename.setText(self.fname)
    
  #  def keyPressEvent(self, event):
   #     """Detecteer een toetsindruk en stop de meting als de Escape-toets wordt ingedrukt."""
    #    if event.key() == QtCore.Qt.Key_Escape:
            
     #       self.btnStopclicked()

    def keyPressEvent(self, event):
        """Detecteer een toetsindruk en stop de meting als de spatiebalk wordt ingedrukt."""
        if event.key() == QtCore.Qt.Key_Space:
            print("Spatiebalk ingedrukt. Stop de kernel.")
            sys.exit()  # Dit stopt de kernel en sluit de applicatie.
            
    #def start_measurement(self):
     #   self.count = 0
      #  self.X = []
       # self.Y = []

        #Start de meting en verzamel de gegevens gedurende 30 seconden
        #start_time = time.time()
       # while time.time() - start_time < 30:  # 30 seconden lang meten
        #    result = self.dev.measurement()
         #   print(result)  # Toon de gemeten waarde
          #  self.Y.append(result)
           # self.X.append(self.count * 1)  # Voeg de tijdstap toe (of pas dit aan)
            #self.count += 1
            #time.sleep(1)  # Voeg een pauze toe van 1 seconde tussen de metingen

        # Na 30 seconden stoppen we de meting en beëindigen de applicatie
#        print("Metingen zijn voltooid!")
 #       sys.exit(      
            
def main():

    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
 
if __name__ == '__main__':      

    main()


# Functie om gegevens naar Excel op te slaan
    def save_to_excel(data, filename='output.xlsx'):
    # Maak een nieuw werkboek en een werkblad
        wb = Workbook()
        sheet = wb.active
        sheet.title = "Meetgegevens"
    
    # Voeg een header toe
        sheet.append(["Tijd", "Metingen", "Eenheid"])  # Aanpassen op basis van je data
    
    # Voeg de gegevens toe
        for item in data:
            sheet.append(item)
    
    # Sla het werkboek op
        wb.save(filename)

# Voorbeeld: gegevens verzamelen

data = []
for i in range(5):  # Simuleer 5 metingen
    tijd = time.strftime('%Y-%m-%d %H:%M:%S')  # Huidige tijd
    meting = round(23.45 + (i * 0.1), 2)  # Voorbeeld van een meting (hier simuleer ik)
    eenheid = "mm"  # Stel een eenheid in
    data.append([tijd, meting, eenheid])
    time.sleep(1)  # Wacht 1 seconde tussen de metingen

# Sla de gegevens op in een Excel-bestand
save_to_excel(data, "meetresultaten.xlsx")

print("Gegevens zijn opgeslagen in meetresultaten.xlsx")




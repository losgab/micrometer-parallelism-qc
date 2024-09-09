# This Python file uses the following encoding: utf-8
import sys
import pandas as pd
import os
from requests import post

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QThread, Signal
from PySide6.QtCore import Qt

URL = "https://script.google.com/macros/s/AKfycbx6wPNqYTieuuD5W6441Im1kWIoejl3Oze2mHHC07Wy18FoQr_Y1vQ4vJ_qXpdOeL0jYw/exec"
data_points_key = "p"
parallelism_value_key = "parallelismValue"

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow
from ExtractData import SerialPortGetter, DataGetter
# from ParallelismChecker import ParallelismChecker
from qr import QRScanner

DATA_FILE = "data.csv"

class MainWindow(QMainWindow):
    get_qr_id = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.showMaximized()

        # Connect click/open on combo box to starting getSerialPortsThread
        # Once done, serve the results from the thread onto the UI

        self.data = {}

        # Initialise serial port refresher thread
        self.serport_getter = self.serport_thread = None
        self.data_getter = self.data_thread = None
        self.qr_scanner = self.qr_scanner_thread = None
        self.init_buttons() # Test & Save buttons
        self.init_qr_scanner()
        self.init_serport_getter()

        self.ui.serialport_select1.addItem("No Device Selected")
        self.portgroup1 = 1
        self.ui.serialport_select1.currentTextChanged.connect(self.serialPort1Selected)
        

        self.parallelism_value = self.identifier = None
        

        # Terminate all threads
        app.aboutToQuit.connect(self.terminate_threads)

        # Thread for receiving data from serial port
        self.portCurrent = None

    def init_buttons(self):
        self.ui.button_test.clicked.connect(self.grade_part)
        self.ui.button_clear.clicked.connect(self.clear)
        self.ui.button_save.clicked.connect(self.save_data)

    # Initialise getting SERIAL PORTS
    def init_serport_getter(self):
        self.serport_getter = SerialPortGetter() # Serial port worker
        self.serport_thread = QThread() # Port Getter Thread

        self.serport_getter.moveToThread(self.serport_thread)

        # Start signal
        self.serport_thread.started.connect(self.serport_getter.getPorts)

        # Termination Signals
        self.serport_getter.finished.connect(self.serport_thread.quit) # When getter is finished, tell thread to quit
        self.serport_getter.finished.connect(self.serport_thread.wait) # When getter is finished, tell thread to quit
        self.serport_thread.finished.connect(self.serport_thread.deleteLater) # When thread is finished, signal thread cleanup
        self.serport_getter.finished.connect(self.serport_getter.deleteLater) # When getter is finished, signal getter cleanup
        self.serport_getter.dataOut.connect(self.serveSerialPorts) # Connect data signal to receiver function
        self.serport_thread.start()

    # Initialising getting DATA FROM SERIAL PORT
    def init_data_getter(self):
        self.data_getter = DataGetter(self.portCurrent, 10) # Serial port worker
        self.data_thread = QThread() # Port Getter Thread

        self.data_getter.moveToThread(self.data_thread)

        # Start signal
        self.data_thread.started.connect(self.data_getter.getData)

        # Process data received signal
        self.data_getter.dataOut.connect(self.display_values)
        # self.data_getter.dataOut.connect(self.parallelism_checker.receive)

        # Termination Signals
        self.data_getter.finished.connect(self.data_thread.quit) # When getter is finished, tell thread to quit
        self.data_getter.finished.connect(self.data_thread.wait) # Wait for thread to finish quitting
        self.data_thread.finished.connect(self.data_thread.deleteLater) # When thread is finished, signal thread cleanup
        self.data_getter.finished.connect(self.data_getter.deleteLater) # When getter is finished, signal getter cleanup
        self.data_thread.start()

    # Initialise QR Scanner
    def init_qr_scanner(self):
        self.qr_scanner = QRScanner()
        self.qr_scanner_thread = QThread()

        self.qr_scanner.moveToThread(self.qr_scanner_thread)

        # Start signal
        # self.qr_scanner_thread.started.connect(self.qr_scanner.scanner_connect)

        # Signals
        self.get_qr_id.connect(self.qr_scanner.read_qr)
        self.qr_scanner.qr_identifier.connect(self.show_identifier)
        self.ui.button_connect_scanner.clicked.connect(self.qr_scanner.find_scanner)

        # Termination Signals
        self.qr_scanner.finished.connect(self.qr_scanner_thread.quit) # When getter is finished, tell thread to quit
        self.qr_scanner.finished.connect(self.qr_scanner_thread.wait) # Wait for thread to finish quitting
        self.qr_scanner_thread.finished.connect(self.qr_scanner_thread.deleteLater) # When thread is finished, signal thread cleanup
        self.qr_scanner.finished.connect(self.qr_scanner.deleteLater) # When getter is finished, signal getter cleanup
        self.qr_scanner_thread.start()

    def grade_part(self):
        self.clear()
        self.ui.button_test.setText("...")
        self.get_qr_id.emit()

        if self.ui.serialport_select1.currentText() == "No Device Selected":
            self.ui.grade_data.setText("No Device")
            self.ui.parallelism_data.setText("No Device")
            self.ui.button_test.setText("TEST PLATFORM")
            return
    
        if not self.data or any([value == None or value == "--.---" for value in self.data.values()]):
            self.ui.grade_data.setText("DATA ERROR")
            self.ui.parallelism_data.setText("DATA ERROR")
            self.ui.button_test.setText("TEST PLATFORM")
            self.parallelism_value = None
            return

        # Calculating parallelism value
        float_data = [float(value) for value in self.data.values()]
        max_min = abs(max(float_data) - min(float_data))
        self.parallelism_value = str(round(max_min, 3))

        self.ui.parallelism_data.setText(self.parallelism_value)

        if (max_min <= 0.03):
            self.ui.grade_data.setText("PASS")
            self.ui.grade_data.setStyleSheet("background: green")
        else:
            self.ui.grade_data.setText("FAIL")
            self.ui.grade_data.setStyleSheet("background: red")
        
        # Highlight points
        max_index = float_data.index(max(float_data))
        min_index = float_data.index(min(float_data))
        self.highlight_points([max_index, min_index])

        # Reset
        self.ui.button_test.setText("TEST PLATFORM")

    def show_identifier(self, qr_code_text):
        self.ui.identifier_data.setText(str(qr_code_text))
        self.identifier = qr_code_text

    def highlight_points(self, points):
        for point in points:
            match int(point):
                case 0:
                    self.ui.data1.setStyleSheet("background: green")
                case 1:
                    self.ui.data2.setStyleSheet("background: green")
                case 2:
                    self.ui.data3.setStyleSheet("background: green")
                case 3:
                    self.ui.data4.setStyleSheet("background: green")
                case 4:
                    self.ui.data5.setStyleSheet("background: green")
                case 5:
                    self.ui.data6.setStyleSheet("background: green")
                case 6:
                    self.ui.data7.setStyleSheet("background: green")
                case 7:
                    self.ui.data8.setStyleSheet("background: green")
                case 8:
                    self.ui.data9.setStyleSheet("background: green")

    def clear(self):
        self.ui.parallelism_data.setText("")
        self.ui.identifier_data.setText("")
        self.ui.grade_data.setText("")
        self.ui.data1.setStyleSheet("")
        self.ui.data2.setStyleSheet("")
        self.ui.data3.setStyleSheet("")
        self.ui.data4.setStyleSheet("")
        self.ui.data5.setStyleSheet("")
        self.ui.data6.setStyleSheet("")
        self.ui.data7.setStyleSheet("")
        self.ui.data8.setStyleSheet("")
        self.ui.data9.setStyleSheet("")
        self.ui.grade_data.setStyleSheet("")

    # SHOW SERIAL PORTS
    def serveSerialPorts(self, data):
        for port in data:
            if self.ui.serialport_select1.findText(str(port.description()), Qt.MatchContains) == -1:
                self.ui.serialport_select1.addItem(f"[{port.portName()}] {port.description()}")
                self.portgroup1 += 1

    # SELECT SERIAL PORT
    def serialPort1Selected(self, portName):
        if portName == "No Device Selected":
            # print("No port selected")
            self.ui.data1.setText("No Data")
            self.ui.data2.setText("No Data")
            self.ui.data3.setText("No Data")
            self.ui.data4.setText("No Data")
            self.ui.data5.setText("No Data")
            self.ui.data6.setText("No Data")
            self.ui.data7.setText("No Data")
            self.ui.data8.setText("No Data")
            self.ui.data9.setText("No Data")

            self.data_getter.finish()
            self.portCurrent = None
            return

        # Get raw port name from selection
        portName = portName.split(' ')[0]
        # print(portName)
        for char in ('[', ']'):
            portName = portName.replace(char, '')

        # Gets the currently selected port

        if self.portCurrent != portName:
            print(f"New Port: {self.portCurrent} -> {portName}")

            if self.portCurrent is not None:
                self.data_getter.finish()

            self.portCurrent = portName
            self.init_data_getter()
            print(f"Thread started for port: {str(self.ui.serialport_select1.currentText())}")

    # Display received values
    def display_values(self, data):
        assert(type(data) is dict)

        self.data = data

        for i in data.keys():
            match int(i):
                case 0: #
                    self.ui.data1.setText(data[i])
                case 1:
                    self.ui.data2.setText(data[i])
                case 2:
                    self.ui.data3.setText(data[i])
                case 3:
                    self.ui.data4.setText(data[i])
                case 4:
                    self.ui.data5.setText(data[i])
                case 5:
                    self.ui.data6.setText(data[i])
                case 6:
                    self.ui.data7.setText(data[i])
                case 7:
                    self.ui.data8.setText(data[i])
                case 8:
                    self.ui.data9.setText(data[i])

    def save_data(self):
        if self.parallelism_value == None:
            self.ui.parallelism_data.setText("No Parallelism Data")
            return

        if self.identifier == None:
            self.ui.identifier_data.setText("No Identifier Data")
            return

        file_exists = os.path.isfile(DATA_FILE)
        if file_exists:
            file = pd.read_csv(DATA_FILE)
            if len(file) != 0:
                last_row = file.tail(1)
                print(last_row)
                last_row_list = last_row.values.tolist()[0]
                index = int(last_row_list[0]) + 1
            else:
                index = 0

            self.get_qr_id.emit() # Get QR ID

            new_row = pd.DataFrame([{'Index': f'{index}', 'ParallelismVal': f'{self.parallelism_value}', 'Grade': f"{'PASS' if float(self.parallelism_value) < 0.03 else 'FAIL'}", 'PlatformID': f'{self.identifier}'}])
            file = pd.concat([file, new_row], ignore_index=True)
            file.to_csv(DATA_FILE, index=False)
        else:
            print("File does not exist")

        post(f'''{URL}?
                {data_points_key}=
                {str(self.data['0'])},
                {str(self.data['1'])},
                {str(self.data['2'])},
                {str(self.data['3'])},
                {str(self.data['4'])},
                {str(self.data['5'])},
                {str(self.data['6'])},
                {str(self.data['7'])},
                {str(self.data['8'])}&
                {parallelism_value_key}=
                {str(self.parallelism_value)}''')

        
    def terminate_threads(self):
        if self.serport_thread.isRunning():
            self.serport_getter.finish()
        if self.data_thread is not None:
            self.data_getter.finish()
        if self.qr_scanner_thread.isRunning(): # Thread for parallelism checker
            self.qr_scanner.finish_all()
        print("Threads Terminated")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()

    sys.exit(app.exec())

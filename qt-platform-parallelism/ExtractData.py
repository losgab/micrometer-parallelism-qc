# This Python file uses the following encoding: utf-8

from PySide6.QtSerialPort import QSerialPortInfo, QSerialPort
from PySide6.QtCore import QObject, Signal, QMutex
from time import sleep

class SerialPortGetter(QObject):

    # Signals
    finished = Signal()
    dataOut = Signal(list)
    running = True

    # Get Serial Ports
    def getPorts(self):
        while self.running:
            ports = QSerialPortInfo.availablePorts()
            self.dataOut.emit(ports)
            sleep(1)

    def finish(self):
        self.running = False
        self.finished.emit()


class DataGetter(QObject):

    # Signals
    running = True
    finished = Signal()

    # Do mapping from IN-USE ports to INDEX
    mux_ports_in_use = [1, 2, 4, 5, 6, 9, 10, 12, 13]

    data = {
        "0": "--.---",
        "1": "--.---",
        "2": "--.---",
        "3": "--.---",
        "4": "--.---",
        "5": "--.---",
        "6": "--.---",
        "7": "--.---",
        "8": "--.---"
    }

    dataOut = Signal(dict)

    mutex = QMutex()


    def __init__(self, portName, waitTimeout, parent=None):
        super().__init__(parent)
        self.portName = portName
        self.waitTimeout = waitTimeout

        # Port stuff
        self.port = QSerialPort()
        self.port.readyRead.connect(self.dataAvailable)

        self.port.setPortName(self.portName)
        self.port.setBaudRate(QSerialPort.Baud115200, QSerialPort.AllDirections)
        self.port.setDataBits(QSerialPort.Data8)
        self.port.setParity(QSerialPort.NoParity)
        self.port.setStopBits(QSerialPort.OneStop)
        
        self.port.clear()
        self.port.open(QSerialPort.ReadWrite)

        if not self.port.isOpen():
            self.port.close()
            print("Failed to open port")
            

    # Main function for getting data from serial port
    def getData(self):
        pass

    def dataAvailable(self):
        while self.port.canReadLine() and self.running:
            serial_data = self.port.readLine().data().decode().strip()

            received_data = str(serial_data).split(' ')

            print(f"Received data: {received_data}")
                
            if not (received_data[0].startswith("[M") and received_data[0].endswith("]:")):
                continue

            # Strip unwanted characters
            for char in ('[', 'M', ']', ':'):
                received_data[0] = received_data[0].replace(char, '')

            # Check if USB ports being used
            index = int(received_data[0])
            if index not in self.mux_ports_in_use:
                continue

            match index:
                case 1:
                    self.data['0'] = received_data[1]
                case 2:
                    self.data['1'] = received_data[1]
                case 4:
                    self.data['2'] = received_data[1]
                case 5:
                    self.data['3'] = received_data[1]
                case 6:
                    self.data['4'] = received_data[1]
                case 9:
                    self.data['5'] = received_data[1]
                case 10:
                    self.data['6'] = received_data[1]
                case 12:
                    self.data['7'] = received_data[1]
                case 13:
                    self.data['8'] = received_data[1]

            self.dataOut.emit(self.data)
            

    def finish(self):
        self.running = False
        self.port.close()
        self.finished.emit()










# This Python file uses the following encoding: utf-8

from PySide6.QtSerialPort import QSerialPortInfo, QSerialPort
from PySide6.QtCore import QObject, Signal, QMutex
from time import sleep
from re import sub

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

            # for port in ports:
            #     print(port.portName())
            #     print(port.description())

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


    def __init__(self, parent=None):
        super().__init__(parent)

        # Port stuff
        self.port = QSerialPort(self)

        # Data Available
        self.port.readyRead.connect(self.dataAvailable)

        self.port.setBaudRate(QSerialPort.Baud115200, QSerialPort.AllDirections)
        # self.port.setFlowControl(QSerialPort.HardwareControl)
        self.port.setDataBits(QSerialPort.Data8)
        self.port.setParity(QSerialPort.NoParity)
        self.port.setStopBits(QSerialPort.OneStop)

        # if not self.port.isOpen():
        #     self.port.close()
        #     print("Failed to open port")
            
    def newSerialPort(self, newPortName):
        if self.port.isOpen():
            self.port.close()
            print("Port closed")

        print(f"New serial port: {newPortName}")
        self.port.setPortName(newPortName)
        self.port.open(QSerialPort.ReadOnly)
        self.port.setDataTerminalReady(False)
        # self.port.setDataTerminalReady(False)

        if not self.port.isOpen():
            print("Failed to open port")

    def dataAvailable(self):
        try:
            incoming_data = self.port.readAll().toStdString().strip()
            # print("ReadyRead!")
            # if self.port.canReadLine():
            #     print("Data available")
            # else:
            #     print("No read line data available")
            #     return
        except:
            print("Error handling data")
            return

        # print(incoming_data)

        # if not (incoming_data[0].startswith("[M") and incoming_data[0].endswith("]:")):
        #     return

        # print(incoming_data.split())

        # index, value = incoming_data.split()
        # if index.startswith("[M") and index.endswith("]:"):
        #     index = int(sub(r'[\[\]:M]', '', index))

        #     # Checking if port in use
        #     if index not in self.mux_ports_in_use:
        #         return

        # print(f"Index: {index}, Value: {value}")

        # match index:
        #     case 1:
        #         self.data['0'] = value
        #     case 2:
        #         self.data['1'] = value
        #     case 4:
        #         self.data['2'] = value
        #     case 5:
        #         self.data['3'] = value
        #     case 6:
        #         self.data['4'] = value
        #     case 9:
        #         self.data['5'] = value
        #     case 10:
        #         self.data['6'] = value
        #     case 12:
        #         self.data['7'] = value
        #     case 13:
        #         self.data['8'] = value
        
        # self.dataOut.emit(self.data)



        index, value = None, None
        for string in incoming_data.split():
            # Micrometer index number
            if string.startswith("[M") and string.endswith("]:"):
                index = int(sub(r'[\[\]:M]', '', string))

                # Checking if port in use
                if index not in self.mux_ports_in_use:
                    continue
            # Micrometer value
            elif string.replace(".", "").isnumeric() or string == "--.---":
                value = string
                # print(type(value))
                print(f"Index: {index}, Value: {string}")

                match index:
                    case 1:
                        self.data['0'] = value
                    case 2:
                        self.data['1'] = value
                    case 4:
                        self.data['2'] = value
                    case 5:
                        self.data['3'] = value
                    case 6:
                        self.data['4'] = value
                    case 9:
                        self.data['5'] = value
                    case 10:
                        self.data['6'] = value
                    case 12:
                        self.data['7'] = value
                    case 13:
                        self.data['8'] = value
                
                self.dataOut.emit(self.data)



        # while self.port.canReadLine() and self.running:
        #     serial_data = self.port.readLine().data().decode().strip()

        #     received_data = str(serial_data).split(' ')

        #     print(f"Received data: {received_data}")
                
        #     if not (received_data[0].startswith("[M") and received_data[0].endswith("]:")):
        #         continue

        #     # Strip unwanted characters
        #     for char in ('[', 'M', ']', ':'):
        #         received_data[0] = received_data[0].replace(char, '')

        #     # Check if USB ports being used
        #     index = int(received_data[0])
        #     if index not in self.mux_ports_in_use:
        #         continue

        #     match index:
        #         case 1:
        #             self.data['0'] = received_data[1]
        #         case 2:
        #             self.data['1'] = received_data[1]
        #         case 4:
        #             self.data['2'] = received_data[1]
        #         case 5:
        #             self.data['3'] = received_data[1]
        #         case 6:
        #             self.data['4'] = received_data[1]
        #         case 9:
        #             self.data['5'] = received_data[1]
        #         case 10:
        #             self.data['6'] = received_data[1]
        #         case 12:
        #             self.data['7'] = received_data[1]
        #         case 13:
        #             self.data['8'] = received_data[1]

        #     self.dataOut.emit(self.data)
            

    def finish(self):
        self.running = False
        self.port.close()
        self.finished.emit()











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
            # for port in result:
            #     print(port.portName())
            # print(result)
            self.dataOut.emit(ports)
            sleep(1)

    def finish(self):
        self.running = False
        self.finished.emit()


class DataGetter(QObject):

    # Signals
    running = True
    finished = Signal()

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
        self.port.open(QSerialPort.ReadWrite)

        if not self.port.isOpen():
            self.port.close()
            print("Failed to open port")
            

    # Main function for getting data from serial port
    def getData(self):
        pass
        # currentPortNameChanged = False
        # self.mutex.lock()
        # # currentPortName = ""
        # # if currentPortName != self.m_portName:
        # #     currentPortName = self.m_portName
        # #     currentPortNameChanged = True
        # # currentWaitTimeout = self.m_waitTimeout
        # # currentRespone = self.m_response
        # self.mutex.unlock()


        # while self.running:
        #     if self.portName == "":
        #         print("Port not set")
        #         self.error.emit(str("Port not set"))
        #         return
        #     elif currentPortNameChanged:
        #         port.close()
        #         port.setPortName(self.m_portName)
        #         if not port.open(QIODevice.ReadWrite):
        #             print(f"Cant open {self.m_portName}, error code {serial.error()} ")
        #             self.error.emit(str("Can't open %1, error code %2"))
        #             return

            # if serial.waitForReadyRead():
            #     # read request
            #     requestData = serial.readAll()
            #     while serial.waitForReadyRead(self.waitTimeout):
            #         requestData += serial.readAll()
            # else:
            #     self.timeout.emit(str("Wait read request timeout %1"))

            # self.mutex.lock()

            # if currentPortName != m_portName:
            #     currentPortName = m_portName
            #     currentPortNameChanged = True
            # else:
            #     currentPortNameChanged = False
            # currentWaitTimeout = m_waitTimeout
            # currentResponse = self.m_response
            # self.mutex.unlock()

    def dataAvailable(self):
        while self.port.canReadLine():
            serial_data = self.port.readLine().data().decode().strip()

            received_data = str(serial_data).split(' ')

            # print(received_data)

            for char in ('M', '[', ']', ':'):
                received_data[0] = received_data[0].replace(char, '')

            if int(received_data[0]) not in self.mux_ports_in_use:
                continue

            index = int(received_data[0])

            match int(index):
                case 1:
                    self.data['0'] = received_data[1]
                    self.dataOut.emit(self.data)
                case 2:
                    self.data['1'] = received_data[1]
                    self.dataOut.emit(self.data)
                case 4:
                    self.data['2'] = received_data[1]
                    self.dataOut.emit(self.data)
                case 5:
                    self.data['3'] = received_data[1]
                    self.dataOut.emit(self.data)
                case 6:
                    self.data['4'] = received_data[1]
                    self.dataOut.emit(self.data)
                case 9:
                    self.data['5'] = received_data[1]
                    self.dataOut.emit(self.data)
                case 10:
                    self.data['6'] = received_data[1]
                    self.dataOut.emit(self.data)
                case 12:
                    self.data['7'] = received_data[1]
                    self.dataOut.emit(self.data)
                case 13:
                    self.data['8'] = received_data[1]
                    self.dataOut.emit(self.data)

    def finish(self):
        self.port.close()
        self.running = False
        self.finished.emit()










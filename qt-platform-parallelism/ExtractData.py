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
            sleep(1)

    def finish(self):
        self.running = False
        self.finished.emit()

class DataGetter(QObject):

    # Signals
    running = True
    finished = Signal()
    new_serial_port_name = Signal(str)

    # Do mapping from IN-USE ports to INDEX
    '''
    Each MUX hub has 8 ports
    Mux 1 -> Ports 0 -> 7
    Mux 2 -> Ports 8 -> 15
    '''
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

    def __init__(self, parent=None):
        super().__init__(parent)

        self.port = QSerialPort(self)
        self.port.readyRead.connect(self.dataAvailable)

        self.port.setBaudRate(QSerialPort.Baud115200, QSerialPort.AllDirections)
        self.port.setDataBits(QSerialPort.Data8)
        self.port.setParity(QSerialPort.NoParity)
        self.port.setStopBits(QSerialPort.OneStop)

    def threadFunction(self):
        while self.running:
            if not self.port.isOpen():
                self.findESP32S3Port()

    # Auto find the right USB Serial port
    def findESP32S3Port(self):
        if self.port.isOpen():
            self.port.close()

        ports = QSerialPortInfo.availablePorts()

        # No available ports to browse
        if len(ports) == 0:
            print("No ports to scan")

            return None

        # Browse ports
        for port in ports:
            # Only accept ports that we want
            if port.description() in ["USB Single Serial", "USB-Enhanced-SERIAL CH343"]:
                print(f"Serial Port Device Manufacturer: '{port.manufacturer()}'")
                print(f"New Serial Port: {port.portName()}")
                self.port.setPortName(port.portName())
                self.port.open(QSerialPort.ReadOnly)

                if not self.port.isOpen():
                    print("Failed to open port")
                    return

                self.new_serial_port_name.emit(port.portName())
                return
            
        print("No ports found")
        self.new_serial_port_name.emit("No Device")

    def newSerialPort(self, newPortName):
        if self.port.isOpen():
            self.port.close()

        print(f"New serial port: {newPortName}")
        self.port.setPortName(newPortName)
        self.port.open(QSerialPort.ReadOnly)

        if not self.port.isOpen():
            print("Failed to open port")

    def dataAvailable(self):
        try:
            incoming_data = self.port.readAll().toStdString().strip()
        except:
            print("Error handling data")
            return

        index = None
        for string in incoming_data.split():
            # Micrometer index number
            if string.startswith("[M") and string.endswith("]:"):
                index = int(sub(r'[\[\]:M]', '', string))
            else:
                # Checking if port in use
                if index not in self.mux_ports_in_use:
                    continue
            
                # Micrometer value
                self.data[str(self.mux_ports_in_use.index(index))] = string
                # print(self.data)
                self.dataOut.emit(self.data)

    def finish(self):
        self.running = False
        self.port.close()
        self.finished.emit()











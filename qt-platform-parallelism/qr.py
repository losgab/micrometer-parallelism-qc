from PySide6.QtSerialPort import QSerialPortInfo, QSerialPort
from PySide6.QtCore import QObject, Signal, QByteArray, QTimer
from time import sleep

# Identification command

scanner_identify_command = QByteArray(bytearray([0x7E, 0x00, 0x07, 0x01, 0x00, 0xE0, 0x01, 0xAB, 0xCD]))
command_mode_command = QByteArray(bytearray([0x7E, 0x00, 0x08, 0x01, 0x00, 0x00, 0x01, 0xAB, 0xCD]))
trigger_command = QByteArray(bytearray([0x7E, 0x00, 0x08, 0x01, 0x00, 0x02, 0x01, 0xAB, 0xCD])) # Page 21
save_setting_command = QByteArray(bytearray([0x7E, 0x00, 0x09, 0x01, 0x00, 0x00, 0x00, 0xDE, 0xC8]))

restore_defaults_command = QByteArray(bytearray([0x7E, 0x00, 0x09, 0x01, 0x00, 0x00, 0xFF, 0xAB, 0xCD]))

class QRScanner(QObject):
    #Signals
    qr_identifier = Signal(str)
    finished = Signal()

    # Get serial port connected to barcode scanner
    qr_port_name = None
    scanner = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.find_scanner()

    def find_scanner(self):
        # Target the right port
        if self.scanner != None:
            self.scanner.close()

        ports = QSerialPortInfo.availablePorts()
        for port in ports:
            print(f"Scanning port: {port.portName()} (Total ports: {len(ports)})")
            temp_port = QSerialPort()
            temp_port.setPortName(port.portName())
            temp_port.setBaudRate(QSerialPort.Baud9600, QSerialPort.AllDirections)
            temp_port.setDataBits(QSerialPort.Data8)
            temp_port.setParity(QSerialPort.NoParity)
            temp_port.setStopBits(QSerialPort.OneStop)
            temp_port.open(QSerialPort.ReadWrite)

            # Check if port has been opened
            if not temp_port.isOpen():
                print("Failed to open port")
                continue

            temp_port.write(scanner_identify_command)

            if temp_port.waitForReadyRead(100):  # Wait for up to 1000 ms
                data = list(temp_port.readAll().data())
                data = [hex(byte) for byte in data]

                if self.is_scanner(data):
                    temp_port.close()
                    print("Scanner Found!")
                    self.qr_port_name = port.portName()
                    self.configure_scanner()
                    return True
            else:
                print("Timeout waiting for data. Not scanner")

            temp_port.close()

        print("Scanner not found")
        return False

    def is_scanner(self, data) -> bool:
        return data == ['0x2', '0x0', '0x0', '0x1', '0x2', '0x13', '0x73']

    def configure_scanner(self):
        self.scanner = QSerialPort()
        self.scanner.setPortName(self.qr_port_name)
        self.scanner.setBaudRate(QSerialPort.Baud9600, QSerialPort.AllDirections)
        self.scanner.setDataBits(QSerialPort.Data8)
        self.scanner.setParity(QSerialPort.NoParity)
        self.scanner.setStopBits(QSerialPort.OneStop)
        self.scanner.open(QSerialPort.ReadWrite)

    # Trigger scan and report back data
    def read_qr(self):
        if self.scanner is None:
            self.find_scanner() # Retry connection # PROTOTYPE

        if self.qr_port_name is None:
            self.qr_identifier.emit("No Scanner Connected")
            return

        self.scanner.write(trigger_command)

        if self.scanner.waitForReadyRead(200):  # Wait for up to 1000 ms
            data = list(self.scanner.readAll().data())
            data = [hex(byte) for byte in data]
            if data != ['0x2', '0x0', '0x0', '0x1', '0x0', '0x33', '0x31']:
                print("Trigger command not confirmed!")
                self.qr_identifier.emit("Scanner ERROR 1")
                return
        else:
            print("Timeout waiting for trigger confirmation, closing port. No scanner connected.")
            self.scanner.close()
            self.scanner = None
            self.qr_port_name = None
            self.qr_identifier.emit("No Scanner Connected") # No response from scanner
            return

        if self.scanner.waitForReadyRead(2000):  # Wait for up to 1000 ms
            data = list(self.scanner.readAll().data())
            data = [hex(byte) for byte in data]
            ascii_string = ''.join([chr(int(h, 16)) for h in data])
            self.qr_identifier.emit(ascii_string)
        else:
            print("Timeout waiting for data. No QR code found")
            self.qr_identifier.emit("No QR code found") # No response from scanner
        
    def finish_all(self):
        if self.scanner is not None:
            self.scanner.close()
        self.finished.emit()



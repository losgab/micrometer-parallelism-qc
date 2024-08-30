from PySide6.QtSerialPort import QSerialPortInfo, QSerialPort
from PySide6.QtCore import QObject, Signal, QByteArray

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
    running = True

    def find_scanner(self):
        # Target the right port
        ports = QSerialPortInfo.availablePorts()
        for port in ports:
            port_name = port.portName()
            print(port_name)
            temp_port = QSerialPort(parent=self)
            temp_port.setPortName(port_name)
            temp_port.setBaudRate(QSerialPort.Baud9600, QSerialPort.AllDirections)
            temp_port.setDataBits(QSerialPort.Data8)
            temp_port.setParity(QSerialPort.NoParity)
            temp_port.setStopBits(QSerialPort.OneStop)
            temp_port.open(QSerialPort.ReadWrite)

            temp_port.write(scanner_identify_command)

            if temp_port.waitForReadyRead(100):  # Wait for up to 1000 ms
                data = list(temp_port.readAll().data())
                data = [hex(byte) for byte in data]

                if self.is_scanner(data):
                    temp_port.close()
                    print("Scanner Found!")
                    self.qr_port_name = port_name
                    self.configure_scanner()
                    return
            else:
                print("Timeout waiting for data")

            temp_port.close()

        print("Scanner not found")

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
    def get_qr_identifier(self):
        if self.scanner is None:
            self.find_scanner() # Retry connection

        if self.qr_port_name is None:
            self.qr_identifier.emit("No Scanner Connected")
            return

        # if self.qr_port_name is None:
        #     self.qr_identifier.emit("No Scanner Connected")
        #     return

        self.scanner.write(trigger_command)

        if self.scanner.waitForReadyRead(200):  # Wait for up to 1000 ms
            data = list(self.scanner.readAll().data())
            data = [hex(byte) for byte in data]
            if data != ['0x2', '0x0', '0x0', '0x1', '0x0', '0x33', '0x31']:
                print("Trigger command not confirmed!")
                self.qr_identifier.emit("Scanner ERROR 1")
                return
        else:
            print("Timeout waiting for trigger confirmation, Closing port")
            self.scanner.close()
            self.scanner = None
            self.qr_port_name = None
            self.qr_identifier.emit("No Scanner Connected") # No response from scanner
            return

        if self.scanner.waitForReadyRead(5000):  # Wait for up to 1000 ms
            data = list(self.scanner.readAll().data())
            data = [hex(byte) for byte in data]
            ascii_string = ''.join([chr(int(h, 16)) for h in data])
            # print(f"QR Code Found: {ascii_string}")        
            self.qr_identifier.emit(ascii_string)
        else:
            print("Timeout waiting for data. No QR code found")
            self.qr_identifier.emit("No QR code found") # No response from scanner
            return
        
    def finish(self):
        if self.scanner is not None:
            self.scanner.close()
        self.running = False
        self.finished.emit()



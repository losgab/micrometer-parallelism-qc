from PySide6.QtSerialPort import QSerialPortInfo, QSerialPort
from PySide6.QtCore import QObject, Signal, QMutex, QByteArray

# Identification command

scanner_identify_command = QByteArray(bytearray([0x7E, 0x00, 0x07, 0x01, 0x00, 0xE0, 0x01, 0xAB, 0xCD]))
command_mode_command = QByteArray(bytearray([0x7E, 0x00, 0x08, 0x01, 0x00, 0x00, 0x01, 0xAB, 0xCD]))
trigger_command = QByteArray(bytearray([0x7E, 0x00, 0x08, 0x01, 0x00, 0x02, 0x01, 0xAB, 0xCD])) # Page 21
save_setting_command = QByteArray(bytearray([0x7E, 0x00, 0x09, 0x01, 0x00, 0x00, 0x00, 0xDE, 0xC8]))

restore_defaults_command = QByteArray(bytearray([0x7E, 0x00, 0x09, 0x01, 0x00, 0x00, 0xFF, 0xAB, 0xCD]))

class QR(QObject):
    #Signals
    qr_identifier = Signal(str)

    # Get serial port connected to barcode scanner
    qr_port_name = None
    scanner = None

    def __init__(self, parent=None):
        super().__init__(parent)

        # Target the right port
        ports = QSerialPortInfo.availablePorts()
        for port in ports:
            port_name = port.portName()

            temp_port = QSerialPort()
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

        # self.scanner.write(trigger_command)

        # if self.scanner.waitForReadyRead(100):  # Wait for up to 1000 ms
        #     data = list(self.scanner.readAll().data())
        #     data = [hex(byte) for byte in data]
        #     # Restore default acknowledge
        #     assert(data == ['0x2', '0x0', '0x0', '0x1', '0x0', '0x33', '0x31'])
        #     print("Trigger")
        # else:
        #     print("Timeout waiting for data, Closing port")
        #     self.scanner.close()

        # if self.scanner.waitForReadyRead(1000):  # Wait for up to 1000 ms
        #     data = list(self.scanner.readAll().data())
        #     data = [hex(byte) for byte in data]

        #     ascii_string = ''.join([chr(int(h, 16)) for h in data])

        #     # print(f"READ! {ascii_string}")
        # else:
        #     print("Timeout waiting for data, Closing port")
        #     self.scanner.close()


    # Trigger scan and report back data
    def get_qr_identifier(self):
        if self.scanner is None:
            self.qr_identifier.emit("No Scanner Connected")

        self.scanner.write(trigger_command)

        ascii_string = "No QR code found"

        if self.scanner.waitForReadyRead(100):  # Wait for up to 1000 ms
            data = list(self.scanner.readAll().data())
            data = [hex(byte) for byte in data]
            # Restore default acknowledge
            assert(data == ['0x2', '0x0', '0x0', '0x1', '0x0', '0x33', '0x31'])
        else:
            print("Timeout waiting for data, Closing port")

        if self.scanner.waitForReadyRead(5000):  # Wait for up to 1000 ms
            data = list(self.scanner.readAll().data())
            data = [hex(byte) for byte in data]

            ascii_string = ''.join([chr(int(h, 16)) for h in data])
            print(f"QR Code Found: {ascii_string}")        

            # print(f"READ! {ascii_string}")
        else:
            print("Timeout waiting for data, Closing port")

        self.qr_identifier.emit(ascii_string)


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

    def find_scanner(self) -> str: # CONNECTED TO CONNECT SCANNER BUTTON
        # Target the right port
        if self.scanner != None:
            self.scanner.close()

        ports = QSerialPortInfo.availablePorts()

        # No available ports to browse
        if len(ports) == 0:
            print("No ports to scan")
            self.qr_identifier.emit("No Scanner Connected")
            return None

        # Browse ports
        for port in ports:
            # Skip ports that we are sure are not the scanner
            if port.description() not in ["USB Serial Device", "USB Single Serial", "USBKey Module"]:
                print(f"Skipped port: {port.portName()} - {port.description()}")
                continue

            print(f"Scanning port: {port.portName()} - {port.description()} (Total ports: {len(ports)})")
            temp_port = QSerialPort()
            temp_port.setPortName(port.portName())
            temp_port.setBaudRate(QSerialPort.Baud9600, QSerialPort.AllDirections)
            temp_port.setDataBits(QSerialPort.Data8)
            temp_port.setParity(QSerialPort.NoParity)
            temp_port.setStopBits(QSerialPort.OneStop)
            temp_port.open(QSerialPort.ReadWrite)

            # Check if port has been opened
            if not temp_port.isOpen():
                print(f"Failed to open port: Error {temp_port.error()}")
                temp_port.close()
                continue

            # Send command to identify scanner once opened
            temp_port.write(scanner_identify_command)

            # Wait and read response
            data = []
            if temp_port.waitForReadyRead(100):  # Wait for up to 1000 ms
                data = list(temp_port.readAll().data())
                data = [hex(byte) for byte in data]
            else:
                print("Timeout waiting for data.")
            
            temp_port.close()

            # Check response for scanner
            if self.is_scanner(data):
                print("Scanner Found!")
                return port.portName()

        # No scanners found
        return None

    def is_scanner(self, data: list) -> bool:
        return data == ['0x2', '0x0', '0x0', '0x1', '0x2', '0x13', '0x73']
    
    def connect_scanner(self) -> bool:
        # Find scanner if not connected
        if self.qr_port_name is None:
            self.qr_port_name = self.find_scanner()

            # No scanner found
            if self.qr_port_name is None:
                self.qr_identifier.emit("No Scanner Connected")
                return False
            
            # Scanner found, open a new connection to it
            self.scanner = QSerialPort()
            self.scanner.setPortName(self.qr_port_name)
            self.scanner.setBaudRate(QSerialPort.Baud9600, QSerialPort.AllDirections)
            self.scanner.setDataBits(QSerialPort.Data8)
            self.scanner.setParity(QSerialPort.NoParity)
            self.scanner.setStopBits(QSerialPort.OneStop)
            self.scanner.open(QSerialPort.ReadWrite)

            return True

        else: # Scanner already connected, get a scan
            self.read_qr()
            return True

    # Trigger scan and report back data
    def read_qr(self) -> bool: # CONNECTED TO SIGNAL get_qr_id
        if self.qr_port_name is None:
            connected = self.connect_scanner()

            if not connected:
                self.qr_identifier.emit("Scanner Not Connected")
                return False

        # Verify scanner before doing anything
        if not self.trigger_scanner():
            print("Scanner Not Triggered. Attempting to reconnect...")

            # Attempt to reconnect
            connected = self.connect_scanner()

            if not connected:
                self.qr_identifier.emit("Scanner Not Connected")
                return False

            print("Scanner Reconnected")
            self.trigger_scanner()

        # Scan and read back data
        if self.scanner.waitForReadyRead(2000):  # Wait for up to 1000 ms
            data = list(self.scanner.readAll().data())
            data = [hex(byte) for byte in data]

            # Send data on signal
            ascii_string = ''.join([chr(int(h, 16)) for h in data])
            self.qr_identifier.emit(ascii_string)

            return True
        else:
            print("Timeout waiting for data. No QR code found")
            self.qr_identifier.emit("No QR code found") # No response from scanner

            return False
        
    def finish_all(self):
        if self.scanner is not None:
            self.scanner.close()
        self.finished.emit()

    def trigger_scanner(self) -> bool:
        if self.scanner is None or self.qr_port_name is None:
            return False

        # Send trigger command and wait for confirm response
        self.scanner.write(trigger_command)
        
        data = []
        if self.scanner.waitForReadyRead(200):  # Wait for up to 1000 ms
            data = list(self.scanner.readAll().data())
            data = [hex(byte) for byte in data]
        else:
            print("No trigger confirm, closing port. No scanner connected.")
            self.scanner.close()
            self.scanner = self.qr_port_name = None
            self.qr_identifier.emit("No Scanner Connected") # No response from scanner
            return False
        
        # Check if trigger command was confirmed
        success = self.is_trigger_confirm(data)
        print("Scan trigger confirm" if success else "Trigger confirm failed.")
        
        return success

    def is_trigger_confirm(self, ret_data: list) -> bool:
        return ret_data == ['0x2', '0x0', '0x0', '0x1', '0x0', '0x33', '0x31']

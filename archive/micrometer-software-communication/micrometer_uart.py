from serial import Serial, PARITY_NONE, STOPBITS_TWO, EIGHTBITS, to_bytes
import serial.tools.list_ports as ls
from time import sleep

available_ports = [p.device for p in ls.comports()]

s = Serial(
    "COM3",
    38400,
    timeout=None,
    parity=PARITY_NONE,
    stopbits=STOPBITS_TWO,
    bytesize=EIGHTBITS,
)

# Query Command
query = [0x01, 0x03, 0x00, 0x00, 0x00, 0x02, 0xC4, 0x0B]

num_bytes_written = s.write(to_bytes(query))

print("---------------------------")
# print(f"Available Ports: {available_ports}")
print(f"Bytes Written: {num_bytes_written}")
print("---------------------------")

sleep(0.2)

ret = s.read(9)

sign = "-" if ret[3] else "+"
data = ret[5:7]

decoded_data = int.from_bytes(data, "big") / 1000

print(f"Raw Return: {ret}")
print(f"Decoded Data: {sign}{round(decoded_data, 3)}")
# print(type(res))

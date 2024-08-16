# platform-parallelism
Asiga build platform QC machine, testing parallelism and height spec.

Raspberry Pi 4
PW: 2024

If window is closed, program can be run with measure-buildplatform in Terminal.

# Electronics
### Controller (PN07665)
Used to select micrometer to retrieve data, forwards through to USB serial. Based on ESP32-S3 Waveshare Pico MCU development board. Magnet LED is driven through switching MOSFET. Code written in ESP-IDF framework, developed on PlatformIO. Uses threads for getting data from MUX boards and forwards data on respective UART lines. Note: MCU board and PCB GND are not connected. Tie together externally during assembly. Retrieves data in millimeters, to 3 decimal places.

- Schematic -> micrometer_parallelism/Controller
- PCB design -> micrometer_parallelism/PCB_Controller

### Components
|            Ref            |                                                  Part                                                   |                   Note                   |
| :-----------------------: | :-----------------------------------------------------------------------------------------------------: | :--------------------------------------: |
|            J1             | [ESP32-S3 Waveshare Pico](https://www.waveshare.com/wiki/ESP32-S3_Waveshare_Pico_MCU_Development_Board) |                   MCU                    |
|          LED1-16          |                         [COM-16347](https://www.digikey.com.au/short/n90nzttf)                          |         WS2812B Addressable LED          |
|           C1-16           |                                Generic 0603 16V 0.1uF ceramic capacitor                                 |          Decoupling capacitors           |
|            Q2             |                        [BSS84AK,215](https://www.digikey.com.au/short/h07v5d89)                         |         MOSFET for switching LED         |
|            R3             |                                     Generic 0603 4.7K Ohm Resistor                                      |         MOSFET Pull-up resistor          |
|          R4, R5           |                                      Generic 0603 120 Ohm Resistor                                      |    MOSFET gate resistor, LED resistor    |
|           LED17           |                                       Generic 20mA Green 0603 LED                                       |               5V power LED               |
| MAG_LED_SWITCH, POWER_SUP |                       [S4B-PH-SM4-TB](https://www.digikey.com.au/short/mfrmz3ch)                        | 4-pin JST-SPH right angle SMD receptacle |
|   MUX_UART1 & MUX_UART2   |                       [S6B-PH-SM4-TB](https://www.digikey.com.au/short/5wcvq9v4)                        | 6-pin JST-SPH right angle SMD receptacle |


### GPIO pin assignments
|    GPIO    |                 Detail                 |      IO Type       |
| :--------: | :------------------------------------: | :----------------: |
|   17, 16   |              UART 1 TX/RX              |    OUTPUT/INPUT    |
|   36, 35   |              UART 2 TX/RX              |    OUTPUT/INPUT    |
| 13, 14, 15 | SELECT lines for MUX board 1 (A, B, C) |       OUTPUT       |
| 18, 33, 34 | SELECT lines for MUX board 2 (A, B, C) |       OUTPUT       |
|     11     |        Electromagnet button pin        | INPUT (ACTIVE LOW) |
|     12     |         Electromagnet LED pin          |       OUTPUT       |
|   37, 38   |      Electromagnet control (F, R)      |       OUTPUT       |
|   10, 9    |        LED strip data in (1, 2)        |       OUTPUT       |
___
### MUX board (PN07646)


| GPIO | Detail                                 | IO Type      |



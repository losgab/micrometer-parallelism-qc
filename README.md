# Parallelism & Part Tolerance Quality Check

- Developed and programmed a microcontroller PLC system for automated part quality checking (component face parallelism & nominal profile tolerance)
- Involved interfacing with multiple commercial micrometers via RS232 protocol
- Implemented colour-based grading system computed from comparing measurements against acceptance criteria
- Developed Arduino based version for prototyping, ESP32-S3 based version for finalising
- Designed PLC control board using EasyEDA

### Version 1
- Custom built electronics platforms for logging results on local SD card storage via SPI
- Involved asynchronous measurement gathering through 4 Software Serial channels

### Version 2
- Designed custom PCB with EasyEDA
- Simplified measurement gathering by multiplexing 4 RS232 measurement channels through CD4052BE IC
- ESP32-S3 MCU based
- Fully implemented SD card logging
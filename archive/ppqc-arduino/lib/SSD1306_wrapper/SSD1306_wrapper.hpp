#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
/*
    Wrapper Library for OLED Display SSD1306 for Arduino (OOP)

    Convenience library for printing, clearing & replacing lines easily.

    Written by Gabriel Thien 2023
*/


#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
#define OLED_RESET -1 // Reset pin # (or -1 if sharing Arduino reset pin)

void displaySetup();
void printNewMessage(String);
void printMessage(String);
void replaceCurrentLine(String);
void clearDisplay();
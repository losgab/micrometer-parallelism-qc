#include "SSD1306_wrapper.hpp"

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void displaySetup()
{
    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C))
    {
        Serial.println(F("SSD1306 allocation failed"));
        for (;;)
            ; // Don't proceed, loop forever
    }

    display.display();
    delay(1000); // Pause for 2 seconds

    // Clear the buffer
    display.clearDisplay();

    display.setTextSize(1);
    display.setTextColor(WHITE);
    display.setCursor(0, 0);
    display.display();
}

void printNewMessage(String msg)
{
    display.clearDisplay();
    display.setCursor(0, 0);
    display.print(msg);
    display.display();
}

void printMessage(String msg)
{
    display.print(msg);
    display.display();
}

void replaceCurrentLine(String msg)
{
    int16_t current_y = display.getCursorY();
    for (uint8_t y = current_y; y <= current_y + 7; y++)
    {
        for (uint8_t x = 0; x < 127; x++)
        {
            display.drawPixel(x, y, BLACK);
        }
    }
    display.setCursor(0, current_y);
    display.print(msg);
    display.display();
}

void clearDisplay()
{
    display.clearDisplay();
    display.setCursor(0, 0);
}
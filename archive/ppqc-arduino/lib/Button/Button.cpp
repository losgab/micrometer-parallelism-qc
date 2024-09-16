#include "Button.hpp"

Button::Button(uint8_t pin, uint8_t is_input_pullup, uint8_t is_analog_input)
{
    init(pin, is_input_pullup, is_analog_input);
}

Button::Button(uint8_t pin, uint8_t is_input_pullup)
{
    init(pin, is_input_pullup, false);
}

void Button::init(uint8_t pin, uint8_t is_input_pullup, uint8_t is_analog_input)
{
    _pin = pin;
    last_state = 0;
    pushed = 0;
    pressed = 0;
    is_analog = is_analog_input;

    pinMode(pin, (is_input_pullup) ? INPUT_PULLUP : INPUT);
}

void Button::update_button()
{
    if (is_analog)
    {
        uint16_t reading = analogRead(_pin);
        pushed = (last_state == 0 && reading < 100) ? 1 : 0;
        pressed = last_state = (reading < 100) ? 1 : 0;
    }
    else
    {
        uint8_t reading = !digitalRead(_pin);
        pushed = (last_state == 0 && reading == HIGH) ? 1 : 0;
        pressed = last_state = reading;
    }
}

uint8_t Button::was_pushed()
{
    return pushed;
}

uint8_t Button::is_pressed()
{
    return pressed;
}

uint8_t Button::wait_for_push()
{
    while (1)
    {
        update_button();
        delay(UPDATE_DELAY);
        if (pushed)
        {
            return 1;
        }
    }
}
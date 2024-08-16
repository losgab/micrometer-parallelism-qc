#ifndef MUX_THREAD_H
#define MUX_THREAD_H

#include <freertos/FreeRTOS.h>
#include <driver/uart.h>
#include <driver/gpio.h>
#include "easy_led_strip.h"

typedef struct dial_mux_params
{
    uint8_t mux_id;
    uart_port_t port;
    gpio_num_t tx_pin;
    gpio_num_t rx_pin;
    gpio_num_t sel0;
    gpio_num_t sel1;
    gpio_num_t sel2;
    QueueHandle_t queue_handle;
    led_strip_handle_t strip_handle;
} dial_mux_params_t;

typedef struct data_mesage
{
    uint8_t dial_ind; // micrometer number
    bool flag;        // true for negative, false for positive
    float data;       // micrometer data
} data_message_t;

void dial_mux_main(void *pvParameter);

#endif
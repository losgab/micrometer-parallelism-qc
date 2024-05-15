/**
 * Library for interfacing with micrometers
 * 
 * @author Gabriel Thien @ Zydex (Asiga 3D Printers)
*/
#pragma once

#include <esp_err.h>
#include <driver/uart.h>

typedef struct micrometer_data {
    bool flag; // True -> +ve, False -> -ve
    float data;
    bool valid; // Within spec
} micrometer_data_t;

esp_err_t init_micrometers(uart_port_t port, micrometer_data_t *micrometer);

esp_err_t update_micrometers(micrometer_data_t *micrometer);
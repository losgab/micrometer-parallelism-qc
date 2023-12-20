#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <freertos/queue.h>
#include <freertos/timers.h>
#include <driver/uart.h>
#include <driver/gpio.h>

#define SYS_DELAY(x) vTaskDelay(pdMS_TO_TICKS(x))

// UART Stuff
#define UART_PORT_NUM UART_NUM_2
#define TX_PIN 39
#define RX_PIN 40
#define BUFFER_SIZE 4096

#define QUERY_FREQ 2000

// GPIO Stuff For UART Select

// Micrometer Query Command
const uint8_t query[] = {0x01, 0x03, 0x00, 0x00, 0x00, 0x02, 0xC4, 0x0B}; // Micrometer Specific Query Instruction
uint8_t response[9];

// Prototype Simplified UART Library Functions
void uart_init()
{
    uart_config_t uart_config = {
        .baud_rate = 38400,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_2,
        .flow_ctrl = UART_HW_FLOWCTRL_CTS_RTS,
        .rx_flow_ctrl_thresh = 122,
    };
    // ESP_ERROR_CHECK(uart_set_baudrate(UART_PORT_NUM, 38400));
    // ESP_ERROR_CHECK(uart_set_word_length(UART_PORT_NUM, UART_DATA_8_BITS));
    // ESP_ERROR_CHECK(uart_set_parity(UART_PORT_NUM, UART_PARITY_DISABLE));
    // ESP_ERROR_CHECK(uart_set_stop_bits(UART_PORT_NUM, UART_STOP_BITS_1));
    // ESP_ERROR_CHECK(uart_set_line_inverse(UART_PORT_NUM, UART_SIGNAL_INV_DISABLE));
    // ESP_ERROR_CHECK(uart_set_hw_flow_ctrl(UART_PORT_NUM, UART_HW_FLOWCTRL_CTS_RTS, 122));
    // ESP_ERROR_CHECK(uart_set_mode(UART_PORT_NUM, UART_MODE_UART));
    ESP_ERROR_CHECK(uart_param_config(UART_PORT_NUM, &uart_config));
    uart_set_pin(UART_PORT_NUM, TX_PIN, RX_PIN, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
    ESP_ERROR_CHECK(uart_set_line_inverse(UART_PORT_NUM, UART_SIGNAL_RXD_INV | UART_SIGNAL_TXD_INV));
    uart_driver_install(UART_PORT_NUM, BUFFER_SIZE * 2, 0, 0, NULL, 0);
}

static void uart_send_bytes(const uint8_t *data, uint16_t len)
{
    uart_write_bytes(UART_PORT_NUM, data, len);
    uart_wait_tx_done(UART_PORT_NUM, pdMS_TO_TICKS(100));
}

size_t uart_rx_available()
{
    size_t len;
    uart_get_buffered_data_len(UART_PORT_NUM, &len);
    // printf("Buffer Length: %d\n", len);
    return len;
}

void send_query()
{
    uart_send_bytes(query, sizeof(query));
    printf("Queried!\n");
}

void app_main(void)
{
    uart_init();

    SYS_DELAY(2000);

    // TimerHandle_t timer = xTimerCreate("MyTimer",                 // Timer name
    //                                    pdMS_TO_TICKS(QUERY_FREQ), // Timer period in milliseconds (e.g., 1000 ms for 1 second)
    //                                    pdTRUE,                    // Auto-reload the timer
    //                                    NULL,                      // Timer parameters
    //                                    send_query);               // Timer callback function

    // xTimerStart(timer, 0);

    // uint16_t baudrate = 0;
    while (1)
    {
        // uart_get_baudrate(UART_PORT_NUM, &baudrate);
        // printf("Baudrate: %d\n", baudrate);
        SYS_DELAY(2000);
        send_query();
        printf("---------------\n");
        SYS_DELAY(50);
        if (uart_rx_available() > 0)
        {
            uart_read_bytes(UART_PORT_NUM, response, sizeof(response), pdMS_TO_TICKS(50));
            for (uint8_t i = 0; i < sizeof(response); i++)
            {
                printf("[BYTE] (%d): %d\n", i, response[i]);
            }
            printf("---------------\n");
            // SYS_DELAY(2000);
            // printf("Response Query Sent!\n");
            // send_query();
            // printf("---------------\n");
            //     // uint8_t flag = response[3];
            //     // // float data = ((~response[5] << 8) | ~response[6]);
            //     // // printf("Flag: %d\n", flag);
            //     // // printf("Data: %f\n", data);
            //     uart_flush(UART_PORT_NUM);úúúúúúúúúúú
        }
        // Resetting
        for (uint8_t i = 0; i < 9; i++)
        {
            response[i] = 0;
        }
        uart_flush(UART_PORT_NUM);
    }
}
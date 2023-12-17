#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <freertos/queue.h>
#include <driver/uart.h>
#include <driver/gpio.h>

#define SYS_DELAY(x) vTaskDelay(pdMS_TO_TICKS(x))

// UART Stuff
#define UART_PORT_NUM UART_NUM_1
#define TX_PIN 16
#define RX_PIN 17
#define BUFFER_SIZE 2048

// GPIO Stuff For UART Select

// Micrometer Query Command
uint8_t query[] = {0x01, 0x03, 0x00, 0x00, 0x00, 0x02, 0xC4, 0x0B}; // Micrometer Specific Query Instruction

// Configure UART parameters
uart_config_t uart_config = {
    .baud_rate = 38400,
    .data_bits = UART_DATA_8_BITS,
    .parity = UART_PARITY_DISABLE,
    .stop_bits = UART_STOP_BITS_2,
    .flow_ctrl = UART_HW_FLOWCTRL_CTS_RTS,
    .rx_flow_ctrl_thresh = 122,
};
QueueHandle_t uart_queue;

// Prototype Simplified UART Library Functions
static void uart_init()
{
    ESP_ERROR_CHECK(uart_param_config(UART_PORT_NUM, &uart_config));
    uart_set_pin(UART_PORT_NUM, TX_PIN, RX_PIN, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
    uart_driver_install(UART_PORT_NUM, BUFFER_SIZE, BUFFER_SIZE, 10, &uart_queue, 0);
}

static void uart_send_bytes(const uint8_t *data)
{
    uart_write_bytes(UART_PORT_NUM, (const char *)data, sizeof(data));
    uart_wait_tx_done(UART_PORT_NUM, 100);
}

uint16_t uart_rx_available()
{
    uint16_t length = 0;
    uart_get_tx_buffer_free_size(UART_PORT_NUM, (size_t *)(&length));
    return length;
}

void app_main(void)
{
    uart_init();

    SYS_DELAY(2000);

    while (1)
    {
        printf("Bruh!\n");
        // uart_send_bytes((const uint8_t *)&query);
        // SYS_DELAY(300);
        // if (uart_rx_available() > 0)
        // {
        //     printf("RX Buffer Not Empty!!!\n");
        // }
        // else
        // {
        //     printf("RX Buffer Empty!!!\n");
        // }
    }
}
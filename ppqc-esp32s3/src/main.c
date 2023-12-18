#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <freertos/queue.h>
#include <driver/uart.h>
#include <driver/gpio.h>

#define SYS_DELAY(x) vTaskDelay(pdMS_TO_TICKS(x))

// UART Stuff
#define UART_PORT_NUM UART_NUM_2
#define TX_PIN 39
#define RX_PIN 40
#define BUFFER_SIZE 256

// GPIO Stuff For UART Select

// Micrometer Query Command
const uint8_t query[] = {0x01, 0x03, 0x00, 0x00, 0x00, 0x02, 0xC4, 0x0B}; // Micrometer Specific Query Instruction
uint8_t response[9];
QueueHandle_t uart_queue;

// Prototype Simplified UART Library Functions
void uart_init()
{
    ESP_ERROR_CHECK(uart_set_baudrate(UART_PORT_NUM, 38400));
    ESP_ERROR_CHECK(uart_set_word_length(UART_PORT_NUM, UART_DATA_8_BITS));
    ESP_ERROR_CHECK(uart_set_parity(UART_PORT_NUM, UART_PARITY_DISABLE));
    ESP_ERROR_CHECK(uart_set_stop_bits(UART_PORT_NUM, UART_STOP_BITS_1));
    ESP_ERROR_CHECK(uart_set_line_inverse(UART_PORT_NUM, UART_SIGNAL_RXD_INV));
    ESP_ERROR_CHECK(uart_set_hw_flow_ctrl(UART_PORT_NUM, UART_HW_FLOWCTRL_CTS_RTS, 122));
    // ESP_ERROR_CHECK(uart_set_mode(UART_PORT_NUM, UART_MODE_UART));
    // ESP_ERROR_CHECK(uart_param_config(UART_NUM_2, &uart_config));
    uart_set_pin(UART_PORT_NUM, TX_PIN, RX_PIN, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
    uart_driver_install(UART_PORT_NUM, BUFFER_SIZE, 0, 50, &uart_queue, 0);
}

static void uart_send_bytes(const uint8_t *data)
{

    uart_write_bytes(UART_PORT_NUM, data, sizeof(data));
    uart_wait_tx_done(UART_PORT_NUM, pdMS_TO_TICKS(100));
}

size_t uart_rx_available()
{
    size_t length = 0;
    uart_get_buffered_data_len(UART_PORT_NUM, &length);
    printf("Buffer Length: %d\n", length);
    return length;
}

void app_main(void)
{
    uart_init();

    SYS_DELAY(2000);

    while (1)
    {
        // printf("%d\n", sizeof(query));
        uart_send_bytes(query);
        SYS_DELAY(200);
        if (uart_rx_available() > 0)
        {
            // response[3] = 0;
            printf("RX Buffer Not Empty!!!\n");
            uart_read_bytes(UART_PORT_NUM, response, 9, pdMS_TO_TICKS(50));
            
            for (uint8_t i = 0; i < 9; i++)
            {
                printf("%d: %d\n", i, ~response[i]);
            }
            
            // uint8_t flag = response[3];
            // // float data = ((~response[5] << 8) | ~response[6]);
            // // printf("Flag: %d\n", flag);
            // // printf("Data: %f\n", data);
            uart_flush(UART_PORT_NUM);
        }
    }
}
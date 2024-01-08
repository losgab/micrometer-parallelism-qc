#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <freertos/queue.h>
#include <freertos/timers.h>
#include <driver/uart.h>
#include <driver/gpio.h>

#include <Button.h>

#define SYS_DELAY(x) vTaskDelay(pdMS_TO_TICKS(x))

// UART Stuff
#define UART_PORT_NUM UART_NUM_2
#define TX_PIN GPIO_NUM_5
#define RX_PIN GPIO_NUM_6
#define BUFFER_SIZE 4096

// Micrometer Query Command
#define QUERY_FREQ 2000
const uint8_t query[] = {0x01, 0x03, 0x00, 0x00, 0x00, 0x02, 0xC4, 0x0B}; // Micrometer Specific Query Instruction
uint8_t response[9];

// GPIO Stuff For UART Channel select through CD4052BE IC
#define SELECT_A GPIO_NUM_3
#define SELECT_B GPIO_NUM_4
#define SELECT_PIN_BITMASK ((1ULL << SELECT_A) | (1ULL << SELECT_B))
gpio_config_t gpio_select_config = {
    .pin_bit_mask = SELECT_PIN_BITMASK,
    .mode = GPIO_MODE_OUTPUT,
    .pull_up_en = GPIO_PULLUP_ENABLE,
    .pull_down_en = GPIO_PULLDOWN_DISABLE,
    .intr_type = GPIO_INTR_DISABLE};
uint8_t current_channel = 0;

// Button Stuff
#define PROGRAM_SWITCH_PIN GPIO_NUM_1
#define ENABLE_SWITCH_PIN GPIO_NUM_44
button_t program_button;
button_t enable_button;
uint8_t enable_switch_state = 0;

// Prototype UART Library Functions
void uart_init()
{
    uart_config_t uart_config = {
        .baud_rate = 38400,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_2,
        .flow_ctrl = UART_HW_FLOWCTRL_CTS_RTS,
        .rx_flow_ctrl_thresh = 122,
        .source_clk = UART_SCLK_APB};
    ESP_ERROR_CHECK(uart_param_config(UART_PORT_NUM, &uart_config));
    uart_set_pin(UART_PORT_NUM, TX_PIN, RX_PIN, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
    ESP_ERROR_CHECK(uart_set_line_inverse(UART_PORT_NUM, UART_SIGNAL_RXD_INV | UART_SIGNAL_TXD_INV));
    uart_driver_install(UART_PORT_NUM, BUFFER_SIZE * 2, 0, 0, NULL, 0);
}

void uart_send_bytes(const uint8_t *data, uint16_t len)
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
    // printf("---------------\n");
    // printf("Queried!\n");
    // printf("---------------\n");
}

void app_main(void)
{
    // Initialise UART & GPIO
    uart_init();
    ESP_ERROR_CHECK(gpio_config(&gpio_select_config));

    // Button Config
    program_button = create_button(PROGRAM_SWITCH_PIN, true);
    enable_button = create_button(ENABLE_SWITCH_PIN, true);

    gpio_set_level(SELECT_A, 1);
    gpio_set_level(SELECT_B, 0);

    // TimerHandle_t timer = xTimerCreate("MyTimer",                 // Timer name
    //                                    pdMS_TO_TICKS(QUERY_FREQ), // Timer period in milliseconds (e.g., 1000 ms for 1 second)
    //                                    pdTRUE,                    // Auto-reload the timer
    //                                    NULL,                      // Timer parameters
    //                                    send_query);               // Timer callback function

    // xTimerStart(timer, 0);

    // uint16_t counter = 0;
    gpio_set_level(SELECT_A, 0);
    gpio_set_level(SELECT_B, 0);
    current_channel = 0;
    while (1)
    {
        update_button(program_button);
        update_button(enable_button);
        SYS_DELAY(1000);

        if (was_pushed(program_button))
        {
            if (current_channel)
            {
                gpio_set_level(SELECT_A, 0);
                gpio_set_level(SELECT_B, 0);
                current_channel = 0;
            }
            else
            {
                gpio_set_level(SELECT_A, 1);
                gpio_set_level(SELECT_B, 0);
                current_channel = 1;
            }
            SYS_DELAY(5);
            // printf("Channel switched to %d\n", current_channel);
        }

        if (was_pushed(enable_button))
        {
            printf("Enable Button Pushed!\n");
            enable_switch_state = !enable_switch_state;
        }

        send_query();
        SYS_DELAY(50);

        if (uart_rx_available() > 0)
        {
            // counter++;
            uart_read_bytes(UART_PORT_NUM, response, sizeof(response), pdMS_TO_TICKS(50));
            // for (uint8_t i = 0; i < sizeof(response); i++)
            //     printf("[BYTE] (%d): %d\n", i, response[i]);
            // printf("[COUNTER]: %d\n", counter);
            // printf("---------------\n");
            uint8_t flag = response[3];
            float data = ((response[5] << 8) | response[6]);
            data = data / 1000;
            if (enable_switch_state)
            {
                printf("[%d] [RESULT]: %c%.3f\n", current_channel, flag ? (uint8_t)('-') : (uint8_t)('+'), data);
            }
        }
        // Resetting
        for (uint8_t i = 0; i < 9; i++)
            response[i] = 0;
        uart_flush(UART_PORT_NUM);
    }
}
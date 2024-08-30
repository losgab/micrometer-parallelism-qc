#include "mux_thread.h"
#include <esp_log.h>

#define BUFFER_SIZE 512
#define UART_TAG "UART"

#define RESPONSE_TIMEOUT 50

#define DELAY 500

// Micrometer Query Command
const uint8_t query[] = {0x01, 0x03, 0x00, 0x00, 0x00, 0x02, 0xC4, 0x0B}; // Micrometer Specific Query Instruction

// Dummy Data
const float dummy_data[] = {1.509, 1.517, 1.666, 1.540, 1.575, 1.629, 1.684, 1.661, 1.614};

bool dummy = false;

esp_err_t uart_init(uart_port_t port, gpio_num_t tx_pin, gpio_num_t rx_pin, uart_config_t *uart_config)
{
    return ESP_OK;
}

void uart_send_bytes(uart_port_t port, const uint8_t *data, uint16_t len)
{
    int ret = uart_write_bytes(port, data, len);
    if (ret == -1)
    {
        printf("UART Write Error\n");
    }
    esp_err_t err = uart_wait_tx_done(port, pdMS_TO_TICKS(RESPONSE_TIMEOUT));
    if (err == ESP_ERR_TIMEOUT)
    {
        ESP_LOGE(UART_TAG, "Wait TX Timeout");
    }
}

size_t uart_rx_available(uart_port_t port)
{
    size_t len = 0;
    uart_get_buffered_data_len(port, &len);
    return len;
}

void dial_mux_main(void *pvParameter)
{
    dial_mux_params_t *params = (dial_mux_params_t *)pvParameter;

    led_strip_handle_t strip = params->strip_handle;

    uint8_t response[9] = {0};

    // UART setup
    uart_config_t uart_config = {
        .baud_rate = 38400,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_2,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_APB};
    ESP_ERROR_CHECK(uart_param_config(params->port, &uart_config));
    ESP_ERROR_CHECK(uart_set_pin(params->port, params->tx_pin, params->rx_pin, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE));
    ESP_ERROR_CHECK(uart_set_line_inverse(params->port, UART_SIGNAL_TXD_INV | UART_SIGNAL_RXD_INV));
    // ESP_ERROR_CHECK(uart_set_line_inverse(params->port, UART_SIGNAL_RXD_INV | UART_SIGNAL_TXD_INV));
    ESP_ERROR_CHECK(uart_driver_install(params->port, BUFFER_SIZE * 2, 0, 0, NULL, 0));
    ESP_ERROR_CHECK(uart_set_mode(params->port, UART_MODE_UART));

    // GPIO setup
    gpio_config_t gpio_select_config = {
        .pin_bit_mask = (1ULL << params->sel0) | (1ULL << params->sel1) | (1ULL << params->sel2),
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE};
    ESP_ERROR_CHECK(gpio_config(&gpio_select_config));

    bool received = false;
    float data = 0;
    uint8_t flags = 0b00000000;

    uint8_t mux_dial_start = params->mux_id * 8;

    // data_message_t message_to_send;

    while (1)
    {
        for (uint8_t i = 1; i < 8; i++)
        {
            // gpio_set_level(params->sel2, 0);
            // gpio_set_level(params->sel1, 1);
            // gpio_set_level(params->sel0, 1);
            gpio_set_level(params->sel2, (i >= 4) ? 1 : 0);
            gpio_set_level(params->sel1, (i == 2 || i == 3 || i == 6 || i == 7) ? 1 : 0);
            gpio_set_level(params->sel0, (i == 1 || i == 3 || i == 5 || i == 7) ? 1 : 0);
            
            vTaskDelay(pdMS_TO_TICKS(RESPONSE_TIMEOUT));

            uart_flush(params->port);

            uart_send_bytes(params->port, query, sizeof(query));

            vTaskDelay(pdMS_TO_TICKS(RESPONSE_TIMEOUT));

            if (uart_rx_available(params->port) != 0)
            {
                uart_read_bytes(params->port, response, sizeof(response), pdMS_TO_TICKS(RESPONSE_TIMEOUT));

                flags |= response[3] << i; // Setting flag at appropriate bit

                // for (uint8_t a = 0; a < 9; a++)
                //     printf("Byte %d: %d\n", a, response[a]);


                data = (response[5] << 8) | response[6];
                data = data / 1000;

                received = true;

                // Resetting Data
                for (uint8_t a = 0; a < 9; a++)
                    response[a] = 0;
            }

            // Print on serial or send on queue
            if (received && (i + mux_dial_start) != 0)
            {
                printf("[M%d]: %c%.3f\n", i + mux_dial_start, ((flags >> i) & 1) ? (uint8_t)('-') : (uint8_t)('+'), data);
                led_strip_set_pixel_colour(strip, i, GREEN);
            }
            else
            {
                if (dummy && i < 9)
                {
                    printf("[M%d]: %.3f\n", i + mux_dial_start, dummy_data[i]);
                }
                else
                {
                    printf("[M%d]: --.---\n", i + mux_dial_start);
                    led_strip_set_pixel_colour(strip, i, RED);
                }
            }

            received = false;
            data = 0;
            flags &= ~(1 << i);
            // Resetting Data
            for (uint8_t i = 0; i < 9; i++)
                response[i] = 0;
            uart_flush(params->port);
        }
        vTaskDelay(pdMS_TO_TICKS(DELAY));
    }
}
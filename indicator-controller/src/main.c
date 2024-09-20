#include <freertos/FreeRTOS.h>
// #include <freertos/task.h>
#include <driver/gpio.h>

#include <esp_err.h>
#include <esp_log.h>

#include "iot_button.h"
#include "mux_thread.h"

#define SYS_DELAY(x) vTaskDelay(pdMS_TO_TICKS(x))

// UART Stuff
#define UART1_TX GPIO_NUM_17
#define UART1_RX GPIO_NUM_16
#define UART2_TX GPIO_NUM_36
#define UART2_RX GPIO_NUM_35
#define MUX1_SEL0 GPIO_NUM_13
#define MUX1_SEL1 GPIO_NUM_14
#define MUX1_SEL2 GPIO_NUM_15
#define MUX2_SEL0 GPIO_NUM_18
#define MUX2_SEL1 GPIO_NUM_33
#define MUX2_SEL2 GPIO_NUM_34

// LED Strip Configuration
#include <led_strip.h>
// #include "easy_led_strip.h"
#define NUM_LEDS 8
#define LED_STRIP1_PIN GPIO_NUM_10
#define LED_STRIP2_PIN GPIO_NUM_9

led_strip_handle_t strip1;
led_strip_handle_t strip2;
led_strip_config_t strip_config1 = {
    .strip_gpio_num = LED_STRIP1_PIN,
    .max_leds = NUM_LEDS,
    .led_pixel_format = LED_PIXEL_FORMAT_GRB,
    .led_model = LED_MODEL_WS2812,
};
led_strip_config_t strip_config2 = {
    .strip_gpio_num = LED_STRIP2_PIN,
    .max_leds = NUM_LEDS,
    .led_pixel_format = LED_PIXEL_FORMAT_GRB,
    .led_model = LED_MODEL_WS2812,
};
led_strip_rmt_config_t rmt_config = {
#if ESP_IDF_VERSION < ESP_IDF_VERSION_VAL(5, 0, 0)
    .rmt_channel = 0,
#else
    .clk_src = RMT_CLK_SRC_DEFAULT,    // different clock source can lead to different power consumption
    .resolution_hz = 10 * 1000 * 1000, // 10MHz
    .flags.with_dma = false,           // whether to enable the DMA feature
#endif
};

// Queue Information
#define MAX_ITEMS 16
#define DATA_SIZE sizeof(data_message_t)

// Signal from uart handler, sends appropriate signal when command received from
QueueHandle_t main_request;
// Data response from MUX tasks when data is ready
QueueHandle_t main_response;
uint8_t queue_storage[MAX_ITEMS * DATA_SIZE] = {0};

// Task data
TaskHandle_t mux1_task, mux2_task;
dial_mux_params_t mux1_params = {
    .mux_id = 0,
    .port = UART_NUM_1,
    .tx_pin = UART1_TX,
    .rx_pin = UART1_RX,
    .sel0 = MUX1_SEL0,
    .sel1 = MUX1_SEL1,
    .sel2 = MUX1_SEL2,
};
dial_mux_params_t mux2_params = {
    .mux_id = 1,
    .port = UART_NUM_2,
    .tx_pin = UART2_TX,
    .rx_pin = UART2_RX,
    .sel0 = MUX2_SEL0,
    .sel1 = MUX2_SEL1,
    .sel2 = MUX2_SEL2,
};

// IO Configuration
#define BUTTON_PIN GPIO_NUM_11
#define BUTTON_TAG "BUTTON"
button_handle_t button_handle;
uint8_t state = 0;
#define LED_PIN GPIO_NUM_12
#define MOTOR_DRIVE_A GPIO_NUM_37
#define MOTOR_DRIVE_B GPIO_NUM_38

static void electromagnet_button_cb(void *arg, void *data)
{
    // uint8_t *magnet_state = (uint8_t *)data;

    if (state == 0) // Turn on electromagnet
    {
        state = 1;
        // printf("Turning on Electromagnet!\n");
        gpio_set_level(MOTOR_DRIVE_A, 1);
        gpio_set_level(MOTOR_DRIVE_B, 0);
        gpio_set_level(LED_PIN, !state);
    }
    else
    {
        state = 0;
        // printf("Turning off Electromagnet!\n");
        gpio_set_level(MOTOR_DRIVE_A, 0);

        gpio_set_level(MOTOR_DRIVE_B, 1); // Pulse 1
        SYS_DELAY(130);
        gpio_set_level(MOTOR_DRIVE_B, 0);

        // gpio_set_level(MOTOR_DRIVE_B, 1); // Pulse 2
        // gpio_set_level(MOTOR_DRIVE_B, 0);

        // gpio_set_level(MOTOR_DRIVE_B, 1); // Pulse 3
        // gpio_set_level(MOTOR_DRIVE_B, 0);

        gpio_set_level(LED_PIN, !state);
    }
}

void serial_handler(void *pvParameter)
{
    // QueueHandle_t queue = *((QueueHandle_t *)(pvParameter));
#define BUF_SIZE 16

    while (1)
    {
        // Read data from UART0
        // size_t len;
        // uart_get_buffered_data_len(UART_NUM_0, &len);
        // if (len > 0) {
        //     printf("Received %d bytes\n", len);
        // }
        // while (1)
        // {
        //     uint8_t ch;
        //     ch = fgetc(stdin);
        //     if (ch != 0xFF)
        //     {
        //         fputc(ch, stdout);
        //     }
        // }
        SYS_DELAY(200);
    }
}

void app_main()
{
    // Initialise LED Strip
    ESP_ERROR_CHECK(led_strip_new_rmt_device(&strip_config1, &rmt_config, &strip1));
    ESP_ERROR_CHECK(led_strip_new_rmt_device(&strip_config2, &rmt_config, &strip2));
    led_strip_clear(strip1);
    led_strip_clear(strip2);

    // Initialise LED GPIO & MOTOR GPIO
    gpio_config_t config = {
        .pin_bit_mask = (1ULL << LED_PIN) | (1ULL << MOTOR_DRIVE_A) | (1ULL << MOTOR_DRIVE_B),
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    ESP_ERROR_CHECK(gpio_config(&config));
    gpio_set_level(LED_PIN, 1);
    gpio_set_level(MOTOR_DRIVE_A, 0);
    gpio_set_level(MOTOR_DRIVE_B, 0);

    // Initialise Button
    button_config_t gpio_btn_cfg = {
        .type = BUTTON_TYPE_GPIO,
        .long_press_time = CONFIG_BUTTON_LONG_PRESS_TIME_MS,
        .short_press_time = 100,
        .gpio_button_config = {
            .gpio_num = BUTTON_PIN,
            .active_level = 0,
        },
    };
    button_handle = iot_button_create(&gpio_btn_cfg);
    if (NULL == button_handle)
        ESP_LOGE(BUTTON_TAG, "Button create failed");
    ESP_ERROR_CHECK(iot_button_register_cb(button_handle, BUTTON_PRESS_DOWN, electromagnet_button_cb, NULL));

    // Initialise Queue
    // uart_event_queue = xQueueCreateStatic(MAX_ITEMS, DATA_SIZE, queue_storage, &queue_data_struct);
    main_request = xQueueCreate(MAX_ITEMS, sizeof(char));
    main_response = xQueueCreate(MAX_ITEMS, sizeof(data_message_t));

    mux1_params.data_request = mux2_params.data_request = main_request;
    mux1_params.data_response = mux2_params.data_response = main_response;
    mux1_params.strip_handle = strip1;
    mux2_params.strip_handle = strip2;

    // Worker tasks that add data to the main struct
    // xTaskCreate(dial_mux_main, "MUX1_THREAD", 4096, &mux1_params, 1, &mux1_task);
    // xTaskCreate(dial_mux_main, "MUX2_THREAD", 4096, &mux2_params, 1, &mux2_task);

    // Serial communicator channel
    xTaskCreate(serial_handler, "SERIAL_DATA_HANDLER_THREAD", 256, NULL, 1, NULL);

    // printf("%d - START\n", 0x01); // Start of Packet
    // printf("%d\n", 0x00);         // Length Packet
    // for (uint8_t i = 0; i < 8; i++)
    // {
    //     printf("%d-00.000\n", i);
    // }
    // printf("0x0000\n");
    // printf("%d - END\n\n", 0x04); // End of Packet

    // RPI sends poll command to ESP Serial Handler
    // Serial Handler sends poll command to individual threads on main_request queue
    // Threads send data on main_response queue
    // Serial Handler sends data on main_response queue to RPI
}
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
#define QUERY_RESPONSE_TIMEOUT 50
const uint8_t query[] = {0x01, 0x03, 0x00, 0x00, 0x00, 0x02, 0xC4, 0x0B}; // Micrometer Specific Query Instruction
uint8_t response[9];
typedef struct micrometer_data
{
    uint8_t flags;
    float data[4];
} micrometer_data_t;

// Acceptance Criteria
#define PARALLELISM 0.03
#define PROFILE_NOMINAL 1.6
#define PROFILE_HI_OFFSET 0.2
#define PROFILE_LO_OFFSET 0.1

// Criteria Constants
typedef enum CriteriaConstants
{
    NONE_TRUE,
    PARALELLISM_TRUE_ONLY,
    PROFILE_NOM_TRUE_ONLY,
    BOTH_TRUE,
    ERROR
} criteria_grade_t;
criteria_grade_t grade = NONE_TRUE;

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

// Button Stuff
#define PROGRAM_SWITCH_PIN GPIO_NUM_1
#define ENABLE_SWITCH_PIN GPIO_NUM_44
button_t program_button;
button_t enable_button;
uint8_t enable_switch_state = 0;

// LED Strip Configuration
#include <led_strip.h>
#include "easy_led_strip.h"
#define NUM_LEDS 6
#define LED_STRIP_PIN GPIO_NUM_2

led_strip_handle_t strip;
led_strip_config_t strip_config = {
    .strip_gpio_num = LED_STRIP_PIN,
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

void update_measurements(micrometer_data_t *store)
{
    for (uint8_t channel_index = 0; channel_index < 4; channel_index++)
    {
        // Set channel in CD4052B
        // gpio_set_level(SELECT_A, channel_index & 1);
        // gpio_set_level(SELECT_B, channel_index & 2);
        // SYS_DELAY(10);

        uart_send_bytes(query, sizeof(query));
        SYS_DELAY(QUERY_RESPONSE_TIMEOUT);

        if (uart_rx_available() == 0)
        {
            printf("Response from Micrometer M%d not received!\n", channel_index + 1);
            continue;
        }
        int num_bytes = uart_read_bytes(UART_PORT_NUM, response, sizeof(response), pdMS_TO_TICKS(50));
        printf("NUM BYTES = %d\n", num_bytes);
        for (uint8_t i = 0; i < sizeof(response); i++)
            printf("[BYTE] (%d): %d\n", i, response[i]);
        // printf("---------------\n");
        uint8_t flag = response[3];
        float data = ((response[5] << 8) | response[6]);
        data = data / 1000;

        // Store Data
        store->flags = ~(store->flags ^ (flag << channel_index));
        store->data[channel_index] = data;
    }
    // Resetting
    for (uint8_t i = 0; i < 9; i++)
        response[i] = 0;
    uart_flush(UART_PORT_NUM);
}

void print_measurements(micrometer_data_t *store)
{
    printf("---------------\n");
    printf("----RESULTS----\n");
    printf("---------------\n");
    for (uint8_t channel_index = 0; channel_index < 4; channel_index++)
    {
        printf("[M%d]: %c%.3f\n", channel_index + 1, (store->flags & 1) ? (uint8_t)('-') : (uint8_t)('+'), store->data[channel_index]);
    }
    printf("---------------\n");
}

criteria_grade_t check_criteria(micrometer_data_t *store)
{
    // Assuming not zeroed at micrometer zero!!!!!
    // Parallelism -> |max - min| < PARALLELISM_TOLERANCE
    // Get Max, opposite since data<?> is unsigned
    // Smaller value of data<?> means larger micrometer displacement from build platform
    float max = store->data[0], min = store->data[0];
    if (store->data[1] < max)
        max = store->data[1];
    if (store->data[2] < max)
        max = store->data[2];
    if (store->data[3] < max)
        max = store->data[3];

    // Get Min, opposite since data<?> is unsigned
    // Larger value of data<?> means smaller micrometer displacement from build platform
    if (store->data[1] > min)
        min = store->data[1];
    if (store->data[2] > min)
        min = store->data[2];
    if (store->data[3] > min)
        min = store->data[3];

    // Calculates absolute parallelism value
    float parallelism = ((max - min) >= 0) ? (max - min) : (min - max);
    printf("[Parallelism]: %.3f\n", parallelism);

    // Compute profile nominalness
    uint8_t pronom_flag = 0; // If this is > 0 after calculations, then profile nominality is outside of spec, ie. red light
    pronom_flag = ((PROFILE_NOMINAL - PROFILE_LO_OFFSET <= store->data[0]) && (store->data[0] <= PROFILE_NOMINAL + PROFILE_HI_OFFSET)) ? pronom_flag : pronom_flag | 1;
    pronom_flag = ((PROFILE_NOMINAL - PROFILE_LO_OFFSET <= store->data[1]) && (store->data[1] <= PROFILE_NOMINAL + PROFILE_HI_OFFSET)) ? pronom_flag : pronom_flag | 2;
    pronom_flag = ((PROFILE_NOMINAL - PROFILE_LO_OFFSET <= store->data[2]) && (store->data[2] <= PROFILE_NOMINAL + PROFILE_HI_OFFSET)) ? pronom_flag : pronom_flag | 4;
    pronom_flag = ((PROFILE_NOMINAL - PROFILE_LO_OFFSET <= store->data[3]) && (store->data[3] <= PROFILE_NOMINAL + PROFILE_HI_OFFSET)) ? pronom_flag : pronom_flag | 8;

    if (pronom_flag > 0 && parallelism > PARALLELISM)
        return NONE_TRUE; // Profile Nominal outside spec, parallelism outside of spec, RED
    if (pronom_flag > 0 && parallelism <= PARALLELISM)
        return PARALELLISM_TRUE_ONLY; // Profile Nominal outside spec, parallelism within spec, BLUE
    if (pronom_flag == 0 && parallelism > PARALLELISM)
        return PROFILE_NOM_TRUE_ONLY; // Profile Nominal within spec, parallelism outside spec, YELLOW
    if (pronom_flag == 0 && parallelism <= PARALLELISM)
        return BOTH_TRUE; // Profile Nominal within spec, parallelism within spec, GREEN
    return ERROR;
}

void app_main(void)
{
    // Initialise UART & GPIO
    uart_init();
    ESP_ERROR_CHECK(gpio_config(&gpio_select_config));

    // Button Config
    program_button = create_button(PROGRAM_SWITCH_PIN, true);
    enable_button = create_button(ENABLE_SWITCH_PIN, true);

    // Initialise Micrometer Struct Data
    micrometer_data_t measurement_data = {
        .flags = 0,
        .data = {0, 0, 0, 0}};

    // Initialise LED Strip
    ESP_ERROR_CHECK(led_strip_new_rmt_device(&strip_config, &rmt_config, &strip));
    led_strip_clear(strip);

    gpio_set_level(SELECT_A, 0);
    gpio_set_level(SELECT_B, 1);

    while (1)
    {
        update_button(enable_button);
        update_button(program_button);
        SYS_DELAY(1000);

        if (was_pushed(enable_button))
        {
            printf("Enable Button Pushed!\n");
            enable_switch_state = !enable_switch_state;
        }

        update_measurements(&measurement_data);
        print_measurements(&measurement_data);

        grade = check_criteria(&measurement_data);
        if (grade == NONE_TRUE)
            led_strip_set_colour(strip, NUM_LEDS, palette[RED]);
        else if (grade == PARALELLISM_TRUE_ONLY)
            led_strip_set_colour(strip, NUM_LEDS, palette[BLUE]);
        else if (grade == PROFILE_NOM_TRUE_ONLY)
            led_strip_set_colour(strip, NUM_LEDS, palette[YELLOW]);
        else if (grade == BOTH_TRUE)
            led_strip_set_colour(strip, NUM_LEDS, palette[GREEN]);

        measurement_data.flags = 0;
        measurement_data.data[0] = 0;
        measurement_data.data[1] = 0;
        measurement_data.data[2] = 0;
        measurement_data.data[3] = 0;
    }
}
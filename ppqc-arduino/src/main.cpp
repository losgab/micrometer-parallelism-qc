#include <Arduino.h>
#include <SoftwareSerial.h>
// #include <SSD1306_wrapper.hpp>
#include <Adafruit_NeoPixel.h>
#include <SD.h>
#include <Button.hpp>

// Software Serial Pins
#define MM_RX_1 2 // GOes to D+
#define MM_TX_1 3 // Goes to D-
#define MM_RX_2 4
#define MM_TX_2 5
#define MM_RX_3 6
#define MM_TX_3 7
#define MM_RX_4 8
#define MM_TX_4 9
#define QUERY_WAIT 50

// UI / UX
#define LED_COUNT 6
#define LED_1_PIN A2
#define LED_2_PIN A1

#define BUTTON_PIN A0

// SD Card
#define SD_CS 10
#define SD_MISO 12
#define SD_MOSI 11
#define SD_SCK 13
#define LOG_FILE_NAME "log.txt"

// Acceptance Criteria
#define PARALLELISM 0.03
#define PROFILE_NOMINAL 1.6
#define PROFILE_HI_OFFSET 0.2
#define PROFILE_LO_OFFSET 0.1

// Setup new software Serial
SoftwareSerial micrometer1(MM_RX_1, MM_TX_1, true);
SoftwareSerial micrometer2(MM_RX_2, MM_TX_2, true);
SoftwareSerial micrometer3(MM_RX_3, MM_TX_3, true);
SoftwareSerial micrometer4(MM_RX_4, MM_TX_4, true);
byte query[] = {0x01, 0x03, 0x00, 0x00, 0x00, 0x02, 0xC4, 0x0B}; // Micrometer Specific Query Instruction

// Lights & Colours
Adafruit_NeoPixel strip(LED_COUNT, LED_1_PIN, NEO_GRB + NEO_KHZ800);
uint32_t red = strip.Color(255, 0, 0);
uint32_t blue = strip.Color(0, 0, 255);
uint32_t yellow = strip.Color(255, 255, 0);
uint32_t green = strip.Color(0, 255, 0);
uint32_t aqua = strip.Color(0, 255, 255);
uint32_t last_colour = 0;

// Data fields
uint8_t response[9] = {};
bool flag1, flag2, flag3, flag4 = 0; // If flag, then negative
float data1 = 0, data2 = 0, data3 = 0, data4 = 0;
float parallelism, profile_nominal = 0;

// SD Card stuff
File file;
Button save_button(BUTTON_PIN, true);

// Criteria Constants & Colours
enum CriteriaConstants
{
	NONE_TRUE,
	PARALELLISM_TRUE_ONLY,
	PROFILE_NOM_TRUE_ONLY,
	BOTH_TRUE,
	ERROR
};
typedef CriteriaConstants criteria_grade_t;
criteria_grade_t grade = NONE_TRUE;

// Function Prototypes
void update_micrometers();
void serial_display_readings();
void oled_display_readings();
void save_measurement();
criteria_grade_t check_criteria();
void show_colour(uint32_t colour);

void setup()
{
	Serial.begin(9600);
	// pinMode(SD_CS, OUTPUT);
	// digitalWrite(SD_CS, HIGH);
	// if (!SD.begin(SD_CS))
	// {
	// 	Serial.println("Initialisation Failed!");
	// }

	micrometer1.begin(38400);
	micrometer2.begin(38400);
	micrometer3.begin(38400);
	micrometer4.begin(38400);

	strip.begin();			  // always needed
	strip.show();			  // 0 data => off.
	strip.setBrightness(100); // (max = 255)

	for (uint8_t i = 0; i < LED_COUNT; i++)
	{
		strip.setPixelColor(i, green);
	}
	strip.show();

	// displaySetup();
}

void loop()
{
	save_button.update_button();
	if (save_button.was_pushed())
	{
		save_measurement();
	}

	update_micrometers();
	grade = check_criteria();
	if (grade == NONE_TRUE)
		show_colour(red);
	else if (grade == PARALELLISM_TRUE_ONLY)
		show_colour(blue);
	else if (grade == PROFILE_NOM_TRUE_ONLY)
		show_colour(yellow);
	else if (grade == BOTH_TRUE)
		show_colour(green);
	serial_display_readings();
}

void update_micrometers()
{
	uint8_t i = 0;
	micrometer1.listen();
	response[3] = response[5] = response[6] = 0;
	micrometer1.write(query, sizeof(query));
	delay(QUERY_WAIT);
	while (micrometer1.available())
	{
		response[i] = micrometer1.read();
		i++;
	}
	flag1 = response[3];
	data1 = ((response[5] << 8) | response[6]);
	data1 = data1 / 1000;

	i = 0;
	micrometer2.listen();
	response[3] = response[5] = response[6] = 0;
	micrometer2.write(query, sizeof(query));
	delay(QUERY_WAIT);
	while (micrometer2.available())
	{
		response[i] = micrometer2.read();
		i++;
	}
	flag2 = response[3];
	data2 = ((response[5] << 8) | response[6]);
	data2 = data2 / 1000;

	i = 0;
	micrometer3.listen();
	response[3] = response[5] = response[6] = 0;
	micrometer3.write(query, sizeof(query));
	delay(QUERY_WAIT);
	while (micrometer3.available())
	{
		response[i] = micrometer3.read();
		i++;
	}
	flag3 = response[3];
	data3 = ((response[5] << 8) | response[6]);
	data3 = data3 / 1000;

	i = 0;
	micrometer4.listen();
	response[3] = response[5] = response[6] = 0;
	micrometer4.write(query, sizeof(query));
	delay(QUERY_WAIT);
	while (micrometer4.available())
	{
		response[i] = micrometer4.read();
		i++;
	}
	flag4 = response[3];
	data4 = ((response[5] << 8) | response[6]);
	data4 = data4 / 1000;
}

void serial_display_readings()
{
	// Readout
	Serial.print("M1: ");
	Serial.print(flag1 ? "-" : "+");
	Serial.print(data1, 3);
	Serial.print(" | M2: ");
	Serial.print(flag2 ? "-" : "+");
	Serial.print(data2, 3);
	Serial.print(" | M3: ");
	Serial.print(flag3 ? "-" : "+");
	Serial.print(data3, 3);
	Serial.print(" | M4: ");
	Serial.print(flag4 ? "-" : "+");
	Serial.println(data4, 3);
}

void oled_display_readings() // Not Enabled for memory constraints
{
	// printNewMessage("1 - " + String(data1) + "\n");
	// printMessage("2 - " + String(data2) + "\n");
	// printMessage("3 - " + String(data3) + "\n");
	// printMessage("4 - " + String(data4) + "\n");
}

void save_measurement()
{
	file = SD.open(LOG_FILE_NAME, FILE_WRITE);
	file.seek(EOF);

	file.print("M1: ");
	file.print(flag1 ? "-" : "+");
	file.print(data1 / 1000, 3);
	file.print(" | M2: ");
	file.print(flag2 ? "-" : "+");
	file.print(data2 / 1000, 3);
	file.print(" | M3: ");
	file.print(flag3 ? "-" : "+");
	file.print(data3 / 1000, 3);
	file.print(" | M4: ");
	file.print(flag4 ? "-" : "+");
	file.println(data4 / 1000, 3);
	
	show_colour(aqua);
	show_colour(last_colour);

	file.close();
}

criteria_grade_t check_criteria()
{
	// Assuming not zeroed at micrometer zero!!!!!
	// Parallelism -> |max - min| < PARALLELISM_TOLERANCE
	// Get Max, opposite since data<?> is unsigned
	// Smaller value of data<?> means larger micrometer displacement from build platform
	float max = data1, min = data1;
	if (data2 < max)
		max = data2;
	if (data3 < max)
		max = data3;
	if (data4 < max)
		max = data4;

	// Get Min, opposite since data<?> is unsigned
	// Larger value of data<?> means smaller micrometer displacement from build platform
	if (data2 > min)
		min = data2;
	if (data3 > min)
		min = data3;
	if (data4 > min)
		min = data4;

	// Calculates absolute parallelism value
	parallelism = ((max - min) >= 0) ? (max - min) : (min - max);
	Serial.print("Parallelism: ");
	Serial.println(parallelism);
	// Compute profile nominalness
	uint8_t pronom_flag = 0; // If this is > 0 after calculations, then profile nominality is outside of spec, ie. red light
	pronom_flag = ((PROFILE_NOMINAL - PROFILE_LO_OFFSET <= data1) && (data1 <= PROFILE_NOMINAL + PROFILE_HI_OFFSET)) ? pronom_flag : pronom_flag | 1;
	pronom_flag = ((PROFILE_NOMINAL - PROFILE_LO_OFFSET <= data2) && (data2 <= PROFILE_NOMINAL + PROFILE_HI_OFFSET)) ? pronom_flag : pronom_flag | 2;
	pronom_flag = ((PROFILE_NOMINAL - PROFILE_LO_OFFSET <= data3) && (data3 <= PROFILE_NOMINAL + PROFILE_HI_OFFSET)) ? pronom_flag : pronom_flag | 4;
	pronom_flag = ((PROFILE_NOMINAL - PROFILE_LO_OFFSET <= data4) && (data4 <= PROFILE_NOMINAL + PROFILE_HI_OFFSET)) ? pronom_flag : pronom_flag | 8;

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

void show_colour(uint32_t colour)
{
	for (uint8_t i = 0; i < LED_COUNT; i++)
	{
		strip.setPixelColor(i, colour);
	}
	strip.show();
	last_colour = colour;
}
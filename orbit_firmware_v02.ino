// Orbit-V Firmware Version 0.2 (Hardware Translation)
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Initialize the virtual LCD screen (16 columns, 2 rows)
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Pin Definitions
const int TEMP_PIN = 34;       // Simulated Temperature Sensor Pin
const int CABLE_PIN = 35;      // Simulated Cable Quality Pin
const int BLUE_LED = 2;        // Charging Indicator
const int RED_LED = 4;         // Warning/Pause Indicator

void setup() {
  Serial.begin(115200);
  pinMode(BLUE_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Orbit-V Ready");
  delay(2000);
}

void loop() {
  // 1. Read Simulated Temperature
  int rawTemp = analogRead(TEMP_PIN);
  float currentTemp = (rawTemp / 4095.0) * 100.0; // Simulated range 0-100C

  // 2. Read Simulated Cable Resistance
  int rawCable = analogRead(CABLE_PIN);
  float cableResistance = (rawCable / 4095.0) * 3.0; // Simulated 0-3 Ohms

  lcd.clear();
  
  // 3. Dynamic Thermal Safety Logic (Based on Field Data)
  if (currentTemp >= 45.0) {
    // Critical Heat Pause
    digitalWrite(BLUE_LED, LOW);
    digitalWrite(RED_LED, HIGH); // Red light alert
    lcd.setCursor(0, 0);
    lcd.print("Status: PAUSED");
    lcd.setCursor(0, 1);
    lcd.print("Temp: " + String(currentTemp, 1) + "C Hot");
  } 
  else if (cableResistance > 1.5) {
    // Bad Cable - Throttled Charging
    digitalWrite(BLUE_LED, HIGH);
    digitalWrite(RED_LED, HIGH); // Purple mix (Warning)
    lcd.setCursor(0, 0);
    lcd.print("Status: THROTTLE");
    lcd.setCursor(0, 1);
    lcd.print("Bad Cable Det.");
  } 
  else {
    // Safe Fast Charging
    digitalWrite(BLUE_LED, HIGH);
    digitalWrite(RED_LED, LOW);
    lcd.setCursor(0, 0);
    lcd.print("Status: FAST CHG");
    lcd.setCursor(0, 1);
    lcd.print("Power: 100W Max");
  }

  delay(1000); // Refresh every second
}

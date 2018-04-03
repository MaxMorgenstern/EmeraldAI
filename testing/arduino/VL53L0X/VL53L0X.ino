#include <Wire.h>
#include <VL53L0X.h>

VL53L0X Sensor1;
VL53L0X Sensor2;

const uint8_t Sensor1_xshut = 4;
const uint8_t Sensor2_xshut = 5;

const uint8_t Sensor1_address = 22;
const uint8_t Sensor2_address = 25;

void setup()
{
  pinMode(Sensor1_xshut, OUTPUT);
  pinMode(Sensor2_xshut, OUTPUT);
  digitalWrite(Sensor1_xshut, LOW);
  digitalWrite(Sensor2_xshut, LOW);

  Wire.begin();
  Serial.begin (9600);

  pinMode(Sensor1_xshut, INPUT);
  Sensor1.init(true);
  Sensor1.setAddress(Sensor1_address);
  Sensor1.setTimeout(500);
  Sensor1.startContinuous();

  pinMode(Sensor2_xshut, INPUT);
  Sensor2.init(true);
  Sensor2.setAddress(Sensor2_address);
  Sensor2.setTimeout(500);
  Sensor2.startContinuous();
}

void loop()
{
  Serial.println(Sensor1.readRangeContinuousMillimeters());
  Serial.println(Sensor2.readRangeContinuousMillimeters());
  
  //if (Sensor1.timeoutOccurred()) { Serial.print(" TIMEOUT"); }

  Serial.println("---");
}

#include "freeram.h"

#include "mpu.h"
#include "I2Cdev.h"

// needs to be in inv_mpu.cpp as well
//#define MPU9250
#define MPU6050


//for identity matrix see inv_mpu documentation how this is calculated; this is overwritten by a config packet
uint8_t gyro_orientation = 136;
uint8_t mpu_addr = 0; 

int ret;
void setup() {
    Fastwire::setup(400,0);
    Serial.begin(115200);
    ret = mympu_open(mpu_addr, 200, gyro_orientation);
    Serial.print("MPU init: "); Serial.println(ret);
    Serial.print("Free mem: "); Serial.println(freeRam());
	
}

unsigned int c = 0; //cumulative number of successful MPU/DMP reads
unsigned int np = 0; //cumulative number of MPU/DMP reads that brought no packet back
unsigned int err_c = 0; //cumulative number of MPU/DMP reads that brought corrupted packet
unsigned int err_o = 0; //cumulative number of MPU/DMP reads that had overflow bit set

void loop() {
    #if defined MPU9150 || defined MPU9250
      ret = mympu_update_compass();
    #endif
  
    ret = mympu_update();

    switch (ret) {
	case 0: c++; break;
	case 1: np++; return;
	case 2: err_o++; return;
	case 3: err_c++; return; 
	default: 
		Serial.print("READ ERROR!  ");
		Serial.println(ret);
		return;
    }

    if (!(c%25)) {
      #if defined MPU6050
        Serial.print("MPU6050|"); 
      #endif

      #if defined MPU9150 
        Serial.print("MPU9150|"); 
      #endif

      #if defined MPU6500
        Serial.print("MPU6500|"); 
      #endif
      
      #if defined MPU9250
        Serial.print("MPU9250|"); 
      #endif
      
      Serial.print(np); 
      Serial.print("|"); 
      
      Serial.print(mympu.ypr[0]);
      Serial.print("|"); 
      Serial.print(mympu.ypr[1]);
      Serial.print("|"); 
      Serial.print(mympu.ypr[2]);
      Serial.print("|"); 
      
      Serial.print(mympu.gyro[0]);
      Serial.print("|"); 
      Serial.print(mympu.gyro[1]);
      Serial.print("|"); 
      Serial.print(mympu.gyro[2]);
      Serial.print("|"); 
      
      
      Serial.print(mympu.accel[0]);
      Serial.print("|"); 
      Serial.print(mympu.accel[1]);
      Serial.print("|"); 
      Serial.print(mympu.accel[2]);
      Serial.print("|"); 

      #if defined MPU9150 || defined MPU9250
        Serial.print(mympu.comp[0]);
        Serial.print("|"); 
        Serial.print(mympu.comp[1]);
        Serial.print("|"); 
        Serial.print(mympu.comp[2]);
        Serial.print("|"); 
      #endif
      #if !defined MPU9150 && !defined MPU9250
        Serial.print("0|0|0");
      #endif
      
      Serial.println(""); 
    }
}


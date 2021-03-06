#ifndef MPU_H
#define MPU_H

#include <Arduino.h>

struct s_mympu {
  float ypr[3];
  float gyro[3];
  float accel[3];
#if defined MPU9150 || defined MPU9250
    float comp[3];
#endif
    float gravity;
};

extern struct s_mympu mympu;
extern bool mympu_inverted;

int8_t mympu_open(short addr,unsigned int rate,unsigned short orient);
int8_t mympu_update();
void mympu_reset_fifo();
#if defined MPU9150 || defined MPU9250
int8_t mympu_update_compass();
#endif

#endif



#include <math.h>
#include "Arduino_BMI270_BMM150.h"

float gyro[3];
float acc[3];
float mag[3];

float* ang;

void setup(){
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Started");

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
}


void loop(){
  if (IMU.gyroscopeAvailable() 
  && IMU.accelerationAvailable() 
  && IMU.magneticFieldAvailable()) {
    IMU.readGyroscope(gyro[0], gyro[1], gyro[2]);
    IMU.readAcceleration(acc[0], acc[1], acc[2]);
    IMU.readMagneticField(mag[0], mag[1], mag[2]);
  }

  ang = angles(gyro, acc, mag);
  // for(int i=0; i<3; i++){
  for(int i=0; i<3; i++){
    Serial.print( (*(ang+i)) );
    Serial.print("\t");
  }
  Serial.println();
  delay(250);
}

// Function prototype: angles(gyro: arr[3], acc: arr[3], mag: arr[3])
float* angles(float gyro[3], float acc[3], float mag[3]) {
    float* result = new float[3];  // Array to hold the output: [pitch, roll, yaw]
    
    // Accelerometer calculations for pitch and roll
    float pitch = atan2(acc[1], sqrt(acc[0] * acc[0] + acc[2] * acc[2])) * 180.0 / PI;
    float roll = atan2(-acc[0], acc[2]) * 180.0 / PI;
    
    // Magnetometer calculation for yaw (corrected for pitch and roll)
    float magX = mag[0] * cos(pitch) + mag[1] * sin(roll) * sin(pitch) + mag[2] * cos(roll) * sin(pitch);
    float magY = mag[1] * cos(roll) - mag[2] * sin(roll);
    float yaw = atan2(magY, magX) * 180.0 / PI;
    
    // Store the results in the output array
    result[0] = pitch;
    result[1] = roll;
    result[2] = yaw;
    
    return result;
}
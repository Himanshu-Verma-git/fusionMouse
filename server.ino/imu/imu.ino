/*
  Arduino BMI270 - Simple Gyroscope

  This example reads the gyroscope values from the BMI270
  sensor and continuously prints them to the Serial Monitor
  or Serial Plotter.

  The circuit:
  - Arduino Nano 33 BLE Sense Rev2

  created 10 Jul 2019
  by Riccardo Rizzo

  This example code is in the public domain.
*/

#include "Arduino_BMI270_BMM150.h"

void setup() {
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Started");

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
  Serial.print("Gyroscope sample rate = ");
  Serial.print(IMU.gyroscopeSampleRate());
  Serial.println(" Hz");
  Serial.println();
  Serial.println("Gyroscope in degrees/second");
  Serial.println("X\tY\tZ");

  Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println(" Hz");
  Serial.println();
  Serial.println("Acceleration in G's");
  Serial.println("X\tY\tZ");

  Serial.print("Magnetic field sample rate = ");
  Serial.print(IMU.magneticFieldSampleRate());
  Serial.println(" Hz");
  Serial.println();
  Serial.println("Magnetic Field in uT");
  Serial.println("X\tY\tZ");
}

void loop() {
  float gx, gy, gz;
  float ax, ay, az;
  float mx, my, mz;

  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(gx, gy, gz);

    Serial.print(gx);
    Serial.print('\t');
    Serial.print(gy);
    Serial.print('\t');
    Serial.println(gz);
  }
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(ax, ay, az);

    Serial.print(ax);
    Serial.print('\t');
    Serial.print(ay);
    Serial.print('\t');
    Serial.println(az);
  }

  if (IMU.magneticFieldAvailable()) {
    IMU.readMagneticField(mx, my, mz);

    Serial.print(mx);
    Serial.print('\t');
    Serial.print(my);
    Serial.print('\t');
    Serial.println(mz);
  }

    // Calculate pitch, roll, and yaw
  float pitch = atan2(ay, az) * 180.0 / PI;
  float roll = atan2(ax, sqrt(ay * ay + az * az)) * 180.0 / PI;

  // Yaw calculation using magnetometer data (assumes no calibration for simplicity)
  float yaw = atan2(my, mx) * 180.0 / PI;

  // Output pitch, roll, yaw
  Serial.print("Pitch: ");
  Serial.print(pitch);
  Serial.print(" Roll: ");
  Serial.print(roll);
  Serial.print(" Yaw: ");
  Serial.println(yaw);

  Serial.println();
  delay(250);
}

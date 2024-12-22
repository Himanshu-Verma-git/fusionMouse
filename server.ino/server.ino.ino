#include <ArduinoBLE.h>
#include <math.h>
#include "Arduino_BMI270_BMM150.h"

float gyro[3];
float acc[3];
float mag[3];

float* ang;

// Create a BLE Service
BLEService IMU_Service("180C"); // Custom service UUID
BLECharacteristic IMU_Char("2A56", BLERead | BLENotify, 25); // Custom 
BLECharacteristic flagChar("2A57", BLERead | BLEWrite | BLENotify, 20);

//function prototypes
void details(BLEDevice central);
void writeVal(BLECharacteristic characterstic, int val);

void setup() {
  Serial.begin(9600);
  while (!Serial);

  // Start BLE module
  if (!BLE.begin()) {
    Serial.println("Starting BLE failed!");
    while (1);
  }

  if (!IMU.begin()) {
  Serial.println("Failed to initialize IMU!");
  while (1);
  }

  // Set BLE device properties
  BLE.setLocalName("Nano33BLE_SingleValue");
  BLE.setAdvertisedService(IMU_Service);

  // Add the characteristic to the service
  IMU_Service.addCharacteristic(IMU_Char);
  IMU_Service.addCharacteristic(flagChar);
  
  // Add the service to the BLE stack
  BLE.addService(IMU_Service);

  // Start advertising
  BLE.advertise();
  Serial.println("BLE device is now advertising!");
  
}
 
void loop() {
  // Wait for a BLE central to connect
BLEDevice central = BLE.central();
  if (central) {
    //print details
    details(central);

    //wait until write from client
    while(!flagChar.written() && central.connected()){
      Serial.println("Waiting for Conformation.");
      delay(100);
    }

    if(central.connected()){Serial.print("Connection Confirmed.");}

    while (central.connected()) {

      //  Read Values form sensor
      if (IMU.gyroscopeAvailable() 
      && IMU.accelerationAvailable() 
      && IMU.magneticFieldAvailable()) {
        
        IMU.readGyroscope(gyro[0], gyro[1], gyro[2]);
        IMU.readAcceleration(acc[0], acc[1], acc[2]);
        IMU.readMagneticField(mag[0], mag[1], mag[2]);
      }

      ang = angles(gyro, acc, mag);
      String val = floatToStringConcat( *(ang+0), *(ang+1), *(ang+2) );
      
      writeVal(IMU_Char, val);
      //Notify delay
      delay(200);
    }

    if(!central.connected()){
      Serial.print("Disconnected");
    }
  }
  
}

//write int value to characterstic
void writeVal(BLECharacteristic characterstic, String value){
  characterstic.writeValue(value.c_str());
  Serial.print("Value sent: ");
  Serial.println(value);
}

void details(BLEDevice central){
  Serial.print("(SELF) Server : ");
  Serial.println(BLE.address());
  Serial.print("Connected to central: ");
  Serial.println(central.address());
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

String floatToStringConcat(float num1, float num2, float num3) {
  return String(num1, 2) + "_" + String(num2, 2) + "_" + String(num3, 2);
}
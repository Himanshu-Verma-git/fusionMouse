#include <ArduinoBLE.h>

// Create a BLE Service
BLEService simpleService("180C"); // Custom service UUID

// Create a BLE Characteristic for sending an integer value
BLECharacteristic sampleChar("2A56", BLERead | BLENotify, sizeof(int)); // Custom characteristic UUID for an integer
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

  // Set BLE device properties
  BLE.setLocalName("Nano33BLE_SingleValue");
  BLE.setAdvertisedService(simpleService);

  // Add the characteristic to the service
  simpleService.addCharacteristic(sampleChar);
  simpleService.addCharacteristic(flagChar);
  
  // Add the service to the BLE stack
  BLE.addService(simpleService);

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
    delay(5000);


    //wait until write from client
    while(!flagChar.written() && central.connected()){
      delay(100);
      Serial.println("Unchanged");
      }

      if(central.connected()){
      Serial.print("Value Changed");
        for(int i=0; i<20; i++){
        writeVal(sampleChar, i);
        delay(500);
      }
      }

    //keep the connection alive
    while (central.connected()) {
      delay(200);
    }

    if(!central.connected()){
      Serial.print("Disconnected");
    }
  }
  
}

//write int value to characterstic
void writeVal(BLECharacteristic characterstic, int value){
  characterstic.writeValue((int16_t)value);
  Serial.print("Value sent: ");
  Serial.println(value);
}

void details(BLEDevice central){
  Serial.print("(SELF) Server : ");
  Serial.println(BLE.address());
  Serial.print("Connected to central: ");
  Serial.println(central.address());
}
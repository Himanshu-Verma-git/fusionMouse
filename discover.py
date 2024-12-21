'''
set name for device to connect to
scan devices(handle errors while scanning)
try to connect to the device
set deviceConnected=true
subscribe to service=IMU
subsribe to notification of specific charaterstic
'''
import bleak
import asyncio
from bleak import BleakClient, BleakScanner

async def scan():
    print("Scanning...")
    devices:dict = await BleakScanner.discover(return_adv=True, timeout=3)
    for device, adv in devices.values():
        if("Nano33BLE_SingleValue" == device.name):
            print(device,end="\n")
            print(adv)
            return device, adv

async def connect(device: bleak.backends.device.BLEDevice):
    async with BleakClient(device) as client:
        print("Connecting ", device.name)
        if(client.is_connected):print("Success")
        else:print("Failed")
        
        #get service and char
        SERVICE_UUID = "0000180c-0000-1000-8000-00805f9b34fb"
        CHAR_UUID = "00002a56-0000-1000-8000-00805f9b34fb"
        
        async def notification_handler(characterstic, data: bytearray):
            data = int.from_bytes(data, byteorder='little', signed=True)
            print("Data: ", data)
            
        await client.start_notify(CHAR_UUID, notification_handler)
        # await client.stop_notify(CHAR_UUID)

async def get_val(CHAR_UUID, client:BleakClient)->int:
    val = await client.read_gatt_char(CHAR_UUID)
    return int.from_bytes(val, byteorder='little', signed=True)

def servs_and_chars(client:BleakClient):
    services = client.services
    for service in services:
        print(f"\nService: {service.uuid}")
        print(f"Description: {service.description}")
        print(type(service.uuid))
        for characteristic in service.characteristics:
            print(f"    1.Characteristic: {characteristic.uuid}")
            print(type(characteristic.uuid))
            print(f"    2.Properties: {characteristic.properties}")
            print(f"    3.Description: {characteristic.description}")
            print(f"    4.Descriptors: {characteristic.descriptors}")
    

async def main():
    device, adv = await scan()
    print(type(device))
    await connect(device)
    
asyncio.run(main())
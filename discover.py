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
    devices:dict = await BleakScanner.discover(return_adv=True, timeout=3, )
    for device, adv in devices.values():
        if("Nano33BLE_SingleValue" == device.name):
            print(device,end="\n")
            print(adv)
            return device
    return None

async def connect(device: bleak.backends.device.BLEDevice):
    print("Connecting ", device.name)
    try:
        async with BleakClient(address_or_ble_device= device, timeout= 2) as client:
            if(client.is_connected):print("Connected")
            else:
                print("Failed")
                return None
            
            #get service and char
            SERVICE_UUID = "0000180c-0000-1000-8000-00805f9b34fb"
            CHAR_UUID = "00002a56-0000-1000-8000-00805f9b34fb"
            
            async def notification_handler(characterstic, data: bytearray):
                data = int.from_bytes(data, byteorder='little', signed=True)
                print("Data: ", data)
                
            await client.start_notify(CHAR_UUID, notification_handler)
            #keeping connection alive until connected
            while (client.is_connected):
                await asyncio.sleep(1)
            await client.stop_notify(CHAR_UUID)
    except asyncio.exceptions.CancelledError as e:
        print(e)

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
    device = await scan()
    print(type(device))
    if(device):await connect(device)
    
asyncio.run(main())
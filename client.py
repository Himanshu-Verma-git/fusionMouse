'''
Author: Himanshu Verma
Functions:
    connect->BLEClient
    scan->bleak.backends.device.BLEDevice
    servs_and_chars->None
    
'''
import bleak
import asyncio
from bleak import BleakClient, BleakScanner

async def scan()->bleak.backends.device.BLEDevice:
    print("Scanning...")
    devices:dict = await BleakScanner.discover(return_adv=True)
    for device, adv in devices.values():
        if("Nano33BLE_SingleValue" == device.name):
            print(device,end="\n")
            print(adv)
            return device
    return None

async def notification_handler(characterstic, data: bytearray):
    data = int.from_bytes(data, byteorder='little', signed=True)
    print("Data: ", data)
async def connect(device: bleak.backends.device.BLEDevice):
    print("Connecting ", device.name)
    try:
        async with BleakClient(address_or_ble_device= device, timeout=15) as client:
            print("Connected")
            
            #get service and char
            SERVICE_UUID = "0000180c-0000-1000-8000-00805f9b34fb"
            CHAR_UUID = "00002a56-0000-1000-8000-00805f9b34fb"
            FLAG_CHAR = "00002a57-0000-1000-8000-00805f9b34fb"
            
            await client.write_gatt_char(FLAG_CHAR, b'\x01')
            print("Value written")
                    
            await client.start_notify(CHAR_UUID, notification_handler)
            while(client.is_connected): await asyncio.sleep(1)
            await client.stop_notify(CHAR_UUID)
    
    except (asyncio.exceptions.CancelledError) as e:print("Exception CancelledError: ", e)
    except (TimeoutError) as e:print("Timeout: ", e)
    except Exception as e:print("Exception: ", e)

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
    if(device): await connect(device)
    
asyncio.run(main())
# import bleak
# import asyncio
# from bleak import BleakClient, BleakScanner

# class Client:
    
#     def __init__():
#         pass
    
#     def Client()->None:
#         pass
        
#     def Client(self, device: bleak.backends.device.BLEDevice)->None:
#         self.device = device
        
#     @classmethod
#     async def scan()->dict:
#         return await BleakScanner.discover(return_adv=True)
    
    
# def choose_dev(dev_adv:dict):
#     i=1
#     for dev, adv in dev_adv.values():
#         print("\n",i,". ")
#         print("Device: ", dev)
#         print("Adv: ", adv)
#         i+=1
#     choice: int = input("Choice: ")
    
    
# def main():
#     device_adv:dict = Client.scan()
    
#     client = Client(choose_device(device_adv))

import bleak
import asyncio
from bleak import BleakClient, BleakScanner

async def scan(device_name="Nano33BLE_SingleValue")->bleak.backends.device.BLEDevice:
    devices:dict = await BleakScanner.discover(return_adv=True)
    for device, adv in devices.values():
        if(device_name == device.name):
            return device
    return None

async def notification_handler(characterstic, data: bytearray):
    data = int.from_bytes(data, byteorder='little', signed=True)
    print("Data: ", data)

async def main():
    IMU_UUID = "00002a56-0000-1000-8000-00805f9b34fb"
    FLAG_CHAR = "00002a57-0000-1000-8000-00805f9b34fb"
    
    print("Scanning...")
    device:bleak.backends.device.BLEDevice = await scan()
    
    if(device == None):
        print("Nano33BLE_SingleValue not found.")
        return
    
    try:
        async with BleakClient(device) as client:
            print("Connected")
            await client.start_notify(IMU_UUID, notification_handler)
            await client.write_gatt_char(FLAG_CHAR, b'\x01')
            
            while(client.is_connected):await asyncio.sleep(1)
            await client.stop_notify(IMU_UUID)
            
    except asyncio.exceptions.CancelledError:print("Future Cancel Error")
    except TimeoutError:print("Timeout. Try Again.")
    except Exception:print("Abrubt Abort. Try Again.")

asyncio.run(main())
import bleak

class Client:
    def __init__(self):
        self.device: bleak.BleakClient = None
        self.connected: bool = False
    
    async def connect_device(self, device) -> None:
        self.device = bleak.BleakClient(device)
        self.connected = await self.device.connect()
        self.services = self.device.services
    
    async def disconnect_device(self)->None:
        self.device.disconnect()

    @classmethod
    async def scan(cls)->dict:
        return await bleak.BleakScanner.discover(return_adv=True)
    
    @classmethod
    async def scan_device(cls, device_name)->tuple:
        devices = await bleak.BleakScanner.discover(return_adv=True)
        for device, adv in devices.values():
            if(device.name == device_name):
                return device
        return None
    
    async def writeToChar(self, char_uuid, value):
        try:
            await self.device.write_gatt_char(char_uuid, value)
        except Exception as e:
            print("Exception: ", e)
    
    async def servAndChar(self):
        return self.device.services
    #default notification_handler, pass your async funtion as notification_handler while calling start_notify()
    @classmethod
    async def notification_handler(self, char_uuid, data: bytearray)->None:
        print("Data: ", data.decode("utf-8"))
    
    async def start_notification(self, char_uuid, handler = None):
        if(not self.device.is_connected):raise TimeoutError
        if(handler):    await self.device.start_notify(char_uuid, handler)
        else:   await self.device.start_notify(char_uuid, Client.notification_handler)

    
    async def stop_notification(self, char_uuid):
        await self.device.stop_notify(char_uuid)
    
"""_summary_
Notes:
    1.  After enabling notification remember to keep it alive using an async looping function.
        Eg: while(client.is_connected): await asyncio.sleep(1)
        This will keep the program running. 
"""









# '''
# Author: Himanshu Verma
# Functions:
#     connect->BLEClient
#     scan->bleak.backends.device.BLEDevice
#     servs_and_chars->None
    
# '''
# import bleak
# import asyncio
# from bleak import BleakClient, BleakScanner

# async def scan()->bleak.backends.device.BLEDevice:
#     print("Scanning...")
#     devices:dict = await BleakScanner.discover(return_adv=True)
#     for device, adv in devices.values():
#         if("Nano33BLE_SingleValue" == device.name):
#             print(device,end="\n")
#             print(adv)
#             return device
#     return None

# async def notification_handler(characterstic, data: bytearray):
#     # data = int.from_bytes(data, byteorder='little', signed=True)
#     print("Data: ", data.decode("utf-8"))
    
# #------------------------------------------------------------------------------------------------------------------
# # async def connect(device: bleak.backends.device.BLEDevice):
# #     print("Connecting ", device.name)
# #     try:
# #         async with BleakClient(address_or_ble_device= device, timeout=15) as client:
# #             print("Connected")
            
# #             #get service and char
# #             SERVICE_UUID = "0000180c-0000-1000-8000-00805f9b34fb"
# #             CHAR_UUID = "00002a56-0000-1000-8000-00805f9b34fb"
# #             FLAG_CHAR = "00002a57-0000-1000-8000-00805f9b34fb"
            
# #             await client.write_gatt_char(FLAG_CHAR, b'\x01')
# #             print("Value written")
                    
# #             await client.start_notify(CHAR_UUID, notification_handler)
# #             while(client.is_connected): await asyncio.sleep(1)
# #             await client.stop_notify(CHAR_UUID)
    
# #     except (asyncio.exceptions.CancelledError) as e:print("Exception CancelledError: ", e)
# #     except (TimeoutError) as e:print("Timeout: ", e)
# #     except Exception as e:print("Exception: ", e)
# #------------------------------------------------------------------------------------------------------------------

# #------------------------------------------------------------------------------------------------------------------
# async def connect_device(device):
#     print("Connecting...")
#     client = BleakClient(device)
#     try:
#         # Attempt to connect to the device
#         connected = await client.connect()
        
#         if not connected:
#             print("Failed to connect")
#             return
        
#         print("Connected")

#         # Perform service discovery
#         services = client.services
#         if not services:
#             print("No services found.")
#             return
        
#         # Display services and characteristics
#         for service in services:
#             print(f"Service: {service.uuid}")
#             for characteristic in service.characteristics:
#                 print(f"  Characteristic: {characteristic.uuid}")

#         # Now you can interact with the device's characteristics
#         FLAG_CHAR = "00002a57-0000-1000-8000-00805f9b34fb"
#         await client.write_gatt_char(FLAG_CHAR, b'\x01')
#         print("Value written")
            
#         # Start notifications on a characteristic
#         CHAR_UUID = "00002a56-0000-1000-8000-00805f9b34fb"
#         await client.start_notify(CHAR_UUID, notification_handler)
#         while client.is_connected:
#             await asyncio.sleep(1)
#         await client.stop_notify(CHAR_UUID)

#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         if client.is_connected:
#             await client.disconnect()
#             print("Disconnected")
    
    
# #------------------------------------------------------------------------------------------------------------------

# async def get_val(CHAR_UUID, client:BleakClient)->int:
#     val = await client.read_gatt_char(CHAR_UUID)
#     return int.from_bytes(val, byteorder='little', signed=True)

# def servs_and_chars(client:BleakClient):
#     services = client.services
#     for service in services:
#         print(f"\nService: {service.uuid}")
#         print(f"Description: {service.description}")
#         print(type(service.uuid))
#         for characteristic in service.characteristics:
#             print(f"    1.Characteristic: {characteristic.uuid}")
#             print(type(characteristic.uuid))
#             print(f"    2.Properties: {characteristic.properties}")
#             print(f"    3.Description: {characteristic.description}")
#             print(f"    4.Descriptors: {characteristic.descriptors}")
    

# async def main():
#     device = await scan()
#     print(type(device))
#     if(device): await connect_device(device)
    
# asyncio.run(main())
'''
set name for device to connect to
scan devices(handle errors while scanning)
try to connect to the device
set deviceConnected=true
subscribe to service=IMU
subsribe to notification of specific charaterstic
'''

import asyncio
from bleak import BleakClient, BleakScanner

async def scan():
    print("Scanning...")
    devices = await BleakScanner.discover(return_adv=True)
    print(type(devices))
    for d, a in devices.values():
        print()
        print(d)
        print("-" * len(str(d)))
        print(a)

async def connect()->BleakClient:
        pass

async def main():
    await scan()
    pass
    
asyncio.run(main())
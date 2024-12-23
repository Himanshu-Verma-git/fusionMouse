from client import Client
import calculations
import asyncio
import bleak

async def main():
    CHAR_UUID = "00002a56-0000-1000-8000-00805f9b34fb"
    FLAG_CHAR = "00002a57-0000-1000-8000-00805f9b34fb"
    
    print("Scanning..")
    client = Client()
    await Client.scan()
    server_add = await Client.scan_device("Nano33BLE_SingleValue")
    # server_add = "06:70:DB:B3:CD:E8"

    if(not server_add):
        print("No Device Found")
        return
    
    print("Server Add: ", server_add)
    print("-------------------------------------------------------------------------------------------")
    
    try:
        await client.connect_device(server_add)
    except bleak.exc.BleakError as e:
        print(f"Connection failed: {e}")
    except TimeoutError as e:
        print(f"Timeout error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    if(client.connected):print("Connected")
    else:
        print("Connection Failed.")
        return
    
    # await client.servAndChar()
    # print("-------------------------------------------------------------------------------------------")
    
    await client.writeToChar(FLAG_CHAR, b'\x01')
    await client.start_notification(CHAR_UUID)
    print("Conformation Sent.")
    
    while(client.connected): 
        print("Keep ALive")
        await asyncio.sleep(1)
    
    await client.stop_notification(char_uuid=CHAR_UUID)
    await client.disconnect_device()
    print("Disconnected")


if __name__ == "__main__":
    asyncio.run(main())
from kasa import Discover 
import asyncio

def main(): 
    devices = asyncio.run(Discover.discover())
    device_ips = []
    for addr, dev in devices.items():
        asyncio.run(dev.update())
        device_ips.append(f"{addr}")
    f = open("python_src/ips.txt", "w")
    f.write('\n'.join(device_ips))
    f.close()

if __name__ == "__main__": 
    main()
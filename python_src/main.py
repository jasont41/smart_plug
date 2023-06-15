from kasa import Discover, SmartPlug
from pprint import pformat as pf
import asyncio
import time
import sys
import socket
import power_msg_pb2
'''
Gathers IP addresses of smart plugs on the network
'''
def get_device_ips():
    ips = []
    with open("/home/python_src/ips.txt") as f: 
        for line in f: 
            ips.append(line)
    return ips

'''
Sends message to proxy 
'''
def send_msg(msg): 
    udp_ip = socket.gethostbyname('proxy')
    udp_port = 25000
    msg_serialized = msg.SerializeToString()
    print("sending message.. \n")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #   Implied bind called on ip and port 
    sock.sendto(msg_serialized, (udp_ip, udp_port))

'''
Gets realtime power consumption
'''
def get_realtime_consumption(plugs):
    print("getting realtime power use")
    #   Thread this method once new messages are needed
    while True:
        for plug in plugs: 
            asyncio.run(plug[1].update())
            power_msg = power_msg_pb2.PowerMsg()
            power_msg.name = plug[0]
            #   I only care about wattage, it is power after all
            power_msg.current_power_consumption = int(plug[1].emeter_realtime['power_mw']/ 1000)
            power_msg.timestamp = int(time.time())
            send_msg(power_msg)
            time.sleep(0.25)
            
'''
Create Plug Objects
'''
def create_objs(devices):
    plugs = []
    names = []
    for dev in devices: 
        plugs.append(SmartPlug(dev))
    # Get names of plugs for reporting 
    for dev in plugs:
        asyncio.run(dev.update())
        names.append(dev.sys_info['alias'])
    if len(plugs) == 0: 
        print("nothing is here")
    return list(zip(names, plugs))
    

def main():
    device_ips = get_device_ips()
    if len(device_ips) == 0: 
        print("no devices, exiting")
        sys.exit()
    #   Create SmartPlug Objects 
    plugs = create_objs(device_ips)
    get_realtime_consumption(plugs)
    return 0


if __name__ == "__main__": 
    main()
import socket 
import sys
import time
import power_msg_pb2
import threading 
import os 


'''
Send packet to frontend
'''
def send_packet(msg): 
    print("Proxying packet")
    udp_ip = os.getenv('FRONTEND_IP') 
    udp_port = int(os.getenv('FRONTEND_PORT'))
    msg_serialized = msg.SerializeToString()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(msg_serialized, (udp_ip, udp_port))


def main(): 
    udp_ip = socket.gethostbyname("proxy")
    print(udp_ip)
    udp_port = 25000
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
    sock.bind((udp_ip,udp_port))
    while True: 
        print("Receiving Packets.. ")
        try: 
            data,addr = sock.recvfrom(4096)
            power_msg = power_msg_pb2.PowerMsg()
            power_msg.ParseFromString(data)
            #   Proxy packet to front end 
            send_thread = threading.Thread(target=send_packet,args=(power_msg, ))
            send_thread.start()
        except Exception as e: 
            print(e)
            print("timed out")

if __name__ == "__main__": 
    main()
import sys
from scapy.all import *
def help():
    print("----------USAGE----------")
    print("\t" + sys.argv[0] + " [-c] [-s] [-u] [-x] [-f] [-n] <ip:port>")
    print("OPTIONS") 
    print("\t-c:TCP connect scan ")
    print("\t-s:TCP stealth scan")
    print("\t-x:TCP xmas scan")
    print("\t-f:TCP fin scan")
    print("\t-n:TCP null scan")
    print("\t-u:UDP scan")
    print("\t<ip:port>:destination ip address and ports")
    print("\n\nEXAMPLE:\n\t" + sys.argv[0] + " -c 172.16.111.115:80")

FIN = 0x01
SYN = 0x02
RST = 0x04
PSH = 0x08
ACK = 0x10
URG = 0x20
ECE = 0x40
CWR = 0x80

sport = random.randint(1024,65535)

def TcpConnect(ip,port):
    """
        Open: return 1
        Closed: return 0
        No response: return -1
    """
    print("TCP connect scan:")
    print("------------------")
    pkt = IP(dst=ip)/TCP(sport = sport,dport = port,flags = "S")
    ans = sr1(pkt,retry = 2,timeout = 0.2)
    if not ans:
        return -1
    F=ans['TCP'].flags
    if F & ACK and F & SYN :
        pkt = IP(dst=ip)/TCP(sport = sport,dport = port,seq = ans.ack,ack = ans.seq+1,flags = "AR")
        send(pkt)
        return 1
    elif F & RST and F & ACK:
        return 0
    else:
        return -1

def TcpStealthy(ip,port):
    """
        Open: return 1
        Closed: return 0
        No response: return -1
    """
    print("TCP stealth scan:")
    print("------------------")
    pkt = IP(dst = ip)/TCP(sport = sport,dport = port,flags = "S") 
    ans = sr1(pkt,retry = 2,timeout = 0.2)    
    if not ans :
        return -1
    F=ans['TCP'].flags
    if F & ACK and F & SYN:
        send(IP(dst = ip)/TCP(sport = sport,dport = port,seq = ans.ack,ack = ans.seq+1,flags = "R"))
        return 1
    elif F & ACK and F & RST:
        return 0

def TcpXmas(ip,port):
    """
        Closed: return 1
        Open or Filtered: return 0
        Else case: return -2
    """
    print("TCP xmas scan:")
    print("------------------")
    pkt = IP(dst = ip)/TCP(sport = sport,dport = port,flags = "FPU")
    ans = sr1(pkt,retry = 2,timeout = 0.2)
    if not ans :
        return 0
    F=ans['TCP'].flags
    if F & RST :
        return 1
    return -2

def TcpFin(ip,port):
    """
       Closed: return 1
       Open or Filtered: return 0
       Else case: return -2
    """
    print("TCP fin scan:")
    print("------------------")
    pkt = IP(dst = ip)/TCP(sport = sport,dport = port,flags = "F")
    ans = sr1(pkt,retry = 2,timeout = 0.2)
    if not ans:
        return 0
    F=ans['TCP'].flags
    if F & RST:
        return 1
    return -2 

def TcpNull(ip,port):
    """
       Closed: return 1
       Open or Filtered: return 0
       Else case: return -2
    """
    print("TCP null scan:")
    print("------------------")
    pkt = IP(dst = ip)/TCP(sport = sport,dport = port,flags = "")
    ans = sr1(pkt,retry = 2,timeout = 0.2)
    if not ans:
        return 0
    F=ans['TCP'].flags
    if F & RST:
        return 1
    return -2 

def UdpScan(ip,port):
    """
        Closed: return 1
        Open: return 0
        Filtered: return -1
        Open or Filtered: return -2
    """
    print("UDP scan:")
    print("------------------")
    pkt = IP(dst = ip)/UDP(sport = sport,dport = port)
    ans = sr1(pkt,retry = 2,timeout = 0.2)
    if not ans:
        return -2
    if ans.haslayer(UDP):
        return 0
    if ans.haslayer(ICMP):
        if int(ans.getlayer(ICMP).type)==3 and  int(ans.getlayer(ICMP).code)==3:
            return 1
        if int(ans.getlayer(ICMP).type)==3 and  int(ans.getlayer(ICMP).code) in [1,2,9,10,13]:
            return  -1
    return -3

if __name__=="__main__":
    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
    if len(args) >1 or len(args) ==0:
        help()
        exit(1)
    dividPos = args[0].find(":")
    if(dividPos ==-1):
        print("No port...")
        sys.exit(1)
    ip = args[0][:dividPos]
    port = int(args[0][dividPos + 1:])
    if "-c" in opts :
        res=TcpConnect(ip,port)
        if res == 1:
            print("Open")
        elif res== 0:
            print("Closed")
        else :
            print("Filtered")
    elif "-s" in opts:
        res = TcpStealthy(ip,port)
        if res == 1:
            print("Open")
        elif res== 0:
            print("Closed")
        else :
            print("Filtered")

    elif  "-x" in opts:
        res = TcpXmas(ip,port) 
        if res == 1:
            print("Closed")
        elif res ==0:
            print("Open or Filtered")
        else:
            print("xmax abnormal...")
    elif "-f" in opts:
        res = TcpFin(ip,port)
        if res ==1:
            print("Closed")
        elif res==0:
            print("Open or Filtered")
        else:
            print("No else case handled...")
    elif "-n" in opts:
        res = TcpNull(ip,port)
        if res ==1:
            print("Closed")
        elif res==0:
            print("Open or Filtered")
        else:
            print("No else case considered...")
    elif "-u" in opts:
        res = UdpScan(ip,port)
        if res ==1:
            print("Closed")
        elif res ==0:
            print("Open")
        elif res ==-1:
            print("Filtered")
        elif res ==-2:
            print("Open or Filtered")
        else:
            print("No else case considered")
    else:
        help()
        sys.exit(1)
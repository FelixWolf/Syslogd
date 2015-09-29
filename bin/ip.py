import socket, struct, math

def ip2long(addr):
    return struct.unpack("!L", socket.inet_aton(addr))[0]
    
def long2ip(addr):
    return socket.inet_ntoa(struct.pack('!L', addr))

    
def inRangeInt(input, p1, p2):
    if type(input) == str:
        input = ip2long(input)
    if type(p1) == str:
        p1 = ip2long(p1)
    if type(p2) == str:
        p2 = ip2long(p2)
    return p1 < input < p2

def inRangeStr(input, r):
    input=ip2long(input)
    if r.find("/") == -1:
        r=r+"/32"
    r, m = r.split("/")
    r=ip2long(r)
    nm = ~int(math.pow(2,(32-ip2long(m)))-1)
    return (input&nm)==(r&nm)

def inRange(input, p1, p2=None):
    if p2:
        return inRangeInt(input, p1, p2)
    return inRangeStr(input, p1)
#!/usr/bin/env python
print("[Syslogd] Server is starting...")
#Stock modules
import os, sys, socket, json, threading, signal, time, datetime
#Server modules
import sysLogPriorities, ip

#Default configuration
config = {
    "host": "0.0.0.0",
    "port": 514,
    "range": "127.0.0.1/32",
    "verbose": False,
    "logdir": "../var/syslog/"
}

#Load user config file
userConfig = {}
f = None
try:
    #We take the apple
    if len(sys.argv) > 1:
        f = open(sys.argv[2],"r+")
    else:
        f = open("../var/syslogd.conf","r+")
    try:
        userConfig = json.loads(f.read());
    except json.JSONDecodeError as e: #Its a bad apple file
        print("[ERR] Failed to load syslogd.conf!\nLine %i: %s"%(e.pos,e.msg))
        exit()
except IOError as e: #The apple doesn't even exist
    print("[ERR] Failed to load syslogd.conf!\n%i: %s"%(e.errno, e.strerror))
    exit()
#We eat the apple
f.close();

#Override config with userConfig, keeping defaults if not exist
for i in userConfig:
    config[i] = userConfig[i]


#Binding sockets
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
try:
    sock.bind((config["host"], config["port"]))
except OSError as e:
    print("[ERR] Cannot bind to port %i:\n%s"%(config["port"],e.msg))
    exit()

#We made it
def server_main():
    def parseSysLog(input):
        if input.find("<")==0: #Sanity check
            x = input.find(">")
            if x==-1: #Sanity check
                return (
                    5,
                    (
                        sysLogPriorities.origins[5],
                        sysLogPriorities.serverities[4]
                    ),
                    "Unknown packet recieved: %s" % input.strip()
                )
            code = int(input[1:x])
            return (
                code,
                sysLogPriorities.resolveMatrix(code),
                input[x+1:].strip()
            )
        return (
            5,
            (
                sysLogPriorities.origins[5],
                sysLogPriorities.serverities[4]
            ),
            "Unknown packet recieved: %s" % input.strip()
        )

    while True:
        data, addr = sock.recvfrom(1024)
        if ip.inRange(addr[0],config["range"]):
            data = parseSysLog(data.decode("latin1"))
            now = datetime.datetime.now()
            msg = "[%s.%s] %s@%s: %s" % (
                now.strftime("%Y-%m-%dT%H:%M:%S"),
                str(now.microsecond).zfill(6),
                data[1][1], data[1][0],
                data[2]
            )
            f = open("%s%s-%s.log" %
                (
                    config["logdir"],
                    addr[0],
                    now.strftime("%y%m%d")
                ), 'ab+')
            f.write((msg+"\n").encode("latin1"))
            f.close()
            if config["verbose"]:
                print(addr[0]+">"+msg)
            

server_thread = threading.Thread(target=server_main)
server_thread.daemon = True
server_thread.start()

def shutdown(signal, frame):
        print("[Syslogd] Sigint recieved, shutting down.")
        sock.close()
        sys.exit(0)

print("[Syslogd] Server listening on port %i."%config["port"])

signal.signal(signal.SIGINT, shutdown)

#Main loop
if os.name == 'nt':
    #Windows has no support for signal.pause()
    while True:
        time.sleep(0xff)
else:
    #Pause is better than sleep
    while True:
        signal.pause()


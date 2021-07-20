
import time
import sys
import pprint
from mctools import RCONClient
from mctools.mclient import QUERYClient
#**************************************************************
#setup logging early so we can log as much as possible
DEBUG = False
LOGFILE = "mc_log.txt"
def log_event(event):
    with open(LOGFILE, 'a') as log:
        log.write(event+"\n")
#**************************************************************
# define function to grab auth info
admin_info = []
KEYFILE = "mc_admin.txt"
def get_admin_info():
    '''opens 'mc_admin.txt' to get auth info for minecraft client.File must be in . of script.
    Only place keyvalue remove any ' or " from string, order is important
    ex. 192.168.0.1  #host to connect to
        password     #password used for rcon communication
        25575        #port to connect to
        
    note:
        password/port is set on minecraft server. in a file called server.properties located in root of server instance
    '''
    log_event("[*] Looking for mc_admin.txt")
    try:    
        with open(KEYFILE, "r") as keytemp:
            log_event("[*] Found mc_admin.txt")
            for line in keytemp:
                line = line.strip()
                admin_info.append(line)
        keytemp.close()
        return(admin_info[0], admin_info[1],admin_info[2])
    except FileNotFoundError as err:
        print("[*] mc_admin.txt was not found please make sure it is present....")
        log_event("[*] mc_admin.txt was not found please make sure it is present....")
        sys.exit()
#*****************************************************************
#get auth info for use in script
auth = get_admin_info()
#******************************************************************
#create variables from mc_admin.txt
IP = auth[0]
PASS = auth[1]
Sport = auth[2]
#******************************************************************
# call our rcon\query client classes with settings
rc = RCONClient(IP,port=Sport)
qc = QUERYClient(IP)
#******************************************************************
#add some stuff for printing
pp = pprint.PrettyPrinter()
#
#send cmds to server
def send_cmd(cmd):
    '''sends cmd to server'''
    response = rc.command(cmd)
    return response
#client loop for talking to server
def client_loop():
    '''main loop for talking to server'''
    keepalive = False
    try:
        print("[*] Connected to "+IP+":"+str(Sport))
        log_event("[*] Connected to "+IP+":"+str(Sport))
        try:
            if keepalive:
                print("[*] keep alive on")
                msg = "keep alive msg to prevent console freeze please ignore."
                whattodo = send_cmd("say " +msg)
                print(str(whattodo))
                time.sleep(600)
                looper()
            else:
                pass
        except KeyboardInterrupt:
            print("[*] exiting keep alive function")
            rc.stop()
            qc.stop()
            sys.exit()
        whattodo = input("[*]Welcome!!!! Type help to see availible options\n>>> ")
        if whattodo == "cmd":
            c = input("[*] please enter cmd to run:\n>> ")
            if DEBUG:
                print("[*] trying to send cmd")
            resp = send_cmd(c)
            pp.pprint("[*] "+str(resp))
        elif whattodo == "broadcast":
            message = input("[*] msg to broadcast?\n>>> ")
            if DEBUG:
                print("[*] trying to send "+message)
            resp = send_cmd("say "+message)
            print("[*] "+str(resp))
        elif whattodo == "msg":
            usr = input("[*] please specify user\n>>> ")
            message = input("[*] msg to send?\n>>> ")
            if DEBUG:
                print("[*] trying to send "+message+" to "+usr)
            resp = send_cmd("msg "+usr+" "+message)
            print("[*] "+str(resp))
        elif whattodo == "query":
            c = input("[*] Full or Basic?\n[*] ")
            if c == "full" or "Full":
                stats= qc.get_full_stats()
                for k,v in stats.items():
                    print("[*] "+k+": ", v)
            else:
                stats = qc.get_basic_stats()
                for k,v in stats.items():
                    print("[*] "+k+": ", v)
        elif whattodo == "help":
            options = ["broadcast - sends msg to all players", "exit - exits the session to current server", "query - queries server for info", "cmd - sends commands to server ex: help", "msg - sends msg to specified user"]
            for item in options:
                print("[*] "+item)
        elif whattodo == "exit":
            print("[*] Shutting down.....")
            log_event("[*] Shutting down.....")
            time.sleep(2)
            #kill the connection to server
            rc.stop()
            qc.stop()
            sys.exit()
    except Exception as err:
        print(err)
    else:
        #jump back into func to continue work
        looper()
#jump back in for work
def looper():
    '''returns to client_loop'''
    time.sleep(3)
    client_loop()
#login to server
def login():
    try:
        rc.login(PASS)
        client_loop()
    except TimeoutError as e:
        print("A timeout occured contacting the server")
        print(e)


login()
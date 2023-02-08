"""
This file tries to imitate the mctools binary but with added abilities, automatically attempts to login to server given the right info
to allow commmunication between u and the server. this file along with a few others will allow full connection to "server" including file transfers
for "updating config files" and the like.
"""
import time
import sys
import pprint
from mctools import RCONClient
from mctools.mclient import QUERYClient
from log_handler import mylogger
#
# define function to grab auth info
def check_admin_info():
    '''opens 'mc_admin.txt' to get auth info for minecraft client.File must be in . of script.
    Only place keyvalue remove any ' or " from string, order is important returns info for get_login_info()
    ex. 192.168.0.1  #host to connect to
        password     #password used for rcon communication
        25575        #port to connect to
        
    note:
        password/port is set on minecraft server. in a file called server.properties located in root of server instance
    '''
    try:    
        with open(KEYFILE, "r", encoding='utf-8') as keytemp:
            #logs.info("[*] Found mc_admin.txt")
            for line in keytemp:
                line = line.strip()
                admin_info.append(line)
        keytemp.close()
        return(admin_info[0], admin_info[1],admin_info[2])
    except FileNotFoundError as err:
        print(err)
        logs.info("[*] mc_admin.txt was not found please make sure it is present....%s", err.with_traceback())
        sys.exit()

def get_login_info():
    """
    get auth info for use in script and pass to setup_rcon_client()

    returns ip,pass,port
    """
    logs.info("[*] looking for auth info to access server")
    auth = check_admin_info()
    ip = auth[0]
    passw = auth[1]
    port = auth[2]
    return(ip,passw,port)

def setup_rcon_client():
    """
    get rcon info for use in script returns a list of values.

    returns rcclient, qcclient , pass , ip, port
    """
    logs.info("[*] grabbing rcon settings")
    info =get_login_info()
    port = info[2]
    ip = info[0]
    paswd = info[1]
    rc = RCONClient(info[0],port=info[2])
    qc = QUERYClient(info[0])

    return(rc,qc,paswd,ip,port)

#send cmds to server
def send_cmd(cmd):
    '''sends cmd to server'''
    response = rc.command(cmd)
    return response

def run_cmd_on_server():
    """
    runs specified cmds on server.returns a response
    """

    c = input("[*] please enter cmd to run:\n>> ")
    if DEBUG:
        print("[*] trying to send cmd")
    logs.info(msg = f"[*] sending cmd: {c}")
    resp = send_cmd(c)
    new_list = resp
    item = new_list.replace("\n",",")
    item = new_list.replace("'","")
    item = new_list.replace("Dim","[*]")
    logs.info(item)



def broadcast_to_all_users():
    """
    Broadcasts msg to all users.
    """
    message = input("[*] msg to broadcast?\n>>> ")
    if DEBUG:
        print("[*] trying to send "+message)
    resp = send_cmd("say "+message)
    logs.info("[*] "+str(resp))

def send_msg_to_user():
    """
    sends msg to specified user.
    """
    usr = input("[*] please specify user\n>>> ")
    message = input("[*] msg to send?\n>>> ")
    if DEBUG:
        print("[*] trying to send "+message+" to "+usr)
    resp = send_cmd("msg "+usr+" "+message)
    logs.info("[*] "+str(resp))

def query_server_info():
    """
    queries server for info
    """
    c = input("[*] Full or Basic?\n[*] ")
    if c == "full" or "Full":
        stats= qc.get_full_stats()
        for k,v in stats.items():
            print("[*] "+k+": ", v)
    else:
        stats = qc.get_basic_stats()
        for k,v in stats.items():
            logs.info("[*] "+k+": ", v)


def get_help():
    """
    returs help for use in software
    """
    options = ["broadcast - sends msg to all players", "exit - exits the session to current server", "query - queries server for info", "cmd - sends commands to server ex: help", "msg - sends msg to specified user"]
    for item in options:
        logs.info("[*] "+item)

def kill_console():
    """
    kills connection to server then closes program.
    """
    logs.info(msg="[*] Shutting down.....")
    time.sleep(2)
     #kill the connection to server
    rc.stop()
    qc.stop()
    sys.exit()

def client_loop():
    """
    main loop for talking to server
    """
    try:
        logs.info("[*] Connected to %s:%s", IP, str(Sport))
        whattodo = input("[*]Welcome!!!! Type help to see availible options\n>>> ")
        if whattodo == "cmd":
           run_cmd_on_server()
        elif whattodo == "broadcast":
           broadcast_to_all_users()
        elif whattodo == "msg":
            send_msg_to_user()
        elif whattodo == "query":
            query_server_info()
        elif whattodo == "help":
            get_help()
        elif whattodo == "exit":
            kill_console()
    except Exception as err:
        logs.exception(err.with_traceback())
    else:
        #jump back into func to continue work
        looper()

def looper():
    '''returns to client_loop'''
    time.sleep(3)
    client_loop()

def login():
    """
    starts main routine to login to server
    """

    try:
        logs.info(msg= "[*] Attempting to login to server")
        rc.login(PASS)
        if rc.is_authenticated():
            logs.info(msg= "[*] Success!!!")
            client_loop()
    except TimeoutError as e_err:
        message = "A timeout occured contacting the server. the following error was recieved. %s", str(e_err.with_traceback())
        logs.warning(msg= message)


#main function to start app. sets system wide variables for operation.
if __name__ == '__main__':
    admin_info = []
    #define our log and key file
    KEYFILE = "mc_admin.txt"
    LOGFILE = "mc_log.txt"
    #setup logging early so we can log as much as possible
    logs = mylogger("mclogger", LOGFILE)
    logs.info(msg=f"[{logs.name}] Initializing logger")
    #only for testing
    DEBUG = False
    #add some stuff for printing
    pp = pprint.PrettyPrinter()
    #setup rcon values to login
    rcon_values = setup_rcon_client()
    rc = rcon_values[0]
    qc = rcon_values[1]
    PASS = rcon_values[2]
    IP = rcon_values[3]
    Sport = rcon_values[4]
    #attempt login to server
    login()


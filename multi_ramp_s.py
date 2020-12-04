import socket
import sys
import os
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()

all_connections = []
all_address = []

port = 9999
s_created = False
bind = False
create_s_err = ''
bind_err = ''

stop_all_threads = False

# TODO: update interface
# TODO: implement buffer change
# TODO: clean all da shity code
# TODO: clock sync on them pis how?


# Create socket on given port and host ip
def create_socket():
    try:
        global host 
        global port 
        global create_s_err
        global s 
        global s_created
        host = ''
        s = socket.socket()
        s_created = True

    except socket.error as msg:
        create_s_err = 'Socket creation error: ' + str(msg) + '\n'

# binding socket to server // handling error
def bind_socket():
    try:
        global host 
        global port 
        global s 
        global bind
        global bind_err
        s.bind((host, port))
        bind = True
        s.listen(5)
    except socket.error as msg:
        bind_err = 'socket binding error: ' + str(msg) + '\n' + 'retrying'
        bind_socket()

# handling connections from multiple clients
def accepting_connections():
    for c in all_connections:
        c.close()
    
    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1) # prevents timeout
            all_connections.append(conn)
            all_address.append(address)

            print("Connected to: " + address[0])
        except socket.error as msg:
            print("Error while connecting to clients: " + str(msg))



# start and contral interface basicly main loop
def start_player():

    global bind
    global create_s_err
    global bind_err
    disp_head()

    while True:

        if not s_created:
            print(create_s_err)
            continue

        if not bind:
            print(bind_err)
            continue
  
        disp_menu()

        user_in = input('DECIDE! ')
        
        handle_user_in(user_in)


# Handle input of user and react to commands
def handle_user_in(user_in):
    global s
    if user_in == '1':
       pass
    elif user_in == '2':
        while True:
            disp_player()

            user_in = input('\nDECIDE! ')

            if user_in == "pl":
                broadcast("pl")
            elif user_in =='pa':
                broadcast("pa")
            elif user_in == 'sf':
                print("Not implemented")
            elif user_in == 'sb':
                print("Not implemented")
            elif user_in == 'quit':
                break
            else:
                print("Can't you read?")
                time.sleep(1)
    elif user_in == '4':
        s.close()
        global stop_all_threads
        stop_all_threads = True
        print('\nSee ya!')
        sys.exit()

    else:
        print("Cant you read?")
        time.sleep(1)



# display first menu with basic functionality
def disp_menu():
    disp_head()
    print("\n [1] List connected clients")
    print("\n [2] Send command to all clients")
    print("\n [3] Edit play buffer")
    print("\n [4] Quit")
    print('\n')
    

def disp_player():
    disp_head()
    print("\n [pl] play")
    print("\n [pa] pause")
    print("\n [sf] skip forward")
    print("\n [sb] skip bakwrds")
    print("\n [quit] go back to menu")
    print("\n\n Currently playing: ")
    print('\n')


# Clear screen and display head
def disp_head():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\t**********************************************")
    print("\t***********  RAMP-SOUND-INTERFACE  ***********")
    print("\t**********************************************")



def broadcast(msg):
    for i, conn in enumerate(all_connections):
        conn.send(str.encode(msg))
     

# list all connected clients
def list_connections():
    results = ''
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(201480)
        except:
            del all_connections[i]
            del all_address[i]
            continue

        results = results + str(i) + " " + str(all_address[i][0]) + " " + str(all_address[i][1]) + "\n"

    print("\t--------CLIENTS--------\n" + results)


# target single client
def get_target(cmd):
    try:
        target = cmd.replace("select ","")
        target = int(target)
        conn = all_connections[target]
        print("You selected: " + str(all_address[target][0]))
        print(str(all_address[target][0]) + "$", end = '')
        return conn
    except:
        print("Selection not valid")
        return None


def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            
            if cmd == 'q':
                conn.close()
                s.close()
                sys.exit()

            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480),'utf-8')
                print(client_response, end='')
        except:
            print("Error Sending commands")
            break


def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()
    
# Do next qued job
def work():
    global stop_all_threads
    while True:
        if stop_all_threads:
            print("kill")
            break
        x = queue.get()
        if  x == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        if x == 2:
            start_player()
        queue.task_done()

     

def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()

create_workers()
create_jobs()
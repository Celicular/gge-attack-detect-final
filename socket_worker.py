import base64
from threading import Thread
from pygge.gge_socket import GgeSocket
import json


socket = None
# username = "ADeadKraken"
# password = "Himadri"
MAP_MIN_X, MAP_MIN_Y = 550, 550
MAP_MAX_X, MAP_MAX_Y = 733, 733
CHUNK_SIZE = 13
ISLAND_TYPES = {9: "Level 80", 7: "Level 60", 8: "Level 70"}
all_data = []
count = 0
progress = 0
tries = 0



def decode(e): return base64.urlsafe_b64decode(e.encode()).decode()
def retry():
    global socket, tries
    if socket is None and tries <= 3:
        tries += 1
    
    if tries > 3:
        print("tried 3 times, no solution")
        return

    initialize_socket()

def validate(x):
    return


def initialize_socket(username, password):
    print("starting socket")

    try:
        global socket
        socket = GgeSocket("wss://ep-live-world1-game.goodgamestudios.com", "EmpireEx_46")

        Thread(target=socket.run_forever, daemon=True).start()
        Thread(target=socket.keep_alive, daemon=True).start()

        socket.init_socket()
        socket.login(username, password)
        return True
    except Exception as e:
        if "Unexpected status: 453" in str(e):
            print("[ERROR] Blocked (status 453).")
        elif "Unexpected status: 20" in str(e):
            print("[ERROR] Wrong username or password.")
            return False
        else:
            print("[ERROR] General exception:", e)
        return False


def getuserinfo():
    global socket
    response = socket.get_account_infos()
    return response

def formatData(x : list):
    global all_data
    all_data.append(x)
    return

def scan_map_chunk(x, y):
    
    global socket, count
    count += 1
    
    filterislands = []
    islanddata, isle_dat=[], []
    # response = send_command(f'get_map_chunk(4, {x}, {y})')
    response = socket.get_map_chunk(4, x, y) 
    islands = response["payload"]["data"]["AI"]
    for arr in islands:
        if (len(arr) == 9 and
        all(isinstance(item, (int, float)) for item in arr) and
        arr[5] in ISLAND_TYPES and
        arr[6] == 0 and
        arr[8] == 0):
            filterislands.append(arr)
    
    for arr in filterislands:
        islanddata.append(arr[1])
        islanddata.append(arr[2])
        islanddata.append(arr[5])
        islanddata.append(arr[7])
        isle_dat.append(islanddata.copy())
        islanddata.clear()

        print("found ", len(isle_dat), " in chunk", x , " " , y)
        return isle_dat

def storm_scan():
    global MAP_MAX_X, MAP_MAX_Y, MAP_MIN_Y, MAP_MIN_Y, all_data, count
    count=0

    if socket is None:
        initialize_socket()
    print("socket running")

    for x in range(MAP_MIN_X, MAP_MAX_X, 13):
        for y in range(MAP_MIN_Y, MAP_MAX_Y, 13):
            print("scanning chunk : ", x,y)
            data = scan_map_chunk(x, y)
            
            if data is None:
                continue
            else:
                formatData(data)
            
    return [item[0] for item in all_data if item]

def normal_scan():
    lvl80, lvl70, lvl60 = [], [], []
    data = storm_scan()
    for arr in data:
        arr.append(0)
    for arr in data:
        if arr[2] == 9:
            lvl80.append(arr)
        elif arr[2] == 8:
            lvl70.append(arr)
        else:
            lvl60.append(arr)

    return lvl60, lvl70, lvl80


def spiral_scan(x, y):
    newarr = []
    lvl80, lvl70, lvl60 = [], [], []
    data = storm_scan()
    print("calculating distance")
    for arr in data:
        temp_x = arr[0]
        temp_y = arr[1]
        dist = int(((temp_x-x)**2 + (temp_y-y)**2)**0.5)
        arr.append(dist)
        newarr.append(arr)

    for arr in newarr:
        if arr[2] == 9:
            lvl80.append(arr)
        elif arr[2] == 8:
            lvl70.append(arr)
        else:
            lvl60.append(arr)

    for lvl in (lvl60, lvl70, lvl80):
        lvl.sort(key = lambda x:x[4])

    return lvl60, lvl70, lvl80
    

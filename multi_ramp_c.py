import socket
import os
import subprocess
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import glob
s = socket.socket()
host = '192.168.178.159'
port = 9999

current_dir = os.getcwd()
sound_paths = glob.glob(current_dir + '/sound/*.wav')

track_pointer = 0

s.connect((host, port))

# TODO: implement time buffer
# TODO: implement functions


while True:
    data = s.recv(1024)

    if len(data) > 0:
        if data[:].decode() == 'lsit':
            s.send(str.encode(' '))


        elif data[:].decode() == 'pl':
            print("SHIT WORKS..PLAY")

            pygame.mixer.init()
            pygame.mixer.music.load(sound_paths[track_pointer])
            pygame.mixer.music.play()

        elif data[:].decode() == 'pa':
            print("SHIT WORKS..STOP")
            pygame.mixer.music.stop()

        elif data[:].decode() == 'sf':
            print("SHIT WORKS..SKIP FORWARD")
            
            if len(sound_paths) == 0:
                continue

            if track_pointer == len(sound_paths) -1:
                track_pointer = 0
            else:
                track_pointer += 1

        elif data[:].decode() == 'sb':
            print("SHIT WORKS..SKIP BACKWARD")

            if len(sound_paths) == 0:
                continue

            if track_pointer == 0:
                track_pointer = len(sound_paths) -1
            else:
                track_pointer -= 1
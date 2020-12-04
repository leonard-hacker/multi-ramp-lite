import socket
import os
import subprocess
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

s = socket.socket()
host = '192.168.178.148'
port = 9999

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
            pygame.mixer.music.load("la_priest_rubber_sky.wav")
            pygame.mixer.music.play()

        elif data[:].decode() == 'pa':
            print("SHIT WORKS..STOP")
            pygame.mixer.music.stop()

        elif data[:].decode() == 'sf':
            print("SHIT WORKS..SKIP FORWARD")

        elif data[:].decode() == 'sb':
            print("SHIT WORKS..SKIP BACKWARD")
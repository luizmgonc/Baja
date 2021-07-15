from tkinter import *
from tkinter import ttk
import pygame
from serial.serialutil import SerialException
import serial.tools.list_ports
import serial
import sys
import time
# Inicialização Janela

pygame.mixer.init()

def verificar():
    pygame.mixer.music.load("D:\Baja\ECI\Git Pessoal\Interface Motor SEG\images\song.wav")
    pygame.mixer.music.play(loops = -1)


menu = Tk()
menu.title("Configuração Porta Serial")
menu.geometry("%dx%d" % (400, 150))


# Inicialização Widgets

label0 = Label(menu, text="Porta Serial:")

enviarButton = Button(text="Enviar", command=verificar)
succedLabel = Label(menu, text = '')


# Pack
label0.pack(pady=10)
enviarButton.pack(pady=(0, 15))
succedLabel.pack()

menu.mainloop()

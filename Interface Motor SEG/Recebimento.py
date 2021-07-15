from tkinter import *
from tkinter import ttk
import time
import serial
import threading
from PIL import ImageTk, Image
import serial.tools.list_ports
import pygame
import traceback

from serial.serialutil import SerialException

# Funções


def animation(count):
    global anim
    im2 = im[count]
    print(count)
    label.configure(image=im2)
    count += 1
    if count == 200:
        count = 0
    anim = menu.after(100, lambda: animation(count))


def resize():
    global colorCount
    if(menu.winfo_width() == 762):
        print(menu.winfo_width())
        menu.geometry("%dx%d+%d+%d" % (366, 746, 560, 25))
        pygame.mixer.music.stop()

        menu.after_cancel(anim)

    else:
        print(menu.winfo_width())
        menu.geometry("%dx%d+%d+%d" % (762, 746, 360, 25))
        colorCount += 1
        animation(0)
        pygame.mixer.music.load("images\song.wav")
        pygame.mixer.music.play()

        if(colorCount % 2 == 1):
            leoFrame["bg"] = "#9769ee"
        else:
            leoFrame["bg"] = "#0b7aa5"


def pausar():
    global pause
    pause = not pause
    print(pause)


def receiveSerial():

    while(not fim):

        try:
            while(not pause):

                if(not ser.isOpen()):
                    ser.open()
                mensagem = ser.readline()
                lista = mensagem.decode("utf-8").split()
                atualizarInterface(lista)

            time.sleep(0.05)
        except:
            traceback.print_exc()

        print("HEre 3")
        ser.close()

        # time.sleep(0.01)
    print("HEre 3")


def atualizarInterface(lista):
    checksumActualTorque .set(lista[4])
    aliveCounterActualTorque .set(lista[5])

    if(int(lista[6]) == 0):
        runState .set(f"{lista[6]} (Pre-run)")
    elif(int(lista[6]) == 1):
        runState .set(f"{lista[6]} (Run)")
    elif(int(lista[6]) == 2):
        runState .set(f"{lista[6]} (Post-Run)")
    elif(int(lista[6]) == 3):
        runState .set(f"{lista[6]} (Post-Run Finished)")
    else:
        runState .set(lista[6])

    if(int(lista[7]) == 0):
        operationMode .set(f"{lista[7]} (Idle Mode)")
    elif(int(lista[7]) == 1):
        operationMode .set(f"{lista[7]} (Torque Mode)")
    elif(int(lista[7]) == 4):
        operationMode .set(f"{lista[7]} (Voltage Mode)")
    elif(int(lista[7]) == 6):
        operationMode .set(f"{lista[7]} (Speed Mode)")
    elif(int(lista[7]) == 11):
        operationMode .set(f"{lista[7]} (Start Mode)")
    elif(int(lista[7]) == 14):
        operationMode .set(f"{lista[7]} (Stand-by)")
    elif(int(lista[7]) == 15):
        operationMode .set(f"{lista[7]} (Failure)")
    else:
        operationMode .set(lista[7])

    torque .set("%.1f Nm" % float(lista[0]))
    speed .set(f"{lista[1]} rpm")
    voltage .set("%.4f V" % float(lista[2]))
    current .set(f"{lista[3]} A")

    checksumRequest .set(lista[8])
    aliveCounterRequest .set(lista[9])
    torqueCalculation .set("%.1f Nm" % float(lista[10]))
    speedCalculation .set(f"{lista[11]} rpm")
    machineTemperature .set(f"{lista[12]} %")
    inverterTemperature .set(f"{lista[13]} %")
    startPossible .set(lista[14])
    torquePlausibilisation .set(lista[15])

    checksumAvailableTorque .set(lista[16])
    aliveCounterAvailableTorque .set(lista[17])
    maximumLimitedTorque .set("%.1f Nm" % float(lista[18]))
    maximumAvailableTorque .set("%.1f Nm" % float(lista[19]))
    minimumLimitedTorque .set("%.1f Nm" % float(lista[20]))
    minimumAvailableTorque .set("%.1f Nm" % float(lista[21]))
    actualDeratingState .set(lista[22])


im = []


def carregarGif():
    global im

    im = [PhotoImage(
        file=f"images\ezgif-7-80017838cabb-gif-im\\frame_00{i}_delay-0.02s.png") for i in range(10)]
    for i in range(10, 100):
        im.append(PhotoImage(
            file=f"images\ezgif-7-80017838cabb-gif-im\\frame_0{i}_delay-0.02s.png"))
    for i in range(100, 214):
        im.append(PhotoImage(
            file=f"images\ezgif-7-80017838cabb-gif-im\\frame_{i}_delay-0.02s.png"))


def verificar():
    try:
        global ser
        global su
        entrada = lista.get()
        separada = entrada.split()

        ser = serial.Serial(
            port=separada[0],
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )

        ser.close()
        print(ser)
        succedLabel['text'] = "Conexão bem sucedida!"
        succedLabel['fg'] = "green"
        menuSerial.after(800, menuSerial.destroy)

    except:
        succedLabel['text'] = "Conexão mal sucedida! Tente novamente."
        succedLabel['fg'] = "red"
        succedLabel.pack()
        traceback.print_exc()


# Inicialização Janela Serial
ser = serial.Serial()
menuSerial = Tk()
menuSerial.title("Configuração Porta Serial")
menuSerial.geometry("%dx%d+%d+%d" % (400, 150, 560, 300))

# Listagem portas Seriais
ports = serial.tools.list_ports.comports()
valores = ports

# Inicialização Widgets
label0 = Label(menuSerial, text="Porta Serial:")
lista = ttk.Combobox(menuSerial, values=valores, width=50)
enviarButton = Button(text="Enviar", command=verificar)
succedLabel = Label(menuSerial, text='')

# Pack
label0.pack(pady=10)
lista.pack(pady=(0, 10))
enviarButton.pack(pady=(0, 15))
succedLabel.pack()

menuSerial.mainloop()
# -------------------------------------------------------


# Inicialização Janela

menu = Tk()
menu.title("Jupiter CAN Interface")
menu.geometry("%dx%d+%d+%d" % (366, 746, 560, 25))
menu.resizable(False, False)

# Variáveis Globais
checksumActualTorque = StringVar()
aliveCounterActualTorque = StringVar()
runState = StringVar()
operationMode = StringVar()
torque = StringVar()
speed = StringVar()
voltage = StringVar()
current = StringVar()

checksumRequest = StringVar()
aliveCounterRequest = StringVar()
torqueCalculation = StringVar()
speedCalculation = StringVar()
machineTemperature = StringVar()
inverterTemperature = StringVar()
startPossible = StringVar()
torquePlausibilisation = StringVar()

checksumAvailableTorque = StringVar()
aliveCounterAvailableTorque = StringVar()
maximumLimitedTorque = StringVar()
maximumAvailableTorque = StringVar()
minimumLimitedTorque = StringVar()
minimumAvailableTorque = StringVar()
actualDeratingState = StringVar()

pause = False
fim = False

count = 0
anim = None

colorCount = 0

# Inicialização

pygame.mixer.init()
serialThread = threading.Thread(target=receiveSerial)
serialThread.setDaemon(True)

# Instanciação de Frames

leoFrame = Frame(menu, bg="#0b7aa5", bd=3, relief=SOLID)
dataButtonsFrame = Frame(menu, bd=5, relief=SOLID, bg="black")
buttonsFrame = Frame(dataButtonsFrame, bg="black")
buttonFrame = Frame(buttonsFrame, bg="black")
dataFrame = Frame(dataButtonsFrame, bd=1, relief=SOLID)

# Instanciação de Widgets

initButton = Button(buttonFrame, text="Iniciar recebimento",
                    command=serialThread.start)
pauseButton = Button(buttonFrame, text="Pause / Unpause", command=pausar)

my_jup = Image.open("images\jUPITER_vetorizado.png")
resized = my_jup.resize((230, 40), Image.ANTIALIAS)
new_jup = ImageTk.PhotoImage(resized)
jupiter = Label(dataButtonsFrame, image=new_jup,
                bg="black", width=354, height=60)

my_bot = Image.open("images\\botao.png")
resized = my_bot.resize((100, 100), Image.ANTIALIAS)
new_bot = ImageTk.PhotoImage(resized)
dangerButton = Button(buttonsFrame, image=new_bot, bd=0,
                      command=resize, bg="black", activebackground="black")

label = Label(leoFrame, bd =0)


# Criação de Labels de Dados

edrvActFrame = Frame(dataFrame)

Label(edrvActFrame, text="Checksum Actual Torque: ", anchor=SW, width=23).grid()
Label(edrvActFrame, text="Alive counter actual torque: ", anchor=W, width=23).grid()
Label(edrvActFrame, text="Actual run state: ",
      anchor=W, width=23).grid(sticky=W)
Label(edrvActFrame, text="Actual operation mode: ", anchor=W, width=23).grid()
Label(edrvActFrame, text="Actual torque: ", anchor=W, width=23).grid()
Label(edrvActFrame, text="Actual speed: ", anchor=W, width=23).grid()
Label(edrvActFrame, text="Actual DC voltage: ", anchor=W, width=23).grid()
Label(edrvActFrame, text="Actual DC current: ", anchor=W, width=23).grid()

EdrvActVariablesFrame = Frame(dataFrame)

Label(EdrvActVariablesFrame, textvariable=checksumActualTorque,
      anchor=E, width=17).grid()
Label(EdrvActVariablesFrame, textvariable=aliveCounterActualTorque,
      anchor=E, width=17).grid()
Label(EdrvActVariablesFrame, textvariable=runState, anchor=E, width=17).grid()
Label(EdrvActVariablesFrame, textvariable=operationMode, anchor=E, width=17).grid()
Label(EdrvActVariablesFrame, textvariable=torque, anchor=E, width=17).grid()
Label(EdrvActVariablesFrame, textvariable=speed, anchor=E, width=17).grid()
Label(EdrvActVariablesFrame, textvariable=voltage, anchor=E, width=17).grid()
Label(EdrvActVariablesFrame, textvariable=current, anchor=E, width=17).grid()

# -------------------------------------------------------


edrvReqFrame = Frame(dataFrame)

Label(edrvReqFrame, text="Checksum request ", anchor=SW, width=23).grid()
Label(edrvReqFrame, text="Alive counter request: ", anchor=W, width=23).grid()
Label(edrvReqFrame, text="Torque Calculation EEM: ", anchor=W, width=23).grid()
Label(edrvReqFrame, text="Speed Calculation EEM: ", anchor=W, width=23).grid()
Label(edrvReqFrame, text="Machine Temperature State: ", anchor=W, width=23).grid()
Label(edrvReqFrame, text="Inverter Temperature State: ", anchor=W, width=23).grid()
Label(edrvReqFrame, text="Start possible state: ", anchor=W, width=23).grid()
Label(edrvReqFrame, text="Torque plausibilisation state: ",
      anchor=W, width=23).grid()

edrvReqVariablesFrame = Frame(dataFrame)

Label(edrvReqVariablesFrame, textvariable=checksumRequest,
      anchor=E, width=17).grid()
Label(edrvReqVariablesFrame, textvariable=aliveCounterRequest,
      anchor=E, width=17).grid()
Label(edrvReqVariablesFrame, textvariable=torqueCalculation,
      anchor=E, width=17).grid()
Label(edrvReqVariablesFrame, textvariable=speedCalculation,
      anchor=E, width=17).grid()
Label(edrvReqVariablesFrame, textvariable=machineTemperature,
      anchor=E, width=17).grid()
Label(edrvReqVariablesFrame, textvariable=inverterTemperature,
      anchor=E, width=17).grid()
Label(edrvReqVariablesFrame, textvariable=startPossible, anchor=E, width=17).grid()
Label(edrvReqVariablesFrame, textvariable=torquePlausibilisation,
      anchor=E, width=17).grid()

# -------------------------------------------------------

edrvPredFrame = Frame(dataFrame)

Label(edrvPredFrame, text="Checksum available torque: ",
      anchor=SW, width=23).grid()
Label(edrvPredFrame, text="Alive counter available torque: ",
      anchor=W, width=23).grid()
Label(edrvPredFrame, text="Maximum limited torque: ", anchor=W, width=23).grid()
Label(edrvPredFrame, text="Maximum available torque: ", anchor=W, width=23).grid()
Label(edrvPredFrame, text="Minimum limited torque: ", anchor=W, width=23).grid()
Label(edrvPredFrame, text="Minimum available torque: ", anchor=W, width=23).grid()
Label(edrvPredFrame, text="Actual derating state: ", anchor=W, width=23).grid()

edrvPredVariablesFrame = Frame(dataFrame)

Label(edrvPredVariablesFrame, textvariable=checksumAvailableTorque,
      anchor=E, width=17).grid()
Label(edrvPredVariablesFrame, textvariable=aliveCounterAvailableTorque,
      anchor=E, width=17).grid()
Label(edrvPredVariablesFrame, textvariable=maximumLimitedTorque,
      anchor=E, width=17).grid()
Label(edrvPredVariablesFrame, textvariable=maximumAvailableTorque,
      anchor=E, width=17).grid()
Label(edrvPredVariablesFrame, textvariable=minimumLimitedTorque,
      anchor=E, width=17).grid()
Label(edrvPredVariablesFrame, textvariable=minimumAvailableTorque,
      anchor=E, width=17).grid()
Label(edrvPredVariablesFrame, textvariable=actualDeratingState,
      anchor=E, width=17).grid()

# -------------------------------------------------------

# Grid Button Frame
initButton.grid(row=0, padx=(30, 0), pady=(15, 10))
pauseButton.grid(row=1, padx=(30, 0), pady=(0, 15))
buttonFrame.grid(row=0)

# Grid Buttons Frame
dangerButton.grid(row=0, column=1,  padx=(40, 20))
buttonsFrame.grid()

# Grid Data Frame
edrvActFrame.grid(row=2, pady=(10, 10), padx=(10, 0))
EdrvActVariablesFrame.grid(row=2, column=1, pady=(10, 10), padx=(0, 10))
edrvReqFrame.grid(row=3, pady=10, padx=(10, 0))
edrvReqVariablesFrame.grid(row=3, column=1, pady=10, padx=(0, 10))
edrvPredFrame.grid(row=4, pady=(10, 10), padx=(10, 0))
edrvPredVariablesFrame.grid(row=4, column=1, pady=(10, 15), padx=(0, 10))
dataFrame.grid(row=1)

# Grid Data and Buttons Frame
jupiter.grid(row=4, column=0, pady=(10, 10))
dataButtonsFrame.grid(row=0, column=0)

carregarGif()

# Grid Léo Dançando Frame
label["image"] = im[0]
label.grid(pady=50, padx=20)
leoFrame.grid(row=0, column=1)

menu.mainloop()

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import time
import serial
import threading
from PIL import ImageTk, Image
import serial.tools.list_ports
import pygame
import traceback

from serial.serialutil import SerialException

def pop(text):
    messagebox.showerror("Erro", text)

def send_preCharge():
    if pause:
        
        mensagem = str(6) + '\n'

        if(not ser.isOpen()):
            ser.open()
        ser.write(bytes(mensagem, 'utf-8'))
        ser.close()
    else:
        pop("É necessário pausar o recebimento antes de enviar!")

def send_discharge():
    if pause:
        
        mensagem = str(7) + '\n'

        if(not ser.isOpen()):
            ser.open()
        ser.write(bytes(mensagem, 'utf-8'))
        ser.close()
    else:
        pop("É necessário pausar o recebimento antes de enviar!")

def send_Pt_Edrv_Des_1():
    if pause:
        msg1 = entry1.get()
        msg2 = entry2.get()
        msg3 = entry3.get()
        msg4 = entry4.get()

        if(msg1 == '' or msg2 == '' or msg3 == '' or msg4 == ''):
            pop("Não deixe espaços em branco!")
        else:
            mensagem = str(1) + ' ' + str(msg1) + ' ' + str(msg2) + ' ' + str(msg3) + \
                ' ' + str(msg4) + '\n'

            if(not ser.isOpen()):
                ser.open()
            ser.write(bytes(mensagem, 'utf-8'))
            ser.close()

    else:
        pop("É necessário pausar o recebimento antes de enviar!")

def send_Eem_Edrv_Lim_1():

    if pause:
        msg1 = entry5.get()
        msg2 = entry6.get()
        msg3 = entry7.get()
        msg4 = entry8.get()
        msg5 = entry9.get()
        msg6 = entry10.get()

        if(msg1 == '' or msg2 == '' or msg3 == '' or msg4 == '' or msg5 == '' or msg6 == ''):
            pop("Não deixe espaços em branco!")
        else:
            mensagem = str(2) + ' ' + str(msg1) + ' ' + str(msg2) + ' ' + str(msg3) + \
                ' ' + str(msg4) + ' ' + str(msg5) + ' ' + str(msg6) + '\n'

            if(not ser.isOpen()):
                ser.open()

            ser.write(bytes(mensagem, 'utf-8'))
            ser.close()
    else:
        pop("É necessário pausar o recebimento antes de enviar!")

def send_Eem_Edrv_Pred_1():

    if pause:
        msg1 = entry11.get()
        msg2 = entry12.get()
        msg3 = entry13.get()
        msg4 = entry14.get()

        if(msg1 == '' or msg2 == '' or msg3 == '' or msg4 == ''):
            pop("Não deixe espaços em branco!")
        else:
            mensagem = str(3) + ' ' + str(msg1) + ' ' + str(msg2) + ' ' + str(msg3) + \
                ' ' + str(msg4) + '\n'

            if(not ser.isOpen()):
                ser.open()

            ser.write(bytes(mensagem, 'utf-8'))
            ser.close()
    else:
        pop("É necessário pausar o recebimento antes de enviar!")

def send_Eem_Edrv_Des_1():
    if pause:

        msg1 = entry15.get()
        msg2 = entry16.get()

        if(msg1 == '' or msg2 == ''):
            pop("Não deixe espaços em branco!")
        else:
            mensagem = str(4) + ' ' + str(msg1) + ' ' + str(msg2) + '\n'

            if(not ser.isOpen()):
                ser.open()

            ser.write(bytes(mensagem, 'utf-8'))
            ser.close()
    else:
        pop("É necessário pausar o recebimento antes de enviar!")

def send_Pt_Veh_1():
    if pause:

        msg1 = entry17.get()
        msg2 = entry18.get()
        msg3 = entry19.get()

        if(msg1 == '' or msg2 == '' or msg3 == ''):
            pop("Não deixe espaços em branco!")
        else:
            mensagem = str(5) + ' ' + str(msg1) + ' ' + \
                str(msg2) + ' ' + str(msg3) + '\n'

            if(not ser.isOpen()):
                ser.open()

            ser.write(bytes(mensagem, 'utf-8'))
            ser.close()
    else:
        pop("É necessário pausar o recebimento antes de enviar!")

# Funções


def atualizarPortas():
    global atualizar
    ports = serial.tools.list_ports.comports()
    portaLista["values"] = ports
    atualizar = menu.after(500, atualizarPortas)


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
    if(menu.winfo_width() == 1231):
        print(menu.winfo_width())
        menu.geometry("%dx%d+%d+%d" % (836, 746, 340, 25))
        pygame.mixer.music.stop()

        menu.after_cancel(anim)

    else:
        print(menu.winfo_width())
        menu.geometry("%dx%d+%d+%d" % (1231, 746, 140, 25))
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

    while(True):

        while(not pause):
            try:
                if(not ser.isOpen()):
                    ser.open()
                mensagem = ser.readline()
                lista = mensagem.decode("utf-8").split()
                print(lista)
                atualizarInterface(lista)
                ser.close()
                portaLabel['text'] = "OK!"
                portaLabel['fg'] = "green"
            except IndexError:
                pass
            except:
                traceback.print_exc()
        time.sleep(0.05)

        print("Paused")
        ser.close()

        time.sleep(0.01)


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


def verificar(v):
    try:
        global ser
        entrada = portaLista.get()
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
        portaLabel['text'] = "OK!"
        portaLabel['fg'] = "green"
    except:
        portaLabel['text'] = "Erro!"
        portaLabel['fg'] = "red"
        traceback.print_exc()


# Inicialização Janela Serial
ser = serial.Serial()


# -------------------------------------------------------


# Inicialização Janela

menu = Tk()
menu.title("Jupiter CAN Interface")
menu.geometry("%dx%d+%d+%d" % (836, 746, 340, 25))
# menu.resizable(False, False)

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
comFrame = Frame(buttonsFrame, bg = "black")
dataFrame = Frame(dataButtonsFrame, bd=1, relief=SOLID)

leftFrame = Frame(menu)
sendFrame = Frame(leftFrame)
chargeFrame = Frame(leftFrame)

Pt_Edrv_Des_1_Frame = Frame(sendFrame)
Eem_Edrv_Lim_1_Frame = Frame(sendFrame)
Eem_Edrv_Pred_1_Frame = Frame(sendFrame)

twoFrame = Frame(sendFrame)

Eem_Edrv_Des_1_Frame = Frame(twoFrame)
Pt_Veh_1_Frame = Frame(twoFrame)

# Entrys

label1 = Label(Pt_Edrv_Des_1_Frame, text="Operation Mode Request")
label2 = Label(Pt_Edrv_Des_1_Frame, text="Torque Request")
label3 = Label(Pt_Edrv_Des_1_Frame, text="Minimum Torque")
label4 = Label(Pt_Edrv_Des_1_Frame, text="Speed Request")
label5 = Label(Eem_Edrv_Lim_1_Frame, text="Maximum Allowed Voltage")
label6 = Label(Eem_Edrv_Lim_1_Frame, text="Minimum Allowed Voltage")
label7 = Label(Eem_Edrv_Lim_1_Frame, text="Estimated Battery Resistance")
label8 = Label(Eem_Edrv_Lim_1_Frame, text="Current Calculation Eem")
label9 = Label(Eem_Edrv_Lim_1_Frame, text="Maximum Allowed Current")
label10 = Label(Eem_Edrv_Lim_1_Frame, text="Minimum Allowed Current")
label11 = Label(Eem_Edrv_Pred_1_Frame, text="Predicted Maximum Voltage")
label12 = Label(Eem_Edrv_Pred_1_Frame, text="Predicted Minimum Voltage")
label13 = Label(Eem_Edrv_Pred_1_Frame, text="Predicted Minimum Current")
label14 = Label(Eem_Edrv_Pred_1_Frame, text="Predicted Maximum Current")
label15 = Label(Eem_Edrv_Des_1_Frame, text="Charging Voltage Request")
label16 = Label(Eem_Edrv_Des_1_Frame, text="Battery Relay State")
label17 = Label(Pt_Veh_1_Frame, text="Ignition Switch State")
label18 = Label(Pt_Veh_1_Frame, text="E-Drive Shut-Off Time")
label19 = Label(Pt_Veh_1_Frame, text="Crash Flag")

entry1 = Entry(Pt_Edrv_Des_1_Frame)
entry1.insert(END, "0")
entry2 = Entry(Pt_Edrv_Des_1_Frame)
entry2.insert(END, "0")
entry3 = Entry(Pt_Edrv_Des_1_Frame)
entry3.insert(END, "0")
entry4 = Entry(Pt_Edrv_Des_1_Frame)
entry4.insert(END, "0")
entry5 = Entry(Eem_Edrv_Lim_1_Frame)
entry5.insert(END, "52")
entry6 = Entry(Eem_Edrv_Lim_1_Frame)
entry6.insert(END, "36")
entry7 = Entry(Eem_Edrv_Lim_1_Frame)
entry7.insert(END, "0.02")
entry8 = Entry(Eem_Edrv_Lim_1_Frame)
entry8.insert(END, "0")
entry9 = Entry(Eem_Edrv_Lim_1_Frame)
entry9.insert(END, "2")
entry10 = Entry(Eem_Edrv_Lim_1_Frame)
entry10.insert(END, "0")
entry11 = Entry(Eem_Edrv_Pred_1_Frame)
entry12 = Entry(Eem_Edrv_Pred_1_Frame)
entry13 = Entry(Eem_Edrv_Pred_1_Frame)
entry14 = Entry(Eem_Edrv_Pred_1_Frame)
entry15 = Entry(Eem_Edrv_Des_1_Frame)
entry16 = Entry(Eem_Edrv_Des_1_Frame)
entry17 = Entry(Pt_Veh_1_Frame)
entry17.insert(END, "1")
entry18 = Entry(Pt_Veh_1_Frame)
entry18.insert(END, "0")
entry19 = Entry(Pt_Veh_1_Frame)
entry19.insert(END, "0")

button1 = Button(Pt_Edrv_Des_1_Frame, text="Enviar",
                 command=send_Pt_Edrv_Des_1)
button2 = Button(Eem_Edrv_Lim_1_Frame, text="Enviar",
                 command=send_Eem_Edrv_Lim_1)
button3 = Button(Eem_Edrv_Pred_1_Frame, text="Enviar",
                 command=send_Eem_Edrv_Pred_1)
button4 = Button(Eem_Edrv_Des_1_Frame, text="Enviar",
                 command=send_Eem_Edrv_Des_1)
button5 = Button(Pt_Veh_1_Frame, text="Enviar", command=send_Pt_Veh_1)

prechargeButton = Button(chargeFrame, text = "Pré-Carga", bg="green", font="Arial 15", command= send_preCharge)
dischargeButton = Button(chargeFrame, text = "Descarga", bg="red", font="Arial 15", command=send_discharge)



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

portaLista = ttk.Combobox(comFrame, width=8, state="readonly")
portaLabel = Label(comFrame, text = "", bg = "black")


label = Label(leoFrame, bd=0)


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

# Grid Pt_Edrv_Des_1_Frame
label1.grid()
entry1.grid()
label2.grid()
entry2.grid()
label3.grid()
entry3.grid()
label4.grid()
entry4.grid()
button1.grid(pady=(10, 0))
Pt_Edrv_Des_1_Frame.grid(row=0, column=0, padx=(50, 70))

# Grid Eem_Edrv_Lim_1_Frame
label5.grid()
entry5.grid()
label6.grid()
entry6.grid()
label7.grid()
entry7.grid()
label8.grid()
entry8.grid()
label9.grid()
entry9.grid()
label10.grid()
entry10.grid()
button2.grid(pady=(10, 0))
Eem_Edrv_Lim_1_Frame.grid(row=1, column=0, pady=60, sticky=N)

# Grid Eem_Edrv_Pred_1_Frame

label11.grid()
entry11.grid()
label12.grid()
entry12.grid()
label13.grid()
entry13.grid()
label14.grid()
entry14.grid()
button3.grid(pady=(10, 0))
Eem_Edrv_Pred_1_Frame.grid(row=0, column=1, padx=(0, 50))

# Grid Eem_Edrv_Des_1_Frame
label15.grid()
entry15.grid()
label16.grid()
entry16.grid()
button4.grid(pady=(10, 50))

Eem_Edrv_Des_1_Frame.grid(row=1, column=1)

# Grid Pt_Veh_1_Frame

label17.grid()
entry17.grid()
label18.grid()
entry18.grid()
label19.grid()
entry19.grid()
button5.grid(pady=(10, 0))
Pt_Veh_1_Frame.grid(row=2, column=1)

twoFrame.grid(row=1, column=1, pady=(60, 50), padx=(0, 50), sticky=N)

sendFrame.grid(row=0, column=0)

prechargeButton.grid(row = 0, column=0, padx = (0,40))
dischargeButton.grid(row =0, column=1)
chargeFrame.grid(row = 1, column = 0)

leftFrame.grid()

# Grid Button Frame
initButton.grid(row=0, padx=(0, 0), pady=(15, 10))
pauseButton.grid(row=1, padx=(0, 0), pady=(0, 15))
buttonFrame.grid(row=0)

# Grid Buttons Frame
dangerButton.grid(row=0, column=1,  padx=(10, 10))
portaLista.grid()
portaLabel.grid()
comFrame.grid(row=0, column=2)
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
dataButtonsFrame.grid(row=0, column=1)

carregarGif()
atualizarPortas()
portaLista.bind("<<ComboboxSelected>>", verificar)

# Grid Léo Dançando Frame
label["image"] = im[0]
label.grid(pady=50, padx=20)
leoFrame.grid(row=0, column=2)

menu.mainloop()

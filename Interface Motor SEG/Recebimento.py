from tkinter import *
import time
import serial
import threading
from PIL import ImageTk, Image

from serial.serialutil import SerialException

menu = Tk()

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
im = []

def resize():
    if(menu.winfo_width() == 762):
        print(menu.winfo_width())
        menu.geometry("%dx%d" % (366, 752))
    else:
        print(menu.winfo_width())
        menu.geometry("%dx%d" % (762, 752))


def carregarGif():
    global im
    im = [PhotoImage(file=f"images\ezgif-7-80017838cabb-gif-im\\frame_0{i}_delay-0.02s.png") for i in range(10,100)]

    for i in range (100, 214):
        im.append(PhotoImage(file=f"images\ezgif-7-80017838cabb-gif-im\\frame_{i}_delay-0.02s.png"))

count = 0 
anim = None
def animation(count):
    global anim
    im2 = im[count]

    label.configure(image=im2)
    count += 1
    if count == 200:
        count = 0
    anim = menu.after(50,lambda :animation(count))

def pausar():
    global pause
    pause = not pause
    print(pause)


def finalizar():
    global fim
    fim = True
    menu.after_cancel(anim)

    menu.destroy()


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
            pass
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
    else: operationMode .set(lista[7])  
    
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

# Inicialização Janela

try:
    ser = serial.Serial(
        port='COM5',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )
except SerialException:
    print("Porta não encontrada!")


menu.title("Jupiter CAN Interface")
menu.geometry("%dx%d" % (366, 752))
menu.resizable(False, False)

serialThread = threading.Thread(target=receiveSerial)
serialThread.setDaemon(True)

my_bg = Image.open("D:\Baja\ECI\Git Pessoal\Interface Motor SEG\images\leo.png")
resized = my_bg.resize((348,660), Image.ANTIALIAS)
new_bg = ImageTk.PhotoImage(resized)

leoFrame = Frame(menu, bg="#0b7aa5", bd=3, relief=SOLID)
label = Label (leoFrame, image= new_bg, bd = 0 )

dataButtonsFrame = Frame(menu, bd = 3, relief = SOLID, bg="black")
buttonsFrame = Frame(dataButtonsFrame, bd = 5, relief = SOLID, bg="black")
buttonFrame = Frame(buttonsFrame, bg="black")
dataFrame = Frame(dataButtonsFrame, bd=1, relief=SOLID)

initButton = Button(buttonFrame, text="Iniciar recebimento",command=serialThread.start)
pauseButton = Button(buttonFrame, text = "Pause / Unpause", command = pausar)



# -------------------------------------------------------

edrvActFrame = Frame(dataFrame)

Label(edrvActFrame, text = "Checksum Actual Torque: ", anchor = SW , width =23).grid()
Label(edrvActFrame, text = "Alive counter actual torque: ", anchor = W , width =23).grid()
Label(edrvActFrame, text = "Actual run state: ", anchor = W , width = 23).grid(sticky=W)
Label(edrvActFrame, text = "Actual operation mode: ", anchor = W , width =23).grid()
Label(edrvActFrame, text = "Actual torque: ", anchor = W , width =23).grid()
Label(edrvActFrame, text = "Actual speed: ", anchor = W , width =23).grid()
Label(edrvActFrame, text = "Actual DC voltage: ", anchor = W , width =23).grid()
Label(edrvActFrame, text = "Actual DC current: ", anchor = W , width =23).grid()

EdrvActVariablesFrame = Frame(dataFrame)

Label(EdrvActVariablesFrame, textvariable= checksumActualTorque,  anchor = E, width=17).grid()
Label(EdrvActVariablesFrame, textvariable = aliveCounterActualTorque, anchor = E, width=17).grid()
Label(EdrvActVariablesFrame, textvariable = runState, anchor = E, width=17).grid()
Label(EdrvActVariablesFrame, textvariable = operationMode, anchor = E, width=17).grid()
Label(EdrvActVariablesFrame, textvariable = torque, anchor = E, width=17).grid()
Label(EdrvActVariablesFrame, textvariable = speed, anchor = E, width=17).grid()
Label(EdrvActVariablesFrame, textvariable = voltage, anchor = E, width=17).grid()
Label(EdrvActVariablesFrame, textvariable = current, anchor = E, width=17).grid()

# -------------------------------------------------------


edrvReqFrame = Frame(dataFrame)

Label(edrvReqFrame, text = "Checksum request ", anchor = SW , width =23).grid()
Label(edrvReqFrame, text = "Alive counter request: ", anchor = W , width =23).grid()
Label(edrvReqFrame, text = "Torque Calculation EEM: ", anchor = W , width =23).grid()
Label(edrvReqFrame, text = "Speed Calculation EEM: ", anchor = W , width =23).grid()
Label(edrvReqFrame, text = "Machine Temperature State: ", anchor = W , width =23).grid()
Label(edrvReqFrame, text = "Inverter Temperature State: ", anchor = W , width =23).grid()
Label(edrvReqFrame, text = "Start possible state: ", anchor = W , width =23).grid()
Label(edrvReqFrame, text = "Torque plausibilisation state: ", anchor = W , width =23).grid()

edrvReqVariablesFrame = Frame(dataFrame)

Label(edrvReqVariablesFrame, textvariable= checksumRequest, anchor = E , width = 17).grid()
Label(edrvReqVariablesFrame, textvariable = aliveCounterRequest, anchor = E , width = 17).grid()
Label(edrvReqVariablesFrame, textvariable = torqueCalculation, anchor = E , width = 17).grid()
Label(edrvReqVariablesFrame, textvariable = speedCalculation, anchor = E , width = 17).grid()
Label(edrvReqVariablesFrame, textvariable = machineTemperature, anchor = E , width = 17).grid()
Label(edrvReqVariablesFrame, textvariable = inverterTemperature, anchor = E , width = 17).grid()
Label(edrvReqVariablesFrame, textvariable = startPossible, anchor = E , width = 17).grid()
Label(edrvReqVariablesFrame, textvariable = torquePlausibilisation, anchor = E , width = 17).grid()

# -------------------------------------------------------


edrvPredFrame = Frame(dataFrame)

Label(edrvPredFrame, text = "Checksum available torque: ", anchor = SW , width =23).grid()
Label(edrvPredFrame, text = "Alive counter available torque: ", anchor = W , width =23).grid()
Label(edrvPredFrame, text = "Maximum limited torque: ", anchor = W , width =23).grid()
Label(edrvPredFrame, text = "Maximum available torque: ", anchor = W , width =23).grid()
Label(edrvPredFrame, text = "Minimum limited torque: ", anchor = W , width =23).grid()
Label(edrvPredFrame, text = "Minimum available torque: ", anchor = W , width =23).grid()
Label(edrvPredFrame, text = "Actual derating state: ", anchor = W , width =23).grid()

edrvPredVariablesFrame = Frame(dataFrame)

Label(edrvPredVariablesFrame, textvariable=checksumAvailableTorque, anchor = E , width = 17).grid()
Label(edrvPredVariablesFrame, textvariable = aliveCounterAvailableTorque, anchor = E , width = 17).grid()
Label(edrvPredVariablesFrame, textvariable = maximumLimitedTorque, anchor = E , width = 17).grid()
Label(edrvPredVariablesFrame, textvariable = maximumAvailableTorque, anchor = E , width = 17).grid()
Label(edrvPredVariablesFrame, textvariable = minimumLimitedTorque, anchor = E , width = 17).grid()
Label(edrvPredVariablesFrame, textvariable = minimumAvailableTorque, anchor = E , width = 17).grid()
Label(edrvPredVariablesFrame, textvariable = actualDeratingState, anchor = E , width = 17).grid()

# -------------------------------------------------------

initButton.grid(row = 0, padx = (30,0), pady=(15,10))
pauseButton.grid(row = 1, padx = (30,0), pady=(0,15))

buttonFrame.grid(row=0)

my_bot= Image.open("images\\botao.png")
resized = my_bot.resize((100,100), Image.ANTIALIAS)
new_bot = ImageTk.PhotoImage(resized)
dangerButton = Button(buttonsFrame, image=new_bot, bd = 0, command = resize, bg = "black", activebackground="black")

dangerButton.grid(row = 0,column=1,  padx = (40,20))

buttonsFrame.grid()

edrvActFrame.grid(row = 2, pady = (10,10), padx=(10,0))
EdrvActVariablesFrame.grid(row = 2, column=1, pady = (10,10), padx=(0,10))
edrvReqFrame.grid(row = 3, pady=10, padx=(10,0))
edrvReqVariablesFrame.grid(row = 3, column=1, pady=10, padx=(0,10))
edrvPredFrame.grid(row = 4, pady=(10,10), padx=(10,0))
edrvPredVariablesFrame.grid(row = 4, column=1, pady=(10,15), padx=(0,10))
buttonFrame.grid(row = 0)

dataFrame.grid(row = 1)


my_jup = Image.open("images\jUPITER_vetorizado.png")
resized = my_jup.resize((230,40), Image.ANTIALIAS)
new_jup = ImageTk.PhotoImage(resized)

jupiter = Label (dataButtonsFrame, image= new_jup, bg="black", width=354, height=60)
jupiter.grid(row = 4, column=0, pady = (10, 10))






label.grid( pady = 53, padx = 20)
leoFrame.grid(row = 0, column = 1)

carregarGif()
animation(count)



dataButtonsFrame.grid(row = 0, column=0)

menu.mainloop()

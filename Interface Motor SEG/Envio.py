from tkinter import *
from tkinter import ttk
import serial
import sys

# Funções


def configuraEntrys(v):
    entrada = lista.get()
    space1.pack_forget()
    enviarButton.pack_forget()
    globals()[entrada + "_setLabels"]()
    space1.pack()
    enviarButton.pack()


def Pt_Edrv_Des_1_setLabels():  

    stringlbl1.set("Operation Mode Request")
    label1.pack()
    entry1.pack()

    stringlbl2.set("Torque Request")
    label2.pack()
    entry2.pack()

    stringlbl3.set("Minimun Torque")
    label3.pack()
    entry3.pack()
    
    stringlbl4.set("Speed Request")
    label4.pack()
    entry4.pack()

    label5.pack_forget()
    entry5.pack_forget()
    label6.pack_forget()
    entry6.pack_forget()

    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry4.delete(0, END)
    entry5.delete(0, END)
    entry6.delete(0, END)

def Eem_Edrv_Lim_1_setLabels():
    stringlbl1.set("Maximum Allowed Voltage")
    label1.pack()
    entry1.pack()

    stringlbl2.set("Minimum Allowed Voltage")
    label2.pack()
    entry2.pack()

    stringlbl3.set("Estimated Battery Resistance")
    label3.pack()
    entry3.pack()

    stringlbl4.set("Current Calculation EEM")
    label4.pack()
    entry4.pack()

    stringlbl5.set("Maximum Allowed Current")
    label5.pack()
    entry5.pack()

    stringlbl6.set("Minimum Allowed Current")
    label6.pack()
    entry6.pack()

    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry4.delete(0, END)
    entry5.delete(0, END)
    entry6.delete(0, END)

def Eem_Edrv_Pred_1_setLabels():
    stringlbl1.set("Predicted Maximum Voltage")
    label1.pack()
    entry1.pack()

    stringlbl2.set("Predicted Minimum Voltage")
    label2.pack()
    entry2.pack()

    stringlbl3.set("Predicted Minimum Current")
    label3.pack()
    entry3.pack()

    stringlbl4.set("Predicted Maximum Current")
    label4.pack()
    entry4.pack()

    label5.pack_forget()
    entry5.pack_forget()
    label6.pack_forget()
    entry6.pack_forget()

    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry4.delete(0, END)
    entry5.delete(0, END)
    entry6.delete(0, END)

def Eem_Edrv_Des_1_setLabels():
    stringlbl1.set("Charging Voltage Request")
    label1.pack()
    entry1.pack()

    stringlbl2.set("Battery Relay State")
    label2.pack()
    entry2.pack()

    label3.pack_forget()
    entry3.pack_forget()
    label4.pack_forget()
    entry4.pack_forget()
    label5.pack_forget()
    entry5.pack_forget()
    label6.pack_forget()
    entry6.pack_forget()

    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry4.delete(0, END)
    entry5.delete(0, END)
    entry6.delete(0, END)

def Pt_Veh_1_setLabels():
    stringlbl1.set("Ignition Switch State")
    label1.pack()
    entry1.pack()

    stringlbl2.set("E-Drive Shut-Off Time")
    label2.pack()
    entry2.pack()

    stringlbl3.set("Crash Flag")
    label3.pack()
    entry3.pack()

    label4.pack_forget()
    entry4.pack_forget()
    label5.pack_forget()
    entry5.pack_forget()
    label6.pack_forget()
    entry6.pack_forget()

    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry4.delete(0, END)
    entry5.delete(0, END)
    entry6.delete(0, END)

def Pt_Obd_2_setLabels():
    stringlbl1.set("Time Since Engine Started")
    label1.pack()
    entry1.pack()

    label2.pack_forget()
    entry2.pack_forget()
    label3.pack_forget()
    entry3.pack_forget()
    label4.pack_forget()
    entry4.pack_forget()
    label5.pack_forget()
    entry5.pack_forget()
    label6.pack_forget()
    entry6.pack_forget()

    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry4.delete(0, END)
    entry5.delete(0, END)
    entry6.delete(0, END)





def sendSerial():

    entrada = lista.get()
    i = 0
    for msg in valores:
        if(entrada == msg):
            msgIndex = i
            break
        i += 1

    msg1= entry1.get()
    msg2 = entry2.get()
    msg3 = entry3.get()
    msg4 = entry4.get()
    msg5 = entry5.get()
    msg6 = entry6.get()

    mensagem = str(msgIndex) + ' ' + str(msg1) + ' ' + str(msg2) + ' ' + str(msg3) + \
        ' ' + str(msg4) + ' ' + str(msg5) + ' ' + str(msg6) + '\n'
    if(not ser.isOpen()):
        ser.open()
    ser.write(bytes(mensagem, 'utf-8'))
    ser.close()
    


# Inicialização Janela

ser = serial.Serial(
    port='COM5',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

ser.close()

menu = Tk()
menu.title("Jupiter CAN Interface")
menu.geometry("%dx%d" % (300 , 380))


# Inicialização Widgets
valores = ["Pt_Edrv_Des_1",
           "Eem_Edrv_Lim_1",
           "Eem_Edrv_Pred_1",
           "Eem_Edrv_Des_1",
           "Pt_Veh_1",
           "Pt_Obd_2"]

stringlbl1 = StringVar()
stringlbl2 = StringVar()
stringlbl3 = StringVar()
stringlbl4 = StringVar()
stringlbl5 = StringVar()
stringlbl6 = StringVar()

label0 = Label(menu, text="Mensagem:")
space = Label(menu)
space1 = Label(menu)

label1 = Label(menu, textvariable=stringlbl1)
label2 = Label(menu, textvariable=stringlbl2)
label3 = Label(menu, textvariable=stringlbl3)
label4 = Label(menu, textvariable=stringlbl4)
label5 = Label(menu, textvariable=stringlbl5)
label6 = Label(menu, textvariable=stringlbl6)

entry1 = Entry(menu)
entry2 = Entry(menu)
entry3 = Entry(menu)
entry4 = Entry(menu)
entry5 = Entry(menu)
entry6 = Entry(menu)

lista = ttk.Combobox(menu, state="readonly", values=valores)

enviarButton = Button(text="Enviar", command=sendSerial)

# Pack
label0.pack()
lista.pack()
space.pack()
lista.bind("<<ComboboxSelected>>", configuraEntrys)

menu.mainloop()

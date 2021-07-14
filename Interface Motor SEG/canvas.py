import tkinter as tk
from PIL import Image

root = tk.Tk()
# creating list of PhotoImage objects for each frames

im = [tk.PhotoImage(file=f"images\ezgif-7-80017838cabb-gif-im\\frame_0{i}_delay-0.02s.png") for i in range(10,100)]

for i in range (100, 214):
    im.append(tk.PhotoImage(file=f"images\ezgif-7-80017838cabb-gif-im\\frame_{i}_delay-0.02s.png"))

count = 0
anim = None
def animation(count):
    global anim
    im2 = im[count]

    gif_label.configure(image=im2)
    count += 1
    if count == 200:
        count = 0
    anim = root.after(50,lambda :animation(count))

def stop_animation():
    root.after_cancel(anim)

gif_label = tk.Label(root,image="")
gif_label.pack()

start = tk.Button(root,text="start",command=lambda :animation(count))
start.pack()

stop = tk.Button(root,text="stop",command=stop_animation)
stop.pack()

root.mainloop()
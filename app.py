import tkinter as tk
from tkinter import ttk
from video_start import Start_Video
# root window
root = tk.Tk()
root.geometry('300x200')
root.resizable(False, False)
root.title('Button Demo')

start = Start_Video()


def get_start():
    start.main()

def reset():
    start.reset()
# exit button
start_button = ttk.Button(
    root,
    text='Start',
    command=lambda: get_start()
)

start_button.pack(
    ipadx=5,
    ipady=5,
    expand=True
)

reset_button = ttk.Button(
    root,
    text='Reset',
    command=lambda: reset()
)

reset_button.pack(
    ipadx=5,
    ipady=5,
    expand=True
)
root.mainloop()
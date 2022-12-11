import tkinter
from tkinter import *


def on_closing():
    global running
    running = False


def on_selected():
    selection = "You selected the option " + str(click_mode_var.get())


def on_start():
    start["state"] = "disabled"
    end["state"] = "normal"
    switch["state"] = "disabled"
    click_mode_voice_btn["state"] = "disabled"
    click_mode_time_btn["state"] = "disabled"


def on_end():
    start["state"] = "normal"
    end["state"] = "disabled"
    switch["state"] = "normal"
    click_mode_voice_btn["state"] = "normal"
    click_mode_time_btn["state"] = "normal"


bg_color = '#BC639B'
fg_color = 'white'

root = tkinter.Tk()
# root.protocol("WM_DELETE_WINDOW", on_closing)
root.resizable(False, False)
root.title("Hands Free Mouse")
root.geometry("800x400+500+100")
canvas = Canvas(root, bg="#4392F1", height=400, width=800,
                bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)
background_img = PhotoImage(file=f"assets/background.png")
background = canvas.create_image(400.0, 200.0, image=background_img)
header = canvas.create_text(400.0, 91.0, text="Hands Free Mouse",
                            fill="#ECE8EF", font=("Roboto-Bold", int(30.0)))
create_label = canvas.create_text(
    203.5, 174.5, text="Sensibilidade", fill="#ECE8EF", font=("Roboto-Bold", int(16.0)))
switch = tkinter.Scale(from_=0, to=100, orient=tkinter.HORIZONTAL, length=200, activebackground=bg_color, bg=bg_color, highlightcolor=bg_color, highlightbackground=bg_color, fg=fg_color,
                       troughcolor=fg_color)
switch.set(50)

click_mode_label = canvas.create_text(
    203.5, 255.5, text="Comando de clique", fill="#ECE8EF", font=("Roboto-Bold", int(16.0)))

click_mode_var = IntVar()
click_mode_var.set(1)

click_mode_voice_btn = Radiobutton(root, text="Por voz", variable=click_mode_var, value=1,
                                   command=on_selected, activebackground=bg_color, bg=bg_color, highlightcolor=bg_color, highlightbackground=bg_color, fg=fg_color, selectcolor=bg_color, font=("Roboto-Bold", int(12.0)))

click_mode_time_btn = Radiobutton(root, text="Por tempo", variable=click_mode_var, value=2,
                                  command=on_selected, activebackground=bg_color, bg=bg_color, highlightcolor=bg_color, highlightbackground=bg_color, fg=fg_color, selectcolor=bg_color, font=("Roboto-Bold", int(12.0)))

menubar = Menu(root)
about = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Sobre", menu=about)

start_img = PhotoImage(file=f"assets/start.png")
start = Button(image=start_img, borderwidth=0,
               highlightthickness=0, relief="flat", command=on_start)

end_img = PhotoImage(file=f"assets/end.png")
end = Button(image=end_img, borderwidth=0, highlightthickness=0,
             relief="flat", command=on_end)
end["state"] = "disabled"

switch.place(x=400, y=176, anchor=tkinter.CENTER)
start.place(x=218, y=310, width=172, height=58)
end.place(x=418, y=310, width=172, height=58)
click_mode_voice_btn.place(x=400, y=245.5, anchor=tkinter.CENTER)
click_mode_time_btn.place(x=400, y=280.5, anchor=tkinter.CENTER)
root.config(menu=menubar)

root.mainloop()

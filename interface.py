import os
import threading
import tkinter
from tkinter import *
import clique_tempo, clique_voz
import subprocess

VOZ = 1
TEMPO = 2

# def on_closing():
#     global running
#     running = False

bg_color = '#BC639B'
fg_color = 'white'

voz_proc = None
tempo_proc = None

class App(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def on_selected(self):
        selection = "You selected the option " + str(self.click_mode_var.get())

    def on_start(self):
        global voz_proc, tempo_proc
        self.start_btn["state"] = "disabled"
        self.end["state"] = "normal"
        self.switch["state"] = "disabled"
        self.click_mode_voice_btn["state"] = "disabled"
        self.click_mode_time_btn["state"] = "disabled"

        if self.click_mode_var.get() == VOZ:
            # clique_tempo.running = False
            # clique_voz.running = True
            # clique_voz.activate()
            # self.root.after(0, clique_voz.ouvir_microfone(self.root))
            voz_proc = subprocess.Popen('python clique_voz.py')
            print(voz_proc)


        if self.click_mode_var.get() == TEMPO:
            # clique_voz.running = False
            # clique_tempo.running = True
            # cliquetempo = clique_tempo.CliqueTempo()
            # cliquetempo.activate()
            # self.root.after(0, clique_tempo.wait_for_movement(self.root))
            tempo_proc = subprocess.Popen('python clique_tempo.py')

    def on_end(self):
        global voz_proc, tempo_proc
        self.start_btn["state"] = "normal"
        self.end["state"] = "disabled"
        self.switch["state"] = "normal"
        self.click_mode_voice_btn["state"] = "normal"
        self.click_mode_time_btn["state"] = "normal"

        clique_tempo.running = False
        clique_voz.running = False
        print(voz_proc)
        if voz_proc: 
            print(voz_proc)
            voz_proc.kill()
            
        print(tempo_proc)
        if tempo_proc: 
            print(tempo_proc)
            tempo_proc.kill()
        # os.system('taskkill -f -im clique_tempo')
        # os.system('taskkill -f -im clique_voz')

    def run(self):
        self.root = tkinter.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.resizable(False, False)
        self.root.title("Hands Free Mouse")
        self.root.geometry("800x400+500+100")
        self.canvas = Canvas(self.root, bg="#4392F1", height=400, width=800,
                        bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)
        self.background_img = PhotoImage(file=f"assets/background.png")
        self.background = self.canvas.create_image(400.0, 200.0, image=self.background_img)
        self.header = self.canvas.create_text(400.0, 91.0, text="Hands Free Mouse",
                                    fill="#ECE8EF", font=("Roboto-Bold", int(30.0)))
        self.create_label = self.canvas.create_text(
            203.5, 174.5, text="Sensibilidade", fill="#ECE8EF", font=("Roboto-Bold", int(16.0)))
        self.switch = tkinter.Scale(from_=0, to=100, orient=tkinter.HORIZONTAL, length=200, activebackground=bg_color, bg=bg_color, highlightcolor=bg_color, highlightbackground=bg_color, fg=fg_color,
                            troughcolor=fg_color)
        self.switch.set(50)

        self.click_mode_label = self.canvas.create_text(
            203.5, 255.5, text="Comando de clique", fill="#ECE8EF", font=("Roboto-Bold", int(16.0)))

        self.click_mode_var = IntVar()
        self.click_mode_var.set(VOZ)

        self.click_mode_voice_btn = Radiobutton(self.root, text="Por voz", variable=self.click_mode_var, value=VOZ,
                                        command=self.on_selected, activebackground=bg_color, bg=bg_color, highlightcolor=bg_color, highlightbackground=bg_color, fg=fg_color, selectcolor=bg_color, font=("Roboto-Bold", int(12.0)))

        self.click_mode_time_btn = Radiobutton(self.root, text="Por tempo", variable=self.click_mode_var, value=TEMPO,
                                        command=self.on_selected, activebackground=bg_color, bg=bg_color, highlightcolor=bg_color, highlightbackground=bg_color, fg=fg_color, selectcolor=bg_color, font=("Roboto-Bold", int(12.0)))

        self.menubar = Menu(self.root)
        self.about = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Sobre", menu=self.about)

        self.start_img = PhotoImage(file=f"assets/start.png")
        self.start_btn = Button(image=self.start_img, borderwidth=0,
                    highlightthickness=0, relief="flat", command=self.on_start)

        self.end_img = PhotoImage(file=f"assets/end.png")
        self.end = Button(image=self.end_img, borderwidth=0, highlightthickness=0,
                    relief="flat", command=self.on_end)
        self.end["state"] = "disabled"

        self.switch.place(x=400, y=176, anchor=tkinter.CENTER)
        self.start_btn.place(x=218, y=310, width=172, height=58)
        self.end.place(x=418, y=310, width=172, height=58)
        self.click_mode_voice_btn.place(x=400, y=245.5, anchor=tkinter.CENTER)
        self.click_mode_time_btn.place(x=400, y=280.5, anchor=tkinter.CENTER)
        self.root.config(menu=self.menubar)

        self.root.mainloop()
        del self.root

app = App()

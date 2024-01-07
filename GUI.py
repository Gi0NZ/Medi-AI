import os
from tkinter import *

import timer

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

BG_COLOR = "#17202A"
BG_GRAY = "#ABB2B9"
TEXT_COLOR = "#EAECEE"


class ChatApplication:

    def __init__(self):
        self.window = Tk()
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("Chat")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg=BG_COLOR)

        # head label
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR, text="Medi-AI", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        # tiny divider
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        # text widget
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, padx=5,
                                pady=5)  # per ogni test immessi, mostriamo 20 caratteri in una linea(width=20)
        # mettiamo self perché ci serve dopo in un'altra funzione, mentre head_label ecc non ci servono, perciò non mettiamo self.nome (instance variable)                                                                                                                # e usiamo 2 linee (height=2) e diamo un pò di padding intorno( padx e pady)

        self.text_widget.place(relheight=0.745, relwidth=1,
                               rely=0.08)  # 0.745 quasi il 75 per cento è occuipato dal widget
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        # scrollbar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)

        # bottom label
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        # message entry box
        self.msg_entry = Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        # send button
        send_button = Button(bottom_label, text="Invia", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self.insert_message(msg, "You")

    def insert_message(self, msg, sender):
        if not msg:
            return  # nel caso premiamo invio senza scrivere messaggio
        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(cursor="arrow", state=DISABLED)
    def function(self):












from tkinter import *
from tkinter import messagebox
import pandas
from random import choice
import os

BACKGROUND_COLOR = "#B1DDC6"
CARD_FRONT = "images/card_front.png"
CARD_BACK = "images/card_back.png"
TICK_RIGHT = "images/right.png"
TICK_WRONG = "images/wrong.png"
FONT = "Ariel"

# setup window
window = Tk()
window.title("Flash cards")
window.minsize(width=900, height=800)
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# setup parameters setup
card_front_image = PhotoImage(file=CARD_FRONT)
card_back_image = PhotoImage(file=CARD_BACK)
right_image = PhotoImage(file=TICK_RIGHT)
wrong_image = PhotoImage(file=TICK_WRONG)
words = []
words_to_learn = []
word = ''
translation_id = 0
title_id = 0

def next_word():
    global word
    if len(words) == 0:
        messagebox.showinfo(title="No More words", message="There are no more words to learn")
        return

    canvas.itemconfig(canvas_image, image=card_front_image)
    canvas.itemconfig(title_id, text="French")
    word = choice(words)
    canvas.itemconfig(translation_id, text=word['French'])
    words.remove(word)
    timer = window.after(3000, translate_word)


def right_answer():
    next_word()


def wrong_answer():
    global words_to_learn
    words_to_learn.append(word)
    next_word()
    words_to_learn_csv = pandas.DataFrame.from_dict(words_to_learn)
    words_to_learn_csv.to_csv("data/words_to_learn.csv", index=False)

def translate_word():
    window.after_cancel(timer)
    canvas.itemconfig(canvas_image, image=card_back_image)
    canvas.itemconfig(title_id, text="English")
    canvas.itemconfig(translation_id, text=word['English'])



# setup canvas
canvas = Canvas(width=800, height=526, highlightthickness=0)
canvas_image = canvas.create_image(400, 263, image=card_front_image)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
title_id = canvas.create_text(400, 150, text="French", font=(FONT, 40, "italic"))
translation_id = canvas.create_text(400, 263, text="", font=(FONT, 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

#setup buttons
wrong_button = Button(image=wrong_image, highlightthickness=0, command=wrong_answer)
wrong_button.grid(column=0, row=1)

right_button = Button(image=right_image, highlightthickness=0, command=right_answer)
right_button.grid(column=1, row=1)

try:
    data = pandas.read_csv('data/words_to_learn.csv')
    words = data.to_dict(orient="records")
    os.remove('data/words_to_learn.csv')
except FileNotFoundError:
    data = pandas.read_csv('data/french_words.csv')
    words = data.to_dict(orient="records")

next_word()
timer = window.after(3000, translate_word)


window.mainloop()

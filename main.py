import random
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"
FOREIGN_LANGUAGE = "German"
NATIVE_LANGUAGE = "English"
FOREIGN_LANGUAGE_FONT = ("Arial", 40, "italic")
FOREIGN_NEXT_WORD_FONT = ("Arial", 60, "bold")
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/german_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfigure(card_img, image=card_front_img)
    canvas.itemconfigure(card_title, text=FOREIGN_LANGUAGE, fill="black")
    canvas.itemconfigure(card_word, text=current_card["German"], fill="black")
    flip_timer = window.after(3000, flip_card)


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


def flip_card():
    canvas.itemconfigure(card_img, image=card_back_img)
    canvas.itemconfigure(card_title, text=NATIVE_LANGUAGE, fill="white")
    canvas.itemconfigure(card_word, text=current_card["English"], fill="white")


window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title("Flashy")

flip_timer = window.after(3000, flip_card)

card_back_img = PhotoImage(file="images/card_back.png")
card_front_img = PhotoImage(file="images/card_front.png")
right_img = PhotoImage(file="images/right.png")
wrong_img = PhotoImage(file="images/wrong.png")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

card_img = canvas.create_image(400, 263, image=card_front_img)
canvas.grid(column=0, row=0, columnspan=2)
card_title = canvas.create_text(400, 150, text=FOREIGN_LANGUAGE, font=FOREIGN_LANGUAGE_FONT)
card_word = canvas.create_text(400, 263, text="", font=FOREIGN_NEXT_WORD_FONT)

wrong_button = Button(image=wrong_img, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)

right_button = Button(image=right_img, highlightthickness=0, command=is_known)
right_button.grid(column=1, row=1)

next_card()

window.mainloop()

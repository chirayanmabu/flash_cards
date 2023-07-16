from tkinter import *
from tkinter import messagebox
import pandas
import random
import os

BACKGROUND_COLOR = "#B1DDC6"

# read csv
try:
    df = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    df = pandas.read_csv("./data/french_words.csv")
    words_list = df.to_dict(orient="records")
else:
    # list that has multiple dictionaries
    words_list = df.to_dict(orient="records")
finally:
    # empty dictionary that stores individual words from words_list
    gen_word = {}


def change_text():  # Replaces currently displayed word with a different word
    global gen_word, change_timer
    window.after_cancel(change_timer)  # resetting the timer
    gen_word = random.choice(words_list)
    print(len(words_list))
    print(gen_word)

    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(body_text, text=gen_word["French"], fill="black")
    canvas.itemconfig(canvas_image, image=card_front_image)

    change_timer = window.after(3000, change_bg)


def known_word():
    global words_list
    if len(words_list) > 1:
        # removing the known words from the main list that contains all the words
        words_list.remove(gen_word)
        # converting the unknown words to csv again
        new_learn_df = pandas.DataFrame(words_list)
        new_learn_df.to_csv("./data/words_to_learn.csv", index=False)

        change_text()

    else:
        messagebox.showinfo(title="Finished!", message="Well done, you have memorized all of the words!")
        # removes the saved progress
        os.remove("./data/words_to_learn.csv")


def change_bg():  # changes the French words with its English translation
    canvas.itemconfig(canvas_image, image=card_back_image)
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(body_text, text=gen_word["English"], fill="white")


# ---------------------------- UI SETUP ------------------------------- #
# window
window = Tk()
window.title("Flashcard")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# calling change_bg after 3 seconds
change_timer = window.after(3000, change_bg)

# creating canvas to contain the texts and images
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, borderwidth=0, highlightthickness=0)
card_front_image = PhotoImage(file="./images/card_front.png")
card_back_image = PhotoImage(file="./images/card_back.png")

# creating background image that has title text and body text on top
canvas_image = canvas.create_image(403, 266, image=card_front_image)

# title text
title_text = canvas.create_text(400, 150, text="French", fill="black", font=("Ariel", 40, "italic"))

# body text
body_text = canvas.create_text(400, 263, text="", fill="black", font=("Ariel", 60, "bold"))

# inserting a random French word in the body text
canvas.grid(column=0, row=0, columnspan=2)

# wrong button
wrong_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_image, height=95, width=95, highlightthickness=0, bd=0, command=change_text)
wrong_button.grid(column=0, row=1)

# right button
right_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_image, height=95, width=95, highlightthickness=0, bd=0, command=known_word)
right_button.grid(column=1, row=1)

change_text()

window.mainloop()

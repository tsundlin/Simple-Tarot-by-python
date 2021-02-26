__author__ = "tsundlin"

# based on python 3.7.9

import random
import time
import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image
from PIL import ImageTk

CARD_HEIGHT = 91
CARD_WIDTH = 69

#  list<card_name: str>
from_deck_list = []
# card_name : (image,back_image)
from_deck = {}
# card_name : (image,back_image)
res_deck = {}
# card_name : tk.Label()
cards_to_views = {}
# card_name : ["normal" or "upside_down", "un_flip" or "flip"]
cards_to_state = {}


def get_card_image(name: str):
    # (随机正反的牌面, 牌背)
    if random.choice("ab") == "a":
        from_deck[name] = (
            ImageTk.PhotoImage(Image.open('decks\\' + name).resize((CARD_WIDTH, CARD_HEIGHT))), ImageTk.PhotoImage(
                Image.open('decks\\' + 'card_back.png').resize((CARD_WIDTH, CARD_HEIGHT))))
        cards_to_state[name] = ["normal", "un_flip"]
    else:
        from_deck[name] = (
            ImageTk.PhotoImage(Image.open('decks\\' + name).rotate(180).resize((CARD_WIDTH, CARD_HEIGHT))),
            ImageTk.PhotoImage(
                Image.open('decks\\' + 'card_back.png').resize((CARD_WIDTH, CARD_HEIGHT))))
        cards_to_state[name] = ["upside_down", "un_flip"]

    # from_deck[name] = (
    #     ImageTk.PhotoImage(Image.open('decks\\' + name).resize((CARD_WIDTH, CARD_HEIGHT))) if random.choice(
    #         "ab") == "a" else ImageTk.PhotoImage(
    #         Image.open('decks\\' + name).rotate(180).resize((CARD_WIDTH, CARD_HEIGHT))),
    #     ImageTk.PhotoImage(
    #         Image.open('decks\\' + 'card_back.png').resize((CARD_WIDTH, CARD_HEIGHT))))


def load_all_the_cards():
    dirs = os.listdir("decks")
    for name in dirs:
        if name != "card_back.png":
            from_deck_list.append(name)
            get_card_image(name)


def display_the_cards(master):
    # 13*6
    row = 0
    column = 0
    res = tk.Label(master, bg="grey")
    res.grid(row=8, column=4, columnspan=5)
    action = lambda x, y: (lambda p: click(x, y))

    shuffle()

    for card_name in from_deck_list:
        cards_to_views[card_name] = tk.Label(master, image=from_deck.get(card_name)[1])
        cards_to_views[card_name].grid(row=row, column=column, padx=5, pady=5)
        cards_to_views[card_name].bind('<Button-1>', action(card_name, res))
        column += 1
        if column > 12:
            row += 1
            column = 0


def click(card_name, master):
    action = lambda x, y: (lambda p: click(x, y))
    if card_name in res_deck and len(res_deck) >= 5 and cards_to_state[card_name][1] == "un_flip":
        # flip
        cards_to_views[card_name].config(image=res_deck[card_name][0])
        cards_to_state[card_name][1] = "flip"
        # explain

        explain_label = tk.Label(master, text=card_name[:-4] + "\n" + cards_to_state[card_name][0], bg="blue")
        explain_label.pack()
    elif card_name in res_deck:
        pass
    elif card_name in from_deck and len(res_deck) < 5:
        # update gui
        cards_to_views[card_name].destroy()
        cards_to_views[card_name] = tk.Label(master, image=from_deck.get(card_name)[1])
        cards_to_views[card_name].pack(side=tk.LEFT, padx=5, pady=5)
        cards_to_views[card_name].bind('<Button-1>', action(card_name, master))
        # trance_card
        res_deck[card_name] = from_deck[card_name]
        from_deck_list.remove(card_name)

        if len(res_deck) == 5:
            for card_name in from_deck:
                if card_name not in res_deck:
                    cards_to_views[card_name].destroy()
                    time.sleep(0.01)
                    master.update()

    else:
        pass


def shuffle():
    random.shuffle(from_deck_list)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Lin's tarot")
    load_all_the_cards()
    display_the_cards(root)
    root.minsize(root.winfo_width(), root.winfo_height())
    root.mainloop()

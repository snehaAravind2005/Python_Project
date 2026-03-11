#Design and implement a GUI-based Card Matching Game using Python .
#Cards are arranged in a rectangular grid with their faces hidden. The player
#selects two cards at a time. If the selected cards match, they remain face
#up; otherwise, they are turned face down again.

import tkinter as tk      # Import Tkinter for GUI
import random             # Import random to shuffle cards
import time               # Import time to create timer

# -------- GAME SETTINGS --------
ROWS = 4                  # Number of rows
COLS = 4                  # Number of columns
TOTAL = ROWS * COLS       # Total cards

# -------- MAIN WINDOW --------
root = tk.Tk()            # Create window
root.title("Card Matching Game")   # Window title
root.geometry("360x450")  # Window size

# -------- VARIABLES --------
first = None              # Store first clicked card
second = None             # Store second clicked card
lock = False              # Prevent clicking while checking
matched = 0               # Count matched cards
moves = 0                 # Count moves
start_time = None         # Start time for timer

# -------- CARD VALUES --------
values = list(range(1, TOTAL//2 + 1)) * 2   # Create card pairs
random.shuffle(values)    # Shuffle cards

buttons = {}              # Store buttons
card_values = {}          # Store card values

# -------- TIMER FUNCTION --------
def update_timer():

    if matched != TOTAL:                      # Run timer until game ends
        elapsed = int(time.time() - start_time)  # Calculate time
        timer_label.config(text=f"Time: {elapsed}s")  # Update label
        root.after(1000, update_timer)       # Update every second

# -------- CARD FLIP ANIMATION --------
def flip_animation(btn, value):

    btn.config(text="")        # Hide text
    root.update()              # Refresh window

    root.after(80, lambda: btn.config(text="●"))   # Show dot briefly
    root.after(160, lambda: btn.config(text=""))   # Hide again
    root.after(240, lambda: btn.config(text=value)) # Show card number

# -------- CARD CLICK FUNCTION --------
def card_click(pos):

    global first, second, lock, moves, start_time

    if start_time is None:           # Start timer on first click
        start_time = time.time()
        update_timer()

    if lock:                         # Prevent clicking while checking
        return

    btn = buttons[pos]               # Get button

    if btn["text"] != "":            # If card already open
        return

    flip_animation(btn, card_values[pos])  # Show card

    if first is None:                # First card selection
        first = pos

    else:                            # Second card selection
        second = pos
        moves += 1                   # Increase moves
        moves_label.config(text=f"Moves: {moves}")
        lock = True
        root.after(600, check_match) # Check match after delay

# -------- MATCH CHECK FUNCTION --------
def check_match():

    global first, second, lock, matched

    if card_values[first] == card_values[second]:   # If cards match

        buttons[first].config(bg="lightgreen")      # Change color
        buttons[second].config(bg="lightgreen")

        matched += 2                                # Increase matched count

        status.config(text="Two cards matched!")    # Show message

        if matched == TOTAL:                        # If game finished
            elapsed = int(time.time() - start_time)
            status.config(text=f"You Win! Moves: {moves}  Time: {elapsed}s")

    else:                                           # If cards don't match

        status.config(text="Oops! Try again")

        buttons[first].config(text="", bg="SystemButtonFace")
        buttons[second].config(text="", bg="SystemButtonFace")

    first = None
    second = None
    lock = False

# -------- RESTART FUNCTION --------
def restart():

    global values, first, second, matched, moves, start_time, lock

    values = list(range(1, TOTAL//2 + 1)) * 2
    random.shuffle(values)

    first = None
    second = None
    matched = 0
    moves = 0
    start_time = None
    lock = False

    moves_label.config(text="Moves: 0")
    timer_label.config(text="Time: 0s")
    status.config(text="Find matching cards")

    for i in range(TOTAL):
        buttons[i].config(text="", bg="SystemButtonFace")
        card_values[i] = values[i]

# -------- UI DESIGN --------
top = tk.Frame(root)
top.pack(pady=5)

moves_label = tk.Label(top, text="Moves: 0", font=("Arial", 12))
moves_label.pack(side="left", padx=15)

timer_label = tk.Label(top, text="Time: 0s", font=("Arial", 12))
timer_label.pack(side="right", padx=15)

frame = tk.Frame(root)
frame.pack()

index = 0

for r in range(ROWS):
    for c in range(COLS):

        btn = tk.Button(
            frame,
            text="",
            width=6,
            height=3,
            font=("Arial", 16, "bold"),
            command=lambda p=index: card_click(p)
        )

        btn.grid(row=r, column=c, padx=5, pady=5)

        buttons[index] = btn
        card_values[index] = values[index]

        index += 1

status = tk.Label(root, text="Find matching cards", font=("Arial", 12))
status.pack(pady=5)

restart_btn = tk.Button(root, text="Restart Game", bg="orange", command=restart)
restart_btn.pack(pady=10)

root.mainloop()
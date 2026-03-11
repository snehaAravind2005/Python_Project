#Design and implement a GUI-based Card Matching Game using Python .
#Cards are arranged in a rectangular grid with their faces hidden. The player
#selects two cards at a time. If the selected cards match, they remain face
#up; otherwise, they are turned face down again.

import tkinter as tk        # Import Tkinter library for GUI
import random               # Import random module to shuffle card values

# ---------------- SETTINGS ----------------
ROWS = 4                  # Number of rows in the card grid
COLS = 4                 # Number of columns in the card grid
TOTAL_CARDS = ROWS * COLS   # Total number of cards (4x4 = 16)

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()              # Create the main application window
root.title("Card Matching Game")   # Set the window title

first_card = None           # Store position of the first selected card
second_card = None          # Store position of the second selected card
lock = False                # Lock variable to prevent clicking while checking
matched_cards = 0           # Counter for matched cards

# ---------------- CARD VALUES ----------------
values = list(range(1, TOTAL_CARDS // 2 + 1)) * 2   # Create pairs of numbers (1-8 twice)
random.shuffle(values)       # Shuffle the card numbers randomly

buttons = {}                 # Dictionary to store button widgets
card_values = {}             # Dictionary to store card values
index = 0                    # Index to track card positions

# ---------------- CARD CLICK FUNCTION ----------------
def card_click(pos):         # Function called when a card button is clicked

    global first_card, second_card, lock   # Access global variables

    if lock:                 # If the game is locked
        return               # Do nothing

    btn = buttons[pos]       # Get the button at the clicked position

    if btn["text"] != "":    # If the card is already open
        return               # Do nothing

    btn.config(text=card_values[pos], state="disabled")  # Show the card number and disable it

    if first_card is None:   # If this is the first card clicked
        first_card = pos     # Store its position

    else:                    # If first card already selected
        second_card = pos    # Store the second card position
        lock = True          # Lock the board to prevent other clicks
        root.after(800, check_match)   # Wait 800ms then check for match

# ---------------- MATCH CHECK FUNCTION ----------------
def check_match():           # Function to check if two cards match

    global first_card, second_card, lock, matched_cards   # Access global variables

    if card_values[first_card] == card_values[second_card]:  # If both card values are same

        matched_cards += 2   # Increase matched card count by 2

        status_label.config(text="Two cards matched!")  # Show match message

        if matched_cards == TOTAL_CARDS:   # If all cards are matched
            status_label.config(text="You Win! All cards matched!")  # Display win message

    else:                    # If cards do not match

        status_label.config(text="Oops! Try again")  # Show try again message

        buttons[first_card].config(text="", state="normal")  # Hide first card
        buttons[second_card].config(text="", state="normal") # Hide second card

    first_card = None        # Reset first card
    second_card = None       # Reset second card
    lock = False             # Unlock the board

# ---------------- UI LAYOUT ----------------
frame = tk.Frame(root)      # Create a frame to hold card buttons
frame.pack(pady=10)         # Add some vertical padding

for r in range(ROWS):       # Loop through rows
    for c in range(COLS):   # Loop through columns

        pos = index         # Store the card position

        btn = tk.Button(    # Create a button for each card
            frame,
            text="",        # Initially card text is empty
            width=6,        # Button width
            height=3,       # Button height
            font=("Arial", 16),  # Font style
            command=lambda p=pos: card_click(p)  # Call card_click when pressed
        )

        btn.grid(row=r, column=c, padx=5, pady=5)  # Place button in grid layout

        buttons[pos] = btn         # Store button in dictionary
        card_values[pos] = values[index]   # Assign shuffled value to the card

        index += 1                 # Move to next card index

# ---------------- STATUS LABEL ----------------
status_label = tk.Label(           # Create a label to show messages
    root,
    text="Select two cards to find a match",  # Default message
    font=("Arial", 12)
)

status_label.pack(pady=10)         # Display the label with padding

# ---------------- RUN PROGRAM ----------------
root.mainloop()    # Start the GUI event loop
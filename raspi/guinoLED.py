from tkinter import *
from dynamicHz import set_frequency

# Function to handle number button clicks
def button_click(value):
    current_input = input_entry.get()
    input_entry.delete(0, END)
    input_entry.insert(0, current_input + str(value))

# Function to delete the last character (backspace)
def delete_last():
    current_input = input_entry.get()
    input_entry.delete(0, END)
    input_entry.insert(0, current_input[:-1])

# Function to submit input and update frequency
def submit_input():
    current_output = input_entry.get()
    try:
        # Convert input to integer and set the frequency
        frequency = int(current_output)
        set_frequency(frequency)  # Call the dynamicHz module to change frequency
        output_entry.delete(0, END)
        output_entry.insert(0, f"Frequency set to {frequency} Hz")
    except ValueError:
        output_entry.delete(0, END)
        output_entry.insert(0, "Invalid input")
    input_entry.delete(0, END)

# Create main window
window = Tk()
window.title("Keypad Tkinter")

# Create input field
input_entry = Entry(window, width=15, borderwidth=5, font=('Arial', 18), justify='right')
input_entry.grid(row=0, column=0, padx=10, pady=10)

# Create output field
output_entry = Entry(window, width=15, borderwidth=5, font=('Arial', 18), justify='right')
output_entry.grid(row=0, column=1, padx=10, pady=10)

# Create buttons
buttons = [
    ('1', 1, 0), ('2', 1, 1), ('3', 1, 2),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
    ('7', 3, 0), ('8', 3, 1), ('9', 3, 2),
    ('<-', 4, 0), ('0', 4, 1), ('v', 4, 2)
]

# Add buttons to window with grid
for (text, row, col) in buttons:
    if text == '<-':
        button = Button(window, text=text, padx=20, pady=20, font=('Arial', 18), command=delete_last)
    elif text == 'v':
        button = Button(window, text=text, padx=20, pady=20, font=('Arial', 18), command=submit_input)
    else:
        button = Button(window, text=text, padx=20, pady=20, font=('Arial', 18), command=lambda t=text: button_click(t))
    
    button.grid(row=row+1, column=col)

# Run main loop
window.mainloop()

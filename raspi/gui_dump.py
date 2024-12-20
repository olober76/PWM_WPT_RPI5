import tkinter as tk

# Fungsi untuk menangani input tombol angka
def button_click(value):
    current_input = input_entry.get()
    input_entry.delete(0, tk.END)
    input_entry.insert(0, current_input + str(value))

# Fungsi untuk menghapus karakter terakhir (backspace)
def delete_last():
    current_input = input_entry.get()
    input_entry.delete(0, tk.END)
    input_entry.insert(0, current_input[:-1])

# Fungsi untuk mengirimkan input (submit) dan memperbarui output
def submit_input():
    current_output = input_entry.get()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, current_output)
    input_entry.delete(0, tk.END)

# Membuat jendela utama
window = tk.Tk()
window.title("Keypad Tkinter")

# Membuat kolom input untuk menampilkan angka yang ditekan (kiri)
input_entry = tk.Entry(window, width=15, borderwidth=5, font=('Arial', 18), justify='right')
input_entry.grid(row=0, column=0, padx=10, pady=10)

# Membuat kolom output untuk menampilkan angka output (kanan)
output_entry = tk.Entry(window, width=15, borderwidth=5, font=('Arial', 18), justify='right')
output_entry.grid(row=0, column=1, padx=10, pady=10)

# Membuat tombol angka dan fungsinya
buttons = [
    ('1', 1, 0), ('2', 1, 1), ('3', 1, 2),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
    ('7', 3, 0), ('8', 3, 1), ('9', 3, 2),
    ('<-', 4, 0), ('0', 4, 1), ('v', 4, 2)
]

# Menambahkan tombol ke jendela dengan grid
for (text, row, col) in buttons:
    if text == '<-':
        button = tk.Button(window, text=text, padx=20, pady=20, font=('Arial', 18), command=delete_last)
    elif text == 'v':
        button = tk.Button(window, text=text, padx=20, pady=20, font=('Arial', 18), command=submit_input)
    else:
        button = tk.Button(window, text=text, padx=20, pady=20, font=('Arial', 18), command=lambda t=text: button_click(t))
    
    button.grid(row=row+1, column=col)

# Menjalankan loop utama
window.mainloop()

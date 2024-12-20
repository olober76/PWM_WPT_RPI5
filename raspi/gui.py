from tkinter import *

# Membuat jendela utama
window = Tk()

# Mendapatkan ukuran layar
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Mengatur ukuran jendela sesuai dengan ukuran layar
window.geometry(f"{screen_width}x{screen_height}")

# Membuat button
button = Button(window, text="Click Me")

# Menempatkan button di tengah menggunakan pack dengan expand dan anchor
button.pack(expand=True)

# Menjalankan loop utama
window.mainloop()

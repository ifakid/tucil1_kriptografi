import tkinter as tk
from tkinter import filedialog as fd


def file_dialog(label):
    name = fd.askopenfilename()
    label.configure(text=name)


root = tk.Tk()

root.title("Cipher app")

plaintext_label = tk.Label(root, text="Plaintext")
plaintext_label.grid(row=0, column=0, sticky="nw")
plaintext = tk.Text(root, height=10)
plaintext.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

ciphertext_label = tk.Label(root, text="Ciphertext")
ciphertext_label.grid(row=0, column=2, sticky="nw")
cipher_text = tk.Text(root, height=10)
cipher_text.grid(row=1, column=2, padx=10, pady=10, columnspan=2)

select_cipher_label = tk.Label(root, text="Select cipher")
select_cipher_label.grid(row=2, column=0, sticky="e")

file_choose = tk.Button(root, text="Choose file", command=lambda: file_dialog(filename_label))
file_choose.grid(row=3, column=1, sticky="w")
filename_label = tk.Label(root)
filename_label.grid(row=2, column=2, sticky="w")

root.mainloop()

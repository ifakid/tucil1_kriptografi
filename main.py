import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd


def file_dialog(label):
    name = fd.askopenfilename()
    label.configure(text=name)


def validate_number(s):
    return s.isdigit()


def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="OK", command=popup.destroy)
    B1.pack()
    popup.mainloop()


window = tk.Tk()

window.title("Cipher app")

tab_control = ttk.Notebook(window)

aff = ttk.Frame(tab_control)
play = ttk.Frame(tab_control)
vig = ttk.Frame(tab_control)
vig_auto = ttk.Frame(tab_control)
vig_ext = ttk.Frame(tab_control)
vig_full = ttk.Frame(tab_control)

tab_control.add(aff, text='Affine')
tab_control.add(play, text='Playfair')
tab_control.add(vig, text='Vigenere')
tab_control.add(vig_auto, text='Autokey Vigenere')
tab_control.add(vig_ext, text='Extended Vigenere')
tab_control.add(vig_full, text='Full Vigenere')

# ***********************************************


def affine_encrypt():
    if not affine_validate_key(aff_key.get()):
        popupmsg("Key not valid!")
        return
    if not validate_number(aff_shift.get()):
        popupmsg("Shift not valid!")
        return
    if len(aff_enc_filename.cget("text")) == 0 and str(aff_enc_mess.get("1.0", tk.END)).isspace():
        popupmsg("Enter message")
        return

    if len(aff_enc_filename.cget("text")) > 0:
        filename = aff_enc_filename.cget("text")
        print(filename)
    else:  # Text box
        message = str(aff_enc_mess.get("1.0", tk.END))
        print(message)


def affine_decrypt():
    popupmsg("Decrypt")


def affine_validate_key(s):
    return s in ['1', '3', '5', '7', '9', '11', '15', '17', '19', '21', '23', '25']


aff_enc = ttk.Frame(aff, relief=tk.SUNKEN, borderwidth=1)
aff_enc.grid(row=1, column=0, sticky="news")
aff_enc_label = ttk.Label(aff_enc, text="Encode")
aff_enc_label.grid(row=0, column=0)
aff_enc_mess = tk.Text(aff_enc)
aff_enc_mess.grid(row=1, column=0, columnspan=3)
aff_enc_file_label = tk.Label(aff_enc, text="Or choose file: ")
aff_enc_file_label.grid(row=2, column=0)
aff_enc_choose = tk.Button(aff_enc, text="Choose file", command=lambda: file_dialog(aff_enc_filename))
aff_enc_choose.grid(row=2, column=1)
aff_enc_filename = tk.Label(aff_enc)
aff_enc_filename.grid(row=2, column=2)

aff_dec = ttk.Frame(aff, relief=tk.SUNKEN, borderwidth=1)
aff_dec.grid(row=1, column=1, sticky="news")
aff_dec_label = ttk.Label(aff_dec, text="Decode")
aff_dec_label.grid(row=0, column=0)
aff_dec_mess = tk.Text(aff_dec)
aff_dec_mess.grid(row=1, column=0)

aff_key_label = ttk.Label(aff, text="Key: ")
aff_key_label.grid(row=2, column=0)
aff_key = ttk.Entry(aff)
aff_key.grid(row=3, column=0)

aff_shift_label = ttk.Label(aff, text="Shift: ")
aff_shift_label.grid(row=2, column=1)
aff_shift = ttk.Entry(aff)
aff_shift.grid(row=3, column=1)

aff_enc_button = tk.Button(aff, text="Encode", command=affine_encrypt)
aff_enc_button.grid(row=4, column=0)

aff_dec_button = tk.Button(aff, text="Decode", command=affine_decrypt)
aff_dec_button.grid(row=4, column=1)


# ***********************************************

play_label = ttk.Label(play, text="Playfair Cipher")
play_label.grid(row=0, column=0)

play_enc = ttk.Frame(play, relief=tk.SUNKEN, borderwidth=1)
play_enc.grid(row=1, column=0, sticky="news")
play_enc_label = ttk.Label(play_enc, text="Encode")
play_enc_label.grid(row=0, column=0)
play_enc_mess = tk.Text(play_enc)
play_enc_mess.grid(row=1, column=0)

play_dec = ttk.Frame(play, relief=tk.SUNKEN, borderwidth=1)
play_dec.grid(row=1, column=1, sticky="news")
play_dec_label = ttk.Label(play_dec, text="Decode")
play_dec_label.grid(row=0, column=0)
play_dec_mess = tk.Text(play_dec)
play_dec_mess.grid(row=1, column=0)

play_key_label = ttk.Label(play, text="Key: ")
play_key_label.grid(row=2, column=0)
play_key = ttk.Entry(play)
play_key.grid(row=3, column=0)

# ***********************************************

vig_label = ttk.Label(vig, text="Vigenere Cipher")
vig_label.grid(row=0, column=0)

vig_enc = ttk.Frame(vig, relief=tk.SUNKEN, borderwidth=1)
vig_enc.grid(row=1, column=0, sticky="news")
vig_enc_label = ttk.Label(vig_enc, text="Encode")
vig_enc_label.grid(row=0, column=0)
vig_enc_mess = tk.Text(vig_enc)
vig_enc_mess.grid(row=1, column=0)

vig_dec = ttk.Frame(vig, relief=tk.SUNKEN, borderwidth=1)
vig_dec.grid(row=1, column=1, sticky="news")
vig_dec_label = ttk.Label(vig_dec, text="Decode")
vig_dec_label.grid(row=0, column=0)
vig_dec_mess = tk.Text(vig_dec)
vig_dec_mess.grid(row=1, column=0)

vig_key_label = ttk.Label(vig, text="Key: ")
vig_key_label.grid(row=2, column=0)
vig_key = ttk.Entry(vig)
vig_key.grid(row=3, column=0)

# ***********************************************

vig_auto_label = ttk.Label(vig_auto, text="Autokey Vigenere Cipher")
vig_auto_label.grid(row=0, column=0)

vig_auto_enc = ttk.Frame(vig_auto, relief=tk.SUNKEN, borderwidth=1)
vig_auto_enc.grid(row=1, column=0, sticky="news")
vig_auto_enc_label = ttk.Label(vig_auto_enc, text="Encode")
vig_auto_enc_label.grid(row=0, column=0)
vig_auto_enc_mess = tk.Text(vig_auto_enc)
vig_auto_enc_mess.grid(row=1, column=0)

vig_auto_dec = ttk.Frame(vig_auto, relief=tk.SUNKEN, borderwidth=1)
vig_auto_dec.grid(row=1, column=1, sticky="news")
vig_auto_dec_label = ttk.Label(vig_auto_dec, text="Decode")
vig_auto_dec_label.grid(row=0, column=0)
vig_auto_dec_mess = tk.Text(vig_auto_dec)
vig_auto_dec_mess.grid(row=1, column=0)

vig_auto_key_label = ttk.Label(vig_auto, text="Key: ")
vig_auto_key_label.grid(row=2, column=0)
vig_auto_key = ttk.Entry(vig_auto)
vig_auto_key.grid(row=3, column=0)

# ***********************************************

vig_ext_label = ttk.Label(vig_ext, text="Extended Vigenere Cipher")
vig_ext_label.grid(row=0, column=0)

vig_ext_enc = ttk.Frame(vig_ext, relief=tk.SUNKEN, borderwidth=1)
vig_ext_enc.grid(row=1, column=0, sticky="news")
vig_ext_enc_label = ttk.Label(vig_ext_enc, text="Encode")
vig_ext_enc_label.grid(row=0, column=0)
vig_ext_enc_mess = tk.Text(vig_ext_enc)
vig_ext_enc_mess.grid(row=1, column=0)

vig_ext_dec = ttk.Frame(vig_ext, relief=tk.SUNKEN, borderwidth=1)
vig_ext_dec.grid(row=1, column=1, sticky="news")
vig_ext_dec_label = ttk.Label(vig_ext_dec, text="Decode")
vig_ext_dec_label.grid(row=0, column=0)
vig_ext_dec_mess = tk.Text(vig_ext_dec)
vig_ext_dec_mess.grid(row=1, column=0)

vig_ext_key_label = ttk.Label(vig_ext, text="Key: ")
vig_ext_key_label.grid(row=2, column=0)
vig_ext_key = ttk.Entry(vig_ext)
vig_ext_key.grid(row=3, column=0)

# ***********************************************

vig_full_label = ttk.Label(vig_full, text="Full Vigenere Cipher")
vig_full_label.grid(row=0, column=0)

vig_full_enc = ttk.Frame(vig_full, relief=tk.SUNKEN, borderwidth=1)
vig_full_enc.grid(row=1, column=0, sticky="news")
vig_full_enc_label = ttk.Label(vig_full_enc, text="Encode")
vig_full_enc_label.grid(row=0, column=0)
vig_full_enc_mess = tk.Text(vig_full_enc)
vig_full_enc_mess.grid(row=1, column=0)

vig_full_dec = ttk.Frame(vig_full, relief=tk.SUNKEN, borderwidth=1)
vig_full_dec.grid(row=1, column=1, sticky="news")
vig_full_dec_label = ttk.Label(vig_full_dec, text="Decode")
vig_full_dec_label.grid(row=0, column=0)
vig_full_dec_mess = tk.Text(vig_full_dec)
vig_full_dec_mess.grid(row=1, column=0)

vig_full_key_label = ttk.Label(vig_full, text="Key: ")
vig_full_key_label.grid(row=2, column=0)
vig_full_key = ttk.Entry(vig_full)
vig_full_key.grid(row=3, column=0)

# ***********************************************

tab_control.grid(sticky="n", row=0)

window.mainloop()


# ***********************************************



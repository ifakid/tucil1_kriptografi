import tkinter as tk  # python 3
from tkinter import ttk, filedialog as fd, messagebox as mb

import affine
import playfair
import vigenere
import vigenere_autokey
import vigenere_extended
import vigenere_full
import helper


def file_dialog(label, filetypes=None):
    if filetypes is None:
        filetypes = [('All Files', '*.*')]
    name = fd.askopenfilename(filetypes=filetypes)
    label.configure(text=name)


def save_dialog(label, filetypes=None):
    if filetypes is None:
        filetypes = [('All Files', '*.*')]
    file = fd.asksaveasfilename(filetypes=filetypes)
    label.configure(text=file)


class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Cipher')

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, Affine, Playfair, Vigenere, VigenereAuto, VigenereExt, VigenereFull):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Select cipher")
        label.pack(side="top", fill="x", pady=10)

        aff = tk.Button(self, text="Affine Cipher",
                        command=lambda: controller.show_frame("Affine"))
        play = tk.Button(self, text="Playfair Cipher",
                         command=lambda: controller.show_frame("Playfair"))
        vig = tk.Button(self, text="Standard Vigenere Cipher",
                        command=lambda: controller.show_frame("Vigenere"))
        vig_auto = tk.Button(self, text="Auto-key Vigenere Cipher",
                             command=lambda: controller.show_frame("VigenereAuto"))
        vig_ext = tk.Button(self, text="Extended Vigenere Cipher",
                            command=lambda: controller.show_frame("VigenereExt"))
        vig_full = tk.Button(self, text="Full Vigenere Cipher",
                             command=lambda: controller.show_frame("VigenereFull"))

        aff.pack()
        play.pack()
        vig.pack()
        vig_auto.pack()
        vig_ext.pack()
        vig_full.pack()


class Affine(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        home = tk.Button(self, text="Home", command=lambda: controller.show_frame("StartPage"))
        home.grid(row=0, column=0, sticky="w")
        title = tk.Label(self, text="Affine cipher")
        title.grid(row=0, column=1, sticky="w")

        plain_label = tk.Label(self, text="Plaintext")
        plain_label.grid(row=1, column=1, sticky="w")
        self.plain = tk.Text(self, height=10, width=50)
        self.plain.grid(row=2, column=1, columnspan=3, padx=10)

        cipher_label = tk.Label(self, text="Ciphertext")
        cipher_label.grid(row=1, column=4, sticky="w")
        self.cipher = tk.Text(self, height=10, width=50)
        self.cipher.grid(row=2, column=4, columnspan=3, padx=10)

        key_label = tk.Label(self, text="Key")
        key_label.grid(row=3, column=1, sticky="w")
        self.key = tk.Entry(self)
        self.key.grid(row=4, column=1, sticky="w", padx=10)

        shift_label = tk.Label(self, text="Shift")
        shift_label.grid(row=3, column=4, sticky="w")
        self.shift = tk.Entry(self)
        self.shift.grid(row=4, column=4, sticky="w", padx=10)

        encode_button = tk.Button(self, text="Encode", command=self.encrypt)
        encode_button.grid(row=5, column=1)
        decode_button = tk.Button(self, text="Decode", command=self.decrypt)
        decode_button.grid(row=5, column=4)

        separator = ttk.Separator(self, orient="horizontal")
        separator.grid(row=6, sticky="ew", columnspan=7, pady=10)

        filetypes = [('Text document', '*.txt')]

        self.filename = tk.Label(self)
        file_button = tk.Button(self, text="Choose file", command=lambda: file_dialog(self.filename, filetypes))
        file_button.grid(row=7, column=1)
        self.filename.grid(row=7, column=2)

        save_name = tk.Button(self, text="Save file as", command=lambda: save_dialog(self.save_file, filetypes))
        save_name.grid(row=8, column=1, pady=10)
        self.save_file = tk.Label(self)
        self.save_file.grid(row=8, column=2, pady=10)

        key_label = tk.Label(self, text="Key")
        key_label.grid(row=10, column=1, sticky="w")
        self.key_file = tk.Entry(self)
        self.key_file.grid(row=11, column=1, sticky="w", padx=10)

        shift_label = tk.Label(self, text="Shift")
        shift_label.grid(row=10, column=4, sticky="w")
        self.shift_file = tk.Entry(self)
        self.shift_file.grid(row=11, column=4, sticky="w", padx=10)

        encode_button = tk.Button(self, text="Encode", command=lambda: self.encrypt(file=True))
        encode_button.grid(row=12, column=1)
        decode_button = tk.Button(self, text="Decode", command=lambda: self.decrypt(file=True))
        decode_button.grid(row=12, column=4)

    def validate(self, encrypt=True, file=False):
        keys = ['1', '3', '5', '7', '9', '11', '15', '17', '19', '21', '23', '25']
        if file:
            if self.filename.cget('text') == '':
                mb.showwarning(message="Choose source file")
                return False
            if self.save_file.cget('text') == '':
                mb.showwarning(message="Choose save destination")
                return False
            if not self.key_file.get().isdigit() or self.key_file.get() not in keys:
                mb.showwarning(message="Key not valid!")
                return False
            if not self.shift_file.get().isdigit():
                mb.showwarning(message="Shift not valid!")
                return False
            return True
        else:
            if encrypt:
                if self.plain.get("1.0", tk.END).isspace():
                    mb.showwarning(message="Plain text empty")
                    return False
            else:
                if self.cipher.get("1.0", tk.END).isspace():
                    mb.showwarning(message="Cipher text empty")
                    return False
            if not self.key.get().isdigit() or self.key.get() not in keys:
                mb.showwarning(message="Key not valid!")
                return False
            if not self.shift.get().isdigit():
                mb.showwarning(message="Shift not valid!")
                return False
            return True

    def encrypt(self, file=False):
        if file:
            if not self.validate(file=True):
                return False
            source = self.filename.cget('text')
            save = self.save_file.cget('text')
            if save.split('.')[-1] != 'txt':
                save += '.txt'
            key = int(self.key_file.get())
            shift = int(self.shift_file.get())
            with open(source, 'r') as ff, open(save, 'w') as tf:
                while True:
                    line = ff.readline()
                    if not line:
                        break
                    cipher = affine.encode(line, key, shift)
                    tf.writelines(cipher)
            mb.showinfo("File successfully encrypted")
        else:
            if not self.validate():
                return False
            text = self.plain.get("1.0", tk.END)
            key = int(self.key.get())
            shift = int(self.shift.get())
            cipher = affine.encode(text, key, shift)

            self.cipher.delete("1.0", tk.END)
            self.cipher.insert("1.0", cipher)

    def decrypt(self, file=False):
        # TODO: Validation
        if file:
            if not self.validate(file=True, encrypt=False):
                return False
            source = self.filename.cget('text')
            save = self.save_file.cget('text')
            key = int(self.key_file.get())
            shift = int(self.shift_file.get())
            if save.split('.')[-1] != 'txt':
                save += '.txt'
            with open(source, 'r') as ff, open(save, 'w') as tf:
                while True:
                    line = ff.readline()
                    if not line:
                        break
                    cipher = affine.decode(line, key, shift)
                    tf.writelines(cipher)
            mb.showinfo(message="File successfully decrypted")
        else:
            if not self.validate(encrypt=False):
                return False
            text = self.cipher.get("1.0", tk.END)
            key = int(self.key.get())
            shift = int(self.shift.get())
            plain = affine.decode(text, key, shift)

            self.plain.delete("1.0", tk.END)
            self.plain.insert("1.0", plain)


class Playfair(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        home = tk.Button(self, text="Home", command=lambda: controller.show_frame("StartPage"))
        home.grid(row=0, column=0, sticky="w")
        title = tk.Label(self, text="Playfair cipher")
        title.grid(row=0, column=1, sticky="w")

        plain_label = tk.Label(self, text="Plaintext")
        plain_label.grid(row=1, column=1, sticky="w")
        self.plain = tk.Text(self, height=10, width=50)
        self.plain.grid(row=2, column=1, columnspan=3, padx=10)

        cipher_label = tk.Label(self, text="Ciphertext")
        cipher_label.grid(row=1, column=4, sticky="w")
        self.cipher = tk.Text(self, height=10, width=50)
        self.cipher.grid(row=2, column=4, columnspan=3, padx=10)

        key_label = tk.Label(self, text="Key")
        key_label.grid(row=3, column=1, sticky="w")
        self.key = tk.Entry(self)
        self.key.grid(row=4, column=1, sticky="w", padx=10)

        encode_button = tk.Button(self, text="Encode", command=self.encrypt)
        encode_button.grid(row=5, column=1)
        decode_button = tk.Button(self, text="Decode", command=self.decrypt)
        decode_button.grid(row=5, column=4)

        separator = ttk.Separator(self, orient="horizontal")
        separator.grid(row=6, sticky="ew", columnspan=7, pady=10)

        filetypes = [('Text document', '*.txt')]

        self.filename = tk.Label(self)
        file_button = tk.Button(self, text="Choose file", command=lambda: file_dialog(self.filename, filetypes))
        file_button.grid(row=7, column=1)
        self.filename.grid(row=7, column=2)

        save_name = tk.Button(self, text="Save file as", command=lambda: save_dialog(self.save_file, filetypes))
        save_name.grid(row=8, column=1, pady=10)
        self.save_file = tk.Label(self)
        self.save_file.grid(row=8, column=2, pady=10)

        key_label = tk.Label(self, text="Key")
        key_label.grid(row=10, column=1, sticky="w")
        self.key_file = tk.Entry(self)
        self.key_file.grid(row=11, column=1, sticky="w", padx=10)

        encode_button = tk.Button(self, text="Encode", command=lambda: self.encrypt(file=True))
        encode_button.grid(row=12, column=1)
        decode_button = tk.Button(self, text="Decode", command=lambda: self.decrypt(file=True))
        decode_button.grid(row=12, column=4)

    def validate(self, encrypt=True, file=False):
        if file:
            if self.filename.cget('text') == '':
                mb.showwarning(message="Choose source file")
                return False
            if self.save_file.cget('text') == '':
                mb.showwarning(message="Choose save destination")
                return False
            if not playfair.preprocessing(self.key_file.get()):
                mb.showwarning(message="Key not valid!")
                return False
            return True
        else:
            if encrypt:
                if self.plain.get("1.0", tk.END).isspace():
                    mb.showwarning(message="Plain text empty")
                    return False
            else:
                if self.cipher.get("1.0", tk.END).isspace():
                    mb.showwarning(message="Cipher text empty")
                    return False
            if not playfair.preprocessing(self.key.get()):
                mb.showwarning(message="Key not valid!")
                return False
            return True

    def encrypt(self, file=False):
        if file:
            if not self.validate(file=True):
                return False
            source = self.filename.cget('text')
            save = self.save_file.cget('text')
            if save.split('.')[-1] != 'txt':
                save += '.txt'
            key = self.key_file.get()
            with open(source, 'r') as ff, open(save, 'w') as tf:
                line = ff.read()
                cipher = playfair.encode(line, key)
                tf.write(cipher)
            mb.showinfo("File successfully encrypted")
        else:
            if not self.validate():
                return False
            text = self.plain.get("1.0", tk.END)
            key = self.key.get()
            cipher = playfair.encode(text, key)

            self.cipher.delete("1.0", tk.END)
            self.cipher.insert("1.0", cipher)

    def decrypt(self, file=False):
        if file:
            if not self.validate(file=True, encrypt=False):
                return False
            source = self.filename.cget('text')
            save = self.save_file.cget('text')
            key = self.key_file.get()
            if save.split('.')[-1] != 'txt':
                save += '.txt'
            with open(source, 'r') as ff, open(save, 'w') as tf:
                line = ff.read()
                cipher = playfair.decode(line, key)
                tf.write(cipher)
            mb.showinfo(message="File successfully decrypted")
        else:
            if not self.validate(encrypt=False):
                return False
            text = self.cipher.get("1.0", tk.END)
            key = self.key.get()
            plain = playfair.decode(text, key)

            self.plain.delete("1.0", tk.END)
            self.plain.insert("1.0", plain)


class Vigenere(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        home = tk.Button(self, text="Home", command=lambda: controller.show_frame("StartPage"))
        home.grid(row=0, column=0, sticky="w")
        title = tk.Label(self, text="Standard Vigenere cipher")
        title.grid(row=0, column=1, sticky="w")

        plain_label = tk.Label(self, text="Plaintext")
        plain_label.grid(row=1, column=1, sticky="w")
        self.plain = tk.Text(self, height=10, width=50)
        self.plain.grid(row=2, column=1, columnspan=3, padx=10)

        cipher_label = tk.Label(self, text="Ciphertext")
        cipher_label.grid(row=1, column=4, sticky="w")
        self.cipher = tk.Text(self, height=10, width=50)
        self.cipher.grid(row=2, column=4, columnspan=3, padx=10)

        key_label = tk.Label(self, text="Key")
        key_label.grid(row=3, column=1, sticky="w")
        self.key = tk.Entry(self)
        self.key.grid(row=4, column=1, sticky="w", padx=10)

        encode_button = tk.Button(self, text="Encode", command=self.encrypt)
        encode_button.grid(row=5, column=1)
        decode_button = tk.Button(self, text="Decode", command=self.decrypt)
        decode_button.grid(row=5, column=4)

        separator = ttk.Separator(self, orient="horizontal")
        separator.grid(row=6, sticky="ew", columnspan=7, pady=10)

        filetypes = [('Text document', '*.txt')]

        self.filename = tk.Label(self)
        file_button = tk.Button(self, text="Choose file", command=lambda: file_dialog(self.filename, filetypes))
        file_button.grid(row=7, column=1)
        self.filename.grid(row=7, column=2)

        save_name = tk.Button(self, text="Save file as", command=lambda: save_dialog(self.save_file, filetypes))
        save_name.grid(row=8, column=1, pady=10)
        self.save_file = tk.Label(self)
        self.save_file.grid(row=8, column=2, pady=10)

        key_label = tk.Label(self, text="Key")
        key_label.grid(row=10, column=1, sticky="w")
        self.key_file = tk.Entry(self)
        self.key_file.grid(row=11, column=1, sticky="w", padx=10)

        encode_button = tk.Button(self, text="Encode", command=lambda: self.encrypt(file=True))
        encode_button.grid(row=12, column=1)
        decode_button = tk.Button(self, text="Decode", command=lambda: self.decrypt(file=True))
        decode_button.grid(row=12, column=4)

    def validate(self, encrypt=True, file=False):
        if file:
            if self.filename.cget('text') == '':
                mb.showwarning(message="Choose source file")
                return False
            if self.save_file.cget('text') == '':
                mb.showwarning(message="Choose save destination")
                return False
            if not vigenere.preprocessing(self.key_file.get()):
                mb.showwarning(message="Key not valid!")
                return False
            return True
        else:
            if encrypt:
                if self.plain.get("1.0", tk.END).isspace():
                    mb.showwarning(message="Plain text empty")
                    return False
            else:
                if self.cipher.get("1.0", tk.END).isspace():
                    mb.showwarning(message="Cipher text empty")
                    return False
            if not vigenere.preprocessing(self.key.get()):
                mb.showwarning(message="Key not valid!")
                return False
            return True

    # TODO: Decrypt File
    def encrypt(self, file=False):
        if file:
            if not self.validate(file=True):
                return False
            source = self.filename.cget('text')
            save = self.save_file.cget('text')
            if save.split('.')[-1] != 'txt':
                save += '.txt'
            key = self.key_file.get()
            with open(source, 'r') as ff, open(save, 'w') as tf:
                line = ff.read()
                cipher = vigenere.encode(line, key)
                tf.write(cipher)
            mb.showinfo("File successfully encrypted")
        else:
            if not self.validate():
                return False
            text = self.plain.get("1.0", tk.END)
            key = self.key.get()
            cipher = vigenere.encode(text, key)

            self.cipher.delete("1.0", tk.END)
            self.cipher.insert("1.0", cipher)

    def decrypt(self, file=False):
        if file:
            if not self.validate(file=True, encrypt=False):
                return False
            source = self.filename.cget('text')
            save = self.save_file.cget('text')
            key = self.key_file.get()
            if save.split('.')[-1] != 'txt':
                save += '.txt'
            with open(source, 'r') as ff, open(save, 'w') as tf:
                line = ff.read()
                cipher = vigenere.decode(line, key)
                tf.write(cipher)
            mb.showinfo(message="File successfully decrypted")
        else:
            if not self.validate(encrypt=False):
                return False
            text = self.cipher.get("1.0", tk.END)
            key = self.key.get()
            plain = vigenere.decode(text, key)

            self.plain.delete("1.0", tk.END)
            self.plain.insert("1.0", plain)


class VigenereAuto(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        home = tk.Button(self, text="Home", command=lambda: controller.show_frame("StartPage"))
        home.grid(row=0, column=0, sticky="w")
        title = tk.Label(self, text="Playfair cipher")
        title.grid(row=0, column=1, sticky="w")

        plain_label = tk.Label(self, text="Plaintext")
        plain_label.grid(row=1, column=1, sticky="w")
        self.plain = tk.Text(self, height=10, width=50)
        self.plain.grid(row=2, column=1, columnspan=3, padx=10)

        cipher_label = tk.Label(self, text="Ciphertext")
        cipher_label.grid(row=1, column=4, sticky="w")
        self.cipher = tk.Text(self, height=10, width=50)
        self.cipher.grid(row=2, column=4, columnspan=3, padx=10)

        key_label = tk.Label(self, text="Key")
        key_label.grid(row=3, column=1, sticky="w")
        self.key = tk.Entry(self)
        self.key.grid(row=4, column=1, sticky="w", padx=10)

        encode_button = tk.Button(self, text="Encode", command=self.encrypt)
        encode_button.grid(row=5, column=1)
        decode_button = tk.Button(self, text="Decode", command=self.decrypt)
        decode_button.grid(row=5, column=4)

        separator = ttk.Separator(self, orient="horizontal")
        separator.grid(row=6, sticky="ew", columnspan=7, pady=10)

        filetypes = [('Text document', '*.txt')]

        self.filename = tk.Label(self)
        file_button = tk.Button(self, text="Choose file", command=lambda: file_dialog(self.filename, filetypes))
        file_button.grid(row=7, column=1)
        self.filename.grid(row=7, column=2)

        save_name = tk.Button(self, text="Save file as", command=lambda: save_dialog(self.save_file, filetypes))
        save_name.grid(row=8, column=1, pady=10)
        self.save_file = tk.Label(self)
        self.save_file.grid(row=8, column=2, pady=10)

        key_label = tk.Label(self, text="Key")
        key_label.grid(row=10, column=1, sticky="w")
        self.key_file = tk.Entry(self)
        self.key_file.grid(row=11, column=1, sticky="w", padx=10)

        encode_button = tk.Button(self, text="Encode", command=lambda: self.encrypt(file=True))
        encode_button.grid(row=12, column=1)
        decode_button = tk.Button(self, text="Decode", command=lambda: self.decrypt(file=True))
        decode_button.grid(row=12, column=4)

    def validate(self, encrypt=True, file=False):
        if file:
            if self.filename.cget('text') == '':
                mb.showwarning(message="Choose source file")
                return False
            if self.save_file.cget('text') == '':
                mb.showwarning(message="Choose save destination")
                return False
            if not helper.preprocessing(self.key_file.get()):
                mb.showwarning(message="Key not valid!")
                return False
            return True
        else:
            if encrypt:
                if self.plain.get("1.0", tk.END).isspace():
                    mb.showwarning(message="Plain text empty")
                    return False
            else:
                if self.cipher.get("1.0", tk.END).isspace():
                    mb.showwarning(message="Cipher text empty")
                    return False
            if not helper.preprocessing(self.key.get()):
                mb.showwarning(message="Key not valid!")
                return False
            return True

    def encrypt(self, file=False):
        if file:
            if not self.validate(file=True):
                return False
            source = self.filename.cget('text')
            save = self.save_file.cget('text')
            if save.split('.')[-1] != 'txt':
                save += '.txt'
            key = self.key_file.get()
            with open(source, 'r') as ff, open(save, 'w') as tf:
                line = ff.read()
                cipher = vigenere_autokey.encode(line, key)
                tf.write(cipher)
            mb.showinfo("File successfully encrypted")
        else:
            if not self.validate():
                return False
            text = self.plain.get("1.0", tk.END)
            key = self.key.get()
            cipher = vigenere_autokey.encode(text, key)

            self.cipher.delete("1.0", tk.END)
            self.cipher.insert("1.0", cipher)

    def decrypt(self, file=False):
        if file:
            if not self.validate(file=True, encrypt=False):
                return False
            source = self.filename.cget('text')
            save = self.save_file.cget('text')
            key = self.key_file.get()
            if save.split('.')[-1] != 'txt':
                save += '.txt'
            with open(source, 'r') as ff, open(save, 'w') as tf:
                line = ff.read()
                cipher = vigenere_autokey.decode(line, key)
                tf.write(cipher)
            mb.showinfo(message="File successfully decrypted")
        else:
            if not self.validate(encrypt=False):
                return False
            text = self.cipher.get("1.0", tk.END)
            key = self.key.get()
            plain = vigenere_autokey.decode(text, key)

            self.plain.delete("1.0", tk.END)
            self.plain.insert("1.0", plain)


class VigenereExt(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        home = tk.Button(self, text="Home", command=lambda: controller.show_frame("StartPage"))
        home.grid(row=0, column=0, sticky="w")
        title = tk.Label(self, text="Extended Vigenere cipher")
        title.grid(row=0, column=1, sticky="w")

        plain_label = tk.Label(self, text="Plaintext")
        plain_label.grid(row=1, column=1, sticky="w")
        self.plain = tk.Text(self, height=10, width=50)
        self.plain.grid(row=2, column=1, columnspan=3, padx=10)

        cipher_label = tk.Label(self, text="Ciphertext")
        cipher_label.grid(row=1, column=4, sticky="w")
        self.cipher = tk.Text(self, height=10, width=50)
        self.cipher.grid(row=2, column=4, columnspan=3, padx=10)

        key_label = tk.Label(self, text="Key")
        key_label.grid(row=3, column=1, sticky="w")
        self.key = tk.Entry(self)
        self.key.grid(row=4, column=1, sticky="w", padx=10)

        encode_button = tk.Button(self, text="Encode", command=self.encrypt)
        encode_button.grid(row=5, column=1)
        decode_button = tk.Button(self, text="Decode", command=self.decrypt)
        decode_button.grid(row=5, column=4)

        separator = ttk.Separator(self, orient="horizontal")
        separator.grid(row=6, sticky="ew", columnspan=7, pady=10)

        filetypes = [('All files', '*.*')]

        self.filename = tk.Label(self)
        file_button = tk.Button(self, text="Choose file", command=lambda: file_dialog(self.filename, filetypes))
        file_button.grid(row=7, column=1)
        self.filename.grid(row=7, column=2)

        save_name = tk.Button(self, text="Save file as", command=lambda: save_dialog(self.save_file, filetypes))
        save_name.grid(row=8, column=1, pady=10)
        self.save_file = tk.Label(self)
        self.save_file.grid(row=8, column=2, pady=10)

        key_label = tk.Label(self, text="Key")
        key_label.grid(row=10, column=1, sticky="w")
        self.key_file = tk.Entry(self)
        self.key_file.grid(row=11, column=1, sticky="w", padx=10)

        encode_button = tk.Button(self, text="Encode", command=lambda: self.encrypt(file=True))
        encode_button.grid(row=12, column=1)
        decode_button = tk.Button(self, text="Decode", command=lambda: self.decrypt(file=True))
        decode_button.grid(row=12, column=4)

    def validate(self, encrypt=True, file=False):
        if file:
            if self.filename.cget('text') == '':
                mb.showwarning(message="Choose source file")
                return False
            if self.save_file.cget('text') == '':
                mb.showwarning(message="Choose save destination")
                return False
            if self.key_file.get() == '':
                mb.showwarning(message="Key not valid!")
                return False
            return True
        else:
            if encrypt:
                if self.plain.get("1.0", tk.END).isspace():
                    mb.showwarning(message="Plain text empty")
                    return False
            else:
                if self.cipher.get("1.0", tk.END).isspace():
                    mb.showwarning(message="Cipher text empty")
                    return False
            if self.key.get() == '':
                mb.showwarning(message="Key not valid!")
                return False
            return True

    def encrypt(self, file=False):
        if file:
            if not self.validate(file=True):
                return False
            source = self.filename.cget('text')
            save = self.save_file.cget('text')
            key = self.key_file.get()
            with open(source, 'rb') as ff, open(save, 'wb') as tf:
                while True:
                    line = ff.read(len(key))
                    if not line:
                        break
                    cipher = vigenere_extended.encode(line, key, file=True)
                    tf.write(cipher)
            mb.showinfo("File successfully encrypted")
        else:
            if not self.validate():
                return False
            text = self.plain.get("1.0", tk.END)
            key = self.key.get()
            cipher = vigenere_extended.encode(text, key)

            self.cipher.delete("1.0", tk.END)
            self.cipher.insert("1.0", cipher)

    def decrypt(self, file=False):
        if file:
            if not self.validate(file=True, encrypt=False):
                return False
            source = self.filename.cget('text')
            save = self.save_file.cget('text')
            key = self.key_file.get()
            with open(source, 'rb') as ff, open(save, 'wb') as tf:
                while True:
                    line = ff.read(len(key))
                    print(line)
                    if not line:
                        break
                    cipher = vigenere_extended.decode(line, key, file=True)
                    tf.write(cipher)
            mb.showinfo(message="File successfully decrypted")
        else:
            if not self.validate(encrypt=False):
                return False
            text = self.cipher.get("1.0", tk.END)
            key = self.key.get()
            plain = vigenere_extended.decode(text, key)

            self.plain.delete("1.0", tk.END)
            self.plain.insert("1.0", plain)


class VigenereFull(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        home = tk.Button(self, text="Home", command=lambda: controller.show_frame("StartPage"))
        home.grid(row=0, column=0, sticky="w")
        title = tk.Label(self, text="Playfair cipher")
        title.grid(row=0, column=1, sticky="w")

        plain_label = tk.Label(self, text="Plaintext")
        plain_label.grid(row=1, column=1, sticky="w")
        self.plain = tk.Text(self, height=10, width=50)
        self.plain.grid(row=2, column=1, columnspan=3, padx=10)

        cipher_label = tk.Label(self, text="Ciphertext")
        cipher_label.grid(row=1, column=4, sticky="w")
        self.cipher = tk.Text(self, height=10, width=50)
        self.cipher.grid(row=2, column=4, columnspan=3, padx=10)

        key_label = tk.Label(self, text="Key")
        key_label.grid(row=3, column=1, sticky="w")
        self.key = tk.Entry(self)
        self.key.grid(row=4, column=1, sticky="w", padx=10)

        encode_button = tk.Button(self, text="Encode", command=self.encrypt)
        encode_button.grid(row=5, column=1)
        decode_button = tk.Button(self, text="Decode", command=self.decrypt)
        decode_button.grid(row=5, column=4)

        separator = ttk.Separator(self, orient="horizontal")
        separator.grid(row=6, sticky="ew", columnspan=7, pady=10)

        filetypes = [('Text document', '*.txt')]

        self.filename = tk.Label(self)
        file_button = tk.Button(self, text="Choose file", command=lambda: file_dialog(self.filename, filetypes))
        file_button.grid(row=7, column=1)
        self.filename.grid(row=7, column=2)

        save_name = tk.Button(self, text="Save file as", command=lambda: save_dialog(self.save_file, filetypes))
        save_name.grid(row=8, column=1, pady=10)
        self.save_file = tk.Label(self)
        self.save_file.grid(row=8, column=2, pady=10)

        key_label = tk.Label(self, text="Key")
        key_label.grid(row=10, column=1, sticky="w")
        self.key_file = tk.Entry(self)
        self.key_file.grid(row=11, column=1, sticky="w", padx=10)

        encode_button = tk.Button(self, text="Encode", command=lambda: self.encrypt(file=True))
        encode_button.grid(row=12, column=1)
        decode_button = tk.Button(self, text="Decode", command=lambda: self.decrypt(file=True))
        decode_button.grid(row=12, column=4)

    def validate(self, encrypt=True, file=False):
        if file:
            if self.filename.cget('text') == '':
                mb.showwarning(message="Choose source file")
                return False
            if self.save_file.cget('text') == '':
                mb.showwarning(message="Choose save destination")
                return False
            if not helper.preprocessing(self.key_file.get()):
                mb.showwarning(message="Key not valid!")
                return False
            return True
        else:
            if encrypt:
                if self.plain.get("1.0", tk.END).isspace():
                    mb.showwarning(message="Plain text empty")
                    return False
            else:
                if self.cipher.get("1.0", tk.END).isspace():
                    mb.showwarning(message="Cipher text empty")
                    return False
            if not helper.preprocessing(self.key.get()):
                mb.showwarning(message="Key not valid!")
                return False
            return True

    def encrypt(self, file=False):
        if file:
            if not self.validate(file=True):
                return False
            source = self.filename.cget('text')
            save = self.save_file.cget('text')
            if save.split('.')[-1] != 'txt':
                save += '.txt'
            key = self.key_file.get()
            with open(source, 'r') as ff, open(save, 'w') as tf:
                while True:
                    line = ff.readline()
                    if not line:
                        break
                    cipher = vigenere_autokey.encode(line, key)
                    tf.writelines(cipher)
            mb.showinfo("File successfully encrypted")
        else:
            if not self.validate():
                return False
            text = self.plain.get("1.0", tk.END)
            key = self.key.get()
            cipher = vigenere_autokey.encode(text, key)

            self.cipher.delete("1.0", tk.END)
            self.cipher.insert("1.0", cipher)

    def decrypt(self, file=False):
        if file:
            if not self.validate(file=True, encrypt=False):
                return False
            source = self.filename.cget('text')
            save = self.save_file.cget('text')
            key = self.key_file.get()
            if save.split('.')[-1] != 'txt':
                save += '.txt'
            with open(source, 'r') as ff, open(save, 'w') as tf:
                while True:
                    line = ff.readline()
                    if not line:
                        break
                    cipher = vigenere_autokey.decode(line, key)
                    tf.writelines(cipher)
            mb.showinfo(message="File successfully decrypted")
        else:
            if not self.validate(encrypt=False):
                return False
            text = self.cipher.get("1.0", tk.END)
            key = self.key.get()
            plain = vigenere_autokey.decode(text, key)

            self.plain.delete("1.0", tk.END)
            self.plain.insert("1.0", plain)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()

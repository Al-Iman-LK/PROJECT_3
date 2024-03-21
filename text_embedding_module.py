from Crypto.Cipher import AES
from tkinter import *
import tkinter.filedialog
from tkinter import messagebox
from PIL import ImageTk
from PIL import Image
from io import BytesIO
import base64
import hashlib
from Crypto.Cipher import AES
from cryptography.fernet import Fernet
import os

class IMG_Stegno:
    output_image_size = 0

    def main(self, root):
        root.title('Steganographic text-image wrapping tool')
        root.geometry('500x600')
        root.resizable(width=False, height=False)
        root.config(bg='#d4dde5')

        frame = Frame(root, bg='#d4dde5')
        frame.grid()

        title = Label(frame, text='Image Steganography', bg='#d4dde5', fg='#2c3e50')
        title.config(font=('Arial', 25, 'bold'))
        title.grid(pady=20)

        encode = Button(frame, text="Encode", command=lambda: self.encode_frame1(frame), padx=14, bg='#2980b9', fg='#ecf0f1')
        encode.config(font=('Arial', 14))
        encode.grid(row=1, pady=10)

        decode = Button(frame, text="Decode", command=lambda: self.decode_frame1(frame), padx=14, bg='#c0392b', fg='#ecf0f1')
        decode.config(font=('Arial', 14))
        decode.grid(row=2, pady=10)

        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

    def back(self, frame):
        frame.destroy()
        self.main(root)

    def encode_frame1(self, F):
        F.destroy()
        F2 = Frame(root, bg='#d4dde5')

        label1 = Label(F2, text='Select Image to embed text :', bg='#d4dde5', fg='#2c3e50')
        label1.config(font=('Arial', 20, 'bold'))
        label1.grid(row=0, pady=20)

        button_bws = Button(F2, text='Brows', command=lambda: self.encode_frame2(F2), bg='#2980b9', fg='#ecf0f1')
        button_bws.config(font=('Arial', 16))
        button_bws.grid(row=1, pady=10)

        button_back = Button(F2, text='Back', command=lambda: IMG_Stegno.back(self, F2), bg='#c0392b', fg='#ecf0f1')
        button_back.config(font=('Arial', 16))
        button_back.grid(row=2, pady=10)

        F2.grid()

    def decode_frame1(self, F):
        F.destroy()
        d_f2 = Frame(root, bg='#d4dde5')

        label1 = Label(d_f2, text='Select Image to reveal text:', bg='#d4dde5', fg='#2c3e50')
        label1.config(font=('Arial', 20, 'bold'))
        label1.grid(row=0, pady=20)

        button_bws = Button(d_f2, text='Brows', command=lambda: self.decode_frame2(d_f2), bg='#2980b9', fg='#ecf0f1')
        button_bws.config(font=('Arial', 16))
        button_bws.grid(row=1, pady=10)

        button_back = Button(d_f2, text='Back', command=lambda: IMG_Stegno.back(self, d_f2), bg='#c0392b', fg='#ecf0f1')
        button_back.config(font=('Arial', 16))
        button_back.grid(row=2, pady=10)

        d_f2.grid()

    def decode_frame2(self, d_F2):
        d_F3 = Frame(root, bg='#d4dde5')
        myfiles = tkinter.filedialog.askopenfilename(filetypes=(
        [('png', '*.png'), ('jpeg', '*.jpeg'), ('jpg', '*.jpg'), ('All Files', '*.*')]))
        if not myfiles:
            messagebox.showerror("Error", "Your selection is empty! ")
        else:
            my_img = Image.open(myfiles, 'r')
            my_image = my_img.resize((300, 200))
            img = ImageTk.PhotoImage(my_image)
            label4 = Label(d_F3, text='Selected Image :', bg='#d4dde5', fg='#2c3e50')
            label4.config(font=('Arial', 14, 'bold'))
            label4.grid()
            board = Label(d_F3, image=img)
            board.image = img
            board.grid()

            hidden_data = self.decode(my_img)

            label2 = Label(d_F3, text='Wrapped text is :', bg='#d4dde5', fg='#2c3e50')
            label2.config(font=('Arial', 14, 'bold'))
            label2.grid(pady=10)

            text_a = Text(d_F3, width=50, height=10)
            text_a.insert(INSERT, hidden_data)
            text_a.configure(state='disabled')
            text_a.grid()

            button_back = Button(d_F3, text='Cancel', command=lambda: self.frame_3(d_F3), bg='#c0392b', fg='#ecf0f1')
            button_back.config(font=('Arial', 14))
            button_back.grid(pady=15)

            d_F3.grid(row=1)
            d_F2.destroy()

    def encode_frame2(self, e_F2):
        e_pg = Frame(root, bg='#d4dde5')
        myfile = tkinter.filedialog.askopenfilename(filetypes=(
        [('png', '*.png'), ('jpeg', '*.jpeg'), ('jpg', '*.jpg'), ('All Files', '*.*')]))
        if not myfile:
            messagebox.showerror("Error", "Your selection is empty!")
        else:
            my_img = Image.open(myfile)
            new_image = my_img.resize((300, 200))
            img = ImageTk.PhotoImage(new_image)
            label3 = Label(e_pg, text='Selected Image', bg='#d4dde5', fg='#2c3e50')
            label3.config(font=('Arial', 14, 'bold'))
            label3.grid()
            board = Label(e_pg, image=img)
            board.image = img
            board.grid()
            label2 = Label(e_pg, text='Enter the text', bg='#d4dde5', fg='#2c3e50')
            label2.config(font=('Arial', 14, 'bold'))
            label2.grid(pady=15)
            text_a = Text(e_pg, width=50, height=10)
            text_a.grid()
            encode_button = Button(e_pg, text='Cancel', command=lambda: IMG_Stegno.back(self, e_pg), bg='#c0392b',
                                   fg='#ecf0f1')
            encode_button.config(font=('Arial', 14))
            encode_button.grid()

            data = text_a.get("1.0", "end-1c")
            button_back = Button(e_pg, text='Encode', command=lambda:  [self.enc_fun(text_a, my_img), IMG_Stegno.back(self, e_pg)], bg='#2980b9', fg='#ecf0f1')
            button_back.config(font=('Arial', 14))
            button_back.grid(pady=15)

            e_pg.grid(row=1)
            e_F2.destroy()

    def decode(self, image):
        image_data = iter(image.getdata())
        data = ''

        while (True):
            pixels = [value for value in image_data.__next__()[:3] +
                      image_data.__next__()[:3] +
                      image_data.__next__()[:3]]
            binary_str = ''
            for i in pixels[:8]:
                if i % 2 == 0:
                    binary_str += '0'
                else:
                    binary_str += '1'

            data += chr(int(binary_str, 2))
            if pixels[-1] % 2 != 0:
                decrypted_data = self.decrypt(data)
                return decrypted_data

    def decrypt(self, data):
        key = '7pDV8F76ROom7h2QKLY5c5V5iGg21N1Vr81y3Hc1K2Q='
        f = Fernet(key)
        decrypted_data = f.decrypt(data.encode())
        return decrypted_data.decode('utf-8')

    def generate_Data(self, data):
        new_data = []

        for i in data:
            new_data.append(format(ord(str(chr(i))), '08b'))
        return new_data

    def modify_Pix(self, pix, data):
        dataList = self.generate_Data(data)
        dataLen = len(dataList)
        imgData = iter(pix)
        for i in range(dataLen):
            pix = [value for value in imgData.__next__()[:3] +
                   imgData.__next__()[:3] +
                   imgData.__next__()[:3]]

            for j in range(0, 8):
                if (dataList[i][j] == '0') and (pix[j] % 2 != 0):
                    if (pix[j] % 2 != 0):
                        pix[j] -= 1

                elif (dataList[i][j] == '1') and (pix[j] % 2 == 0):
                    pix[j] -= 1

            if (i == dataLen - 1):
                if (pix[-1] % 2 == 0):
                    pix[-1] -= 1
            else:
                if (pix[-1] % 2 != 0):
                    pix[-1] -= 1

            pix = tuple(pix)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]

    def encode_enc(self, newImg, data):
        w = newImg.size[0]
        (x, y) = (0, 0)

        for pixel in self.modify_Pix(newImg.getdata(), data):
            newImg.putpixel((x, y), pixel)
            if (x == w - 1):
                x = 0
                y += 1
            else:
                x += 1

    def enc_fun(self, text_a, my_img):
        data = text_a.get("1.0", "end-1c")
        key = '7pDV8F76ROom7h2QKLY5c5V5iGg21N1Vr81y3Hc1K2Q='
        if len(data) == 0:
            messagebox.showinfo("Alert", "Enter text in TextBox")
        else:
            newImg = my_img.copy()
            newdata = self.encrypt(key, data)
            self.encode_enc(newImg, newdata)
            temp = os.path.splitext(os.path.basename(my_img.filename))[0]
            newImg.save(tkinter.filedialog.asksaveasfilename(initialfile=temp, filetypes=[('png', '*.png')], defaultextension=".png"))
            self.d_image_size = my_img.tell()
            self.d_image_w, self.d_image_h = newImg.size
            messagebox.showinfo("Success", "Encoding Successful\nFile is saved as Image_with_hiddentext.png")

    def encrypt(self, key, data):
        f = Fernet(key)
        encrypted_data = f.encrypt(data.encode())
        return encrypted_data

    def frame_3(self, frame):
        frame.destroy()
        self.main(root)

root = Tk()
o = IMG_Stegno()
o.main(root)
root.mainloop()




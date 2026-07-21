import customtkinter as ctk
from tkinter import PhotoImage
import app

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("600x400")
root.title("Loading...")
root.overrideredirect(True)

icon = PhotoImage(file="icon/logo.png")
root.iconphoto(True, icon)

logo = ctk.CTkLabel(root, image=icon, text="")
logo.pack(pady=30)

judul = ctk.CTkLabel(
    root,
    text="SISTEM DETEKSI\nKERETAKAN UBIN / KERAMIK",
    font=("Arial",24,"bold")
)
judul.pack()

loading = ctk.CTkProgressBar(root,width=350)
loading.pack(pady=30)

loading.set(0)

nilai = 0

def jalan():

    global nilai

    nilai += 0.02

    loading.set(nilai)

    if nilai >= 1:
        root.destroy()
        app.CrackDetectionApp()

    else:
        root.after(50,jalan)

jalan()

root.mainloop()
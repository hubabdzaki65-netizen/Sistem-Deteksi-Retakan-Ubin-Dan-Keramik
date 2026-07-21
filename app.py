import os

from database import *
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2

from detector import detect_crack

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class CrackDetectionApp:

    def __init__(self):

        create_database()

        self.root = ctk.CTk()
        self.root.title("Deteksi Keretakan Ubin/Keramik")
        self.root.geometry("1200x700")

        self.image_path = None
        self.original_image = None

        self.create_widgets()

        self.root.mainloop()

    def create_widgets(self):

        title = ctk.CTkLabel(
            self.root,
            text="SISTEM DETEKSI KERETAKAN UBIN / KERAMIK",
            font=("Arial", 24, "bold")
        )

        title.pack(pady=15)

        button_frame = ctk.CTkFrame(self.root)

        button_frame.pack(pady=10)

        upload_btn = ctk.CTkButton(
            button_frame,
            text="Upload Gambar",
            width=180,
            command=self.upload_image
        )

        upload_btn.grid(row=0, column=0, padx=10)

        process_btn = ctk.CTkButton(
            button_frame,
            text="Proses Deteksi",
            width=180,
            fg_color="green",
            command=self.process_image
        )

        process_btn.grid(row=0, column=1, padx=10)

        save_btn = ctk.CTkButton(
            button_frame,
            text="Simpan Hasil",
            width=180,
            fg_color="orange",
            command=self.save_result
        )

        save_btn.grid(row=0, column=2, padx=10)

        image_frame = ctk.CTkFrame(self.root)

        image_frame.pack(pady=15)

        self.original_label = ctk.CTkLabel(
            image_frame,
            text="Gambar Asli",
            width=450,
            height=400
        )

        self.original_label.grid(row=0, column=0, padx=15)

        self.result_label = ctk.CTkLabel(
            image_frame,
            text="Hasil Deteksi",
            width=450,
            height=400
        )

        self.result_label.grid(row=0, column=1, padx=15)

        info_frame = ctk.CTkFrame(self.root)

        info_frame.pack(fill="x", padx=20, pady=10)

        self.status_text = ctk.CTkLabel(
            info_frame,
            text="Status : -",
            font=("Arial", 18)
        )

        self.status_text.pack(anchor="w", padx=20, pady=5)

        self.percent_text = ctk.CTkLabel(
            info_frame,
            text="Persentase Retakan : -",
            font=("Arial", 18)
        )

        self.percent_text.pack(anchor="w", padx=20, pady=5)

    def upload_image(self):

        file = filedialog.askopenfilename(

            filetypes=[
                ("Image", "*.jpg *.png *.jpeg")
            ]

        )

        if file == "":
            return

        self.image_path = file

        image = Image.open(file)

        image.thumbnail((450, 400))

        self.original_image = ImageTk.PhotoImage(image)

        self.original_label.configure(image=self.original_image, text="")

    def process_image(self):

        if self.image_path is None:

            messagebox.showwarning(
                "Peringatan",
                "Silakan upload gambar terlebih dahulu."
            )

            return

        status, percent, result = detect_crack(self.image_path)

        filename = os.path.basename(self.image_path)

        save_result( 
        filename,
        status,
        percent
        )
            
        rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

        image = Image.fromarray(rgb)

        image.thumbnail((450, 400))

        self.result_image = ImageTk.PhotoImage(image)

        self.result_label.configure(image=self.result_image, text="")

        if status == "NORMAL":

            self.status_text.configure(
                text="Status : NORMAL",
                text_color="green"
            )

        else:

            self.status_text.configure(
                text="Status : RETAK",
                text_color="red"
            )

        self.percent_text.configure(
            text=f"Persentase Retakan : {percent:.2f}%"
        )

        self.last_result = result

    def save_result(self):

        if not hasattr(self, "last_result"):

            messagebox.showwarning(
                "Peringatan",
                "Belum ada hasil deteksi."
            )

            return

        if not os.path.exists("hasil"):

            os.makedirs("hasil")

        filename = filedialog.asksaveasfilename(

            initialdir="hasil",

            defaultextension=".jpg",

            filetypes=[("JPEG", "*.jpg")]

        )

        if filename == "":
            return

        cv2.imwrite(filename, self.last_result)

        messagebox.showinfo(
            "Sukses",
            "Hasil berhasil disimpan."
        )


if __name__ == "__main__":
    CrackDetectionApp()
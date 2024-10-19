 # tkinter: Библиотека для создания графического интерфейса.
# filedialog: Модуль для открытия диалогов выбора файлов.
# messagebox: Модуль для отображения всплывающих окон с сообщениями.
# PIL (Pillow): Библиотека для работы с изображениями.
# os: Модуль для взаимодействия с операционной системой, например, для работы с файлами и директориями.

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

#Создается класс PhotoUploader, который будет отвечать за загрузку и отображение изображений.

class PhotoUploader:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Uploader")
        self.root.geometry("350x750")  # Размеры окна

        # Установка светло-желтого фона для главного окна
        self.root.configure(bg='#FFFACD')  # Светло-желтый цвет

        # Создание рамки для метки и кнопки
        self.frame = tk.Frame(root, bg='#D3D3D3', bd=2, relief=tk.SUNKEN)
        self.frame.pack(pady=10, padx=10, fill=tk.X)

        
        self.label = tk.Label(self.frame, text="Выложить пост", font=("Helvetica", 20, "bold"), bg='#D3D3D3',
                              fg='black')
        self.label.pack(pady=5)

        self.upload_button = tk.Button(self.frame, text="+", command=self.upload_photos, font=("Arial", 16), width=5)
        self.upload_button.pack(pady=5)

        # Создание Frame для прокрутки
        self.scrollable_frame = tk.Frame(root, bg='#D3D3D3')
        self.scrollable_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.scrollable_frame)
        self.scrollbar = tk.Scrollbar(self.scrollable_frame, orient="vertical", command=self.canvas.yview)

        self.image_frame = tk.Frame(self.canvas, bg='#D3D3D3')
        self.image_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.image_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.saved_images_dir = "uploaded_images"
        os.makedirs(self.saved_images_dir, exist_ok=True)

        self.image_labels = []

    def upload_photos(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")])
        if file_paths:
            for file_path in file_paths:
                try:
                    image = Image.open(file_path)
                    image.thumbnail((300, 300))  # Установка размера изображения
                    photo = ImageTk.PhotoImage(image)

                    # Создание контейнера для центрирования изображения
                    image_container = tk.Frame(self.image_frame, bg='#D3D3D3')
                    image_container.pack(pady=5, padx=10)  # Отступы

                    # Создание метки для изображения
                    image_label = tk.Label(image_container, image=photo, bg='#D3D3D3')
                    image_label.image = photo
                    image_label.pack()  # Центрирование по умолчанию в Frame

                    self.image_labels.append(image_label)

                    image_name = os.path.basename(file_path)
                    save_path = os.path.join(self.saved_images_dir, image_name)
                    image.save(save_path)
                    messagebox.showinfo("Успех", f"Изображение сохранено как: {save_path}")
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoUploader(root)
    root.mainloop()
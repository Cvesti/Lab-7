import tkinter as tk
from tkinter import ttk
import requests
from PIL import ImageTk, Image
from io import BytesIO

class FoxImageGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных лисичек")
        self.root.geometry("500x500")
        self.image_frame = ttk.Frame(root)
        self.image_frame.pack(pady=20)
        
        self.fox_image = None
        self.image_label = ttk.Label(self.image_frame)
        self.image_label.pack()
        
        self.update_button = ttk.Button(
            root, 
            text="Показать другую лису", 
            command=self.update_image
        )
        self.update_button.pack(pady=10)
        
        self.update_image()
    
    def update_image(self):
        try:
            response = requests.get("https://randomfox.ca/floof/")
            response.raise_for_status()
            image_url = response.json()["image"]
            
            image_response = requests.get(image_url)
            image_data = Image.open(BytesIO(image_response.content))
            
            image_data.thumbnail((450, 450))
            self.fox_image = ImageTk.PhotoImage(image_data)
            

            self.image_label.config(image=self.fox_image)
            self.image_label.image = self.fox_image
            
        except Exception as e:
            error_image = Image.new('RGB', (450, 300), color='red')
            error_draw = Image.new('RGB', (450, 300))
            self.fox_image = ImageTk.PhotoImage(error_image)
            self.image_label.config(
                image=self.fox_image, 
                text=f"Ошибка загрузки: {str(e)}", 
                compound='center'
            )
            self.image_label.image = self.fox_image

if __name__ == "__main__":
    root = tk.Tk()
    app = FoxImageGenerator(root)
    root.mainloop()
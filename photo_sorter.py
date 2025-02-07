import os
import shutil
from tkinterdnd2 import TkinterDnD, DND_FILES
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.image import load_img, img_to_array

model = MobileNetV2(weights="imagenet")

def classify_image(image_path):
    img = load_img(image_path, target_size=(224, 224))
    img_array = img_to_array(img)
    img_array = preprocess_input(img_array)
    img_array = img_array[None, ...]
    predictions = model.predict(img_array)
    #change top 1 to an if-else to check if the folder exist
    decoded = decode_predictions(predictions, top=1)
    label = decoded[0][0][1]
    return label

def handle_drop(event):
    files = root.tk.splitlist(event.data)
    for file_path in files:
        if file_path.lower().endswith((".png", ".jpg", ".jpeg")):
            try:
                label = classify_image(file_path)
                target_folder = os.path.join(output_dir, label)
                os.makedirs(target_folder, exist_ok=True)
                shutil.move(file_path, os.path.join(target_folder, os.path.basename(file_path)))
                update_image_preview(file_path, label)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process {file_path}.\n{e}")
        else:
            messagebox.showwarning("Unsupported File", f"{file_path} is not a valid image file.")


def update_image_preview(image_path, label):
    img = Image.open(image_path)
    img.thumbnail((200, 200))
    img_tk = ImageTk.PhotoImage(img)
    image_label.configure(image=img_tk)
    image_label.image = img_tk
    label_var.set(f"Classified as: {label}")

def set_output_directory():
    global output_dir
    output_dir = filedialog.askdirectory()
    if output_dir:
        output_dir_label.config(text=f"Output Directory: {output_dir}")

root = TkinterDnD.Tk()
root.title("Image Sorter")
root.geometry("400x500")

output_dir = os.path.expanduser("~/Desktop/SortedImages")

tk.Label(root, text="Drag and Drop Images Below:", font=("Arial", 14)).pack(pady=10)

drop_frame = tk.Frame(root, width=300, height=200, bg="lightblue", relief="sunken")
drop_frame.pack(pady=10)
drop_frame.pack_propagate(False)

root.drop_target_register(DND_FILES)
root.dnd_bind("<<Drop>>", handle_drop)

image_label = tk.Label(drop_frame, bg="lightblue")
image_label.pack(expand=True)

label_var = tk.StringVar(value="No image classified yet.")
tk.Label(root, textvariable=label_var, font=("Arial", 12)).pack(pady=10)

output_dir_label = tk.Label(root, text=f"Output Directory: {output_dir}", font=("Arial", 10))
output_dir_label.pack(pady=10)

set_output_dir_button = tk.Button(root, text="Set Output Directory", command=set_output_directory)
set_output_dir_button.pack(pady=5)

root.mainloop()

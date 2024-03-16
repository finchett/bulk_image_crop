import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image
import os
import threading
from ctypes import windll

# Fix blurry text on Windows
windll.shcore.SetProcessDpiAwareness(1)

def crop_images_to_ratio(input_folder, output_folder, target_ratio, status_label):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    all_files_processed = False
    
    for filename in os.listdir(input_folder):
        try:
            with Image.open(os.path.join(input_folder, filename)) as img:
                width, height = img.size
                current_ratio = width / height
                if current_ratio < target_ratio:
                    new_height = width / target_ratio
                    left = 0
                    right = width
                    top = (height - new_height) / 2
                    bottom = (height + new_height) / 2
                else:
                    new_width = height * target_ratio
                    left = (width - new_width) / 2
                    right = (width + new_width) / 2
                    top = 0
                    bottom = height

                cropped_img = img.crop((left, top, right, bottom))
                cropped_img.save(os.path.join(output_folder, filename))
                status_label.config(text=f"{filename} cropped successfully.")
        except Exception as e:
            status_label.config(text=f"Error cropping {filename}: {e}")
    
    all_files_processed = True
    if all_files_processed:
        status_label.config(text="Done")

def browse_input_folder():
    folder_path = filedialog.askdirectory()
    input_folder_entry.delete(0, tk.END)
    input_folder_entry.insert(0, folder_path)

def browse_output_folder():
    folder_path = filedialog.askdirectory()
    output_folder_entry.delete(0, tk.END)
    output_folder_entry.insert(0, folder_path)

def crop_images():
    input_folder = input_folder_entry.get()
    output_folder = output_folder_entry.get()
    aspect_ratio_str = aspect_ratio_entry.get()
    
    try:
        aspect_ratio = list(map(float, aspect_ratio_str.split(':')))
        target_ratio = aspect_ratio[0] / aspect_ratio[1]
        
        status_label.config(text="Cropping images...")

        # Execute cropping process in a separate thread
        threading.Thread(target=crop_images_to_ratio, args=(input_folder, output_folder, target_ratio, status_label)).start()
    except ValueError:
        status_label.config(text="Invalid aspect ratio format. Please use 'width:height'.")

def set_aspect_ratio(preset):
    preset_aspect_ratios = {
        "3:4": (3, 4),
        "2:3": (2, 3),
        "4:5": (4, 5),
        "ISO": (1, 1.41421)
    }
    aspect_ratio_entry.delete(0, tk.END)
    aspect_ratio_entry.insert(0, f"{preset_aspect_ratios[preset][0]}:{preset_aspect_ratios[preset][1]}")

# Create GUI
root = tk.Tk()
root.title("Image Cropper")

# Set style
style = ttk.Style()
style.theme_use("vista")  # Modern theme

# Frame for input folder
input_frame = ttk.LabelFrame(root, text="Input Folder", padding=(10, 10))
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

input_folder_entry = ttk.Entry(input_frame)
input_folder_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

input_folder_button = ttk.Button(input_frame, text="Browse", command=browse_input_folder)
input_folder_button.grid(row=0, column=1, padx=5, pady=5)

# Frame for output folder
output_frame = ttk.LabelFrame(root, text="Output Folder", padding=(10, 10))
output_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

output_folder_entry = ttk.Entry(output_frame)
output_folder_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

output_folder_button = ttk.Button(output_frame, text="Browse", command=browse_output_folder)
output_folder_button.grid(row=0, column=1, padx=5, pady=5)

# Frame for aspect ratio
aspect_ratio_frame = ttk.LabelFrame(root, text="Aspect Ratio (width:height)", padding=(10, 10))
aspect_ratio_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

aspect_ratio_entry = ttk.Entry(aspect_ratio_frame)
aspect_ratio_entry.grid(row=0, column=0, padx=5, pady=5)

# Preset aspect ratio buttons
preset_buttons_frame = ttk.Frame(root, padding=(10, 10))
preset_buttons_frame.grid(row=3, column=0, padx=10, pady=10)

preset_buttons = {
    "3:4": ttk.Button(preset_buttons_frame, text="3:4", command=lambda: set_aspect_ratio("3:4")),
    "2:3": ttk.Button(preset_buttons_frame, text="2:3", command=lambda: set_aspect_ratio("2:3")),
    "4:5": ttk.Button(preset_buttons_frame, text="4:5", command=lambda: set_aspect_ratio("4:5")),
    "ISO": ttk.Button(preset_buttons_frame, text="ISO", command=lambda: set_aspect_ratio("ISO"))
}

for i, button in enumerate(preset_buttons.values()):
    button.grid(row=0, column=i, padx=5)

# Status Label
status_label = ttk.Label(root, text="", padding=(10, 10))
status_label.grid(row=4, column=0, padx=10, pady=10)

# Crop Button
crop_button = ttk.Button(root, text="Crop Images", command=crop_images)
crop_button.grid(row=5, column=0, padx=10, pady=10)

# Configure rows and columns to resize with the window
for i in range(6):
    root.grid_rowconfigure(i, weight=1)
root.grid_columnconfigure(0, weight=1)

# Run the GUI
root.mainloop()

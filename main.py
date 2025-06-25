import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import os
from uploader import process_file

DESCRIPTION = "Peter England formal shirt made with premium cotton and modern fit. Ideal for office and events."
COLUMNS = ["Amazon", "Flipkart", "Myntra"]

def get_image_from_cid(cid):
    url = f"https://gateway.pinata.cloud/ipfs/{cid}"
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

def select_file():
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.webp")]
    )
    if not file_path:
        return

    try:
        hash_val, cid = process_file(file_path, DESCRIPTION)
        show_image(cid)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_image(cid):
    img = get_image_from_cid(cid).resize((200, 200))
    tk_img = ImageTk.PhotoImage(img)

    for widget in image_frame.winfo_children():
        widget.destroy()

    for i, col in enumerate(COLUMNS):
        frame = tk.Frame(image_frame, borderwidth=2, relief="ridge", padx=10, pady=10)
        frame.grid(row=0, column=i, padx=10, pady=10)

        tk.Label(frame, text=col, font=("Arial", 14, "bold")).pack()
        tk.Label(frame, image=tk_img).pack(pady=5)
        tk.Label(frame, text="Peter England Formal Shirt", font=("Arial", 12)).pack()
        tk.Label(frame, text=DESCRIPTION, wraplength=180, justify="left", font=("Arial", 10)).pack(pady=5)
        tk.Label(frame, text="₹1,799", font=("Arial", 12, "bold"), fg="green").pack()

    image_frame.image = tk_img  # Prevent garbage collection

# === UI SETUP ===
root = tk.Tk()
root.title("Deduplication E-Commerce Viewer")

tk.Button(root, text="Upload Product Image", command=select_file, font=("Arial", 12)).pack(pady=20)

image_frame = tk.Frame(root)
image_frame.pack()

root.mainloop()

import os
import zlib
import tkinter as tk
from tkinter import filedialog, messagebox

def compress_file(input_file, output_file):
    """Compress a file using zlib"""
    try:
        with open(input_file, 'rb') as f_in:
            with open(output_file, 'wb') as f_out:
                f_out.write(zlib.compress(f_in.read()))
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Error compressing file: {e}")
        return False

def decompress_file(input_file, output_file):
    """Decompress a file using zlib"""
    try:
        with open(input_file, 'rb') as f_in:
            with open(output_file, 'wb') as f_out:
                f_out.write(zlib.decompress(f_in.read()))

        return True
    except Exception as e:
        messagebox.showerror("Error", f"Error decompressing file: {e}")
        return False

def select_file():
    return filedialog.askopenfilename()

def save_file():
    return filedialog.asksaveasfilename()

def compress_action():
    input_file = select_file()
    if not input_file:
        return
    output_file = save_file()
    if not output_file:
        return

    if compress_file(input_file, output_file):
        messagebox.showinfo("Success", "File compressed successfully.")


def decompress_action():
    input_file = select_file()
    if not input_file:
        return
    output_file = save_file()
    if not output_file:
        return

    if decompress_file(input_file, output_file):
        messagebox.showinfo("Success", "File decompressed successfully.")

def main():
    root = tk.Tk()
    root.title("File Compression Tool")

    tk.Label(root, text="File Compression Tool", font=("Arial", 16)).pack(pady=10)

    compress_button = tk.Button(root, text="Compress File", command=compress_action, width=20, bg="lightblue")
    compress_button.pack(pady=5)

    decompress_button = tk.Button(root, text="Decompress File", command=decompress_action, width=20, bg="lightgreen")
    decompress_button.pack(pady=5)

    exit_button = tk.Button(root, text="Exit", command=root.quit, width=20, bg="red")
    exit_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()

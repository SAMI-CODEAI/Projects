import os
import zlib
import tkinter as tk
from tkinter import filedialog, messagebox


def compress_file(input_file, output_file):
    """Compress a .txt file using zlib and save it with a .txt extension."""
    try:
        # Open the file in text mode, read all text content
        with open(input_file, 'rt', encoding='utf-8') as f_in:
            content = f_in.read()

        # Compress the content using zlib (encode to bytes before compression)
        compressed_data = zlib.compress(content.encode('utf-8'))

        # Write compressed data to output file (in binary mode)
        with open(output_file, 'wb') as f_out:
            f_out.write(compressed_data)

        return True
    except Exception as e:
        messagebox.showerror("Error", f"Error compressing file: {e}")
        return False


def decompress_file(input_file, output_file):
    """Decompress a .txt file using zlib and save it with a .txt extension."""
    try:
        # Open the compressed file in binary mode
        with open(input_file, 'rb') as f_in:
            compressed_data = f_in.read()

        # Decompress the content (decode from bytes to string)
        content = zlib.decompress(compressed_data).decode('utf-8')

        # Write the decompressed content to the output file in text mode
        with open(output_file, 'wt', encoding='utf-8') as f_out:
            f_out.write(content)

        return True
    except Exception as e:
        messagebox.showerror("Error", f"Error decompressing file: {e}")
        return False


def select_file():
    """Open file dialog to select a .txt file."""
    return filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])


def save_file(input_file):
    """Open a save dialog to save the file with a .txt extension."""
    base_name = os.path.splitext(input_file)[0]
    return filedialog.asksaveasfilename(defaultextension=".txt", initialfile=base_name + ".txt",
                                        filetypes=[("Text Files", "*.txt")])


def compress_action():
    """Compress the selected .txt file."""
    input_file = select_file()
    if not input_file:
        return
    output_file = save_file(input_file)  # Save the compressed file with .txt extension
    if not output_file:
        return

    if compress_file(input_file, output_file):
        messagebox.showinfo("Success", "File compressed successfully.")


def decompress_action():
    """Decompress the selected .txt file."""
    input_file = select_file()
    if not input_file:
        return
    output_file = save_file(input_file)  # Save the decompressed file with .txt extension
    if not output_file:
        return

    if decompress_file(input_file, output_file):
        messagebox.showinfo("Success", "File decompressed successfully.")


def main():
    """Initialize the GUI and buttons."""
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

import tkinter as tk
from tkinter import PhotoImage, filedialog
import heapq
import os
import tkinter.messagebox as messagebox

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    freq_map = {}
    for char in text:
        if char in freq_map:
            freq_map[char] += 1
        else:
            freq_map[char] = 1

    priority_queue = [HuffmanNode(char, freq) for char, freq in freq_map.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)

        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)

    return priority_queue[0]

def build_huffman_codes(root, current_code, huffman_codes):
    if root is None:
        return

    if root.char is not None:
        huffman_codes[root.char] = current_code
        return

    build_huffman_codes(root.left, current_code + '0', huffman_codes)
    build_huffman_codes(root.right, current_code + '1', huffman_codes)

def compress(text):
    if len(text) == 0:
        return '', None

    huffman_root = build_huffman_tree(text)
    huffman_codes = {}
    build_huffman_codes(huffman_root, '', huffman_codes)

    encoded_text = ''.join(huffman_codes[char] for char in text)

    # Convert encoded text to bytes for efficient storage
    encoded_bytes = bytearray()
    for i in range(0, len(encoded_text), 8):
        byte = encoded_text[i:i + 8]
        encoded_bytes.append(int(byte, 2))

    return bytes(encoded_bytes), huffman_root

def decompress(encoded_text, huffman_root):
    if huffman_root is None or len(encoded_text) == 0:
        return ''

    current = huffman_root
    decoded_text = ''

    # Convert bytes back to binary string
    binary_encoded_text = ''.join(format(byte, '08b') for byte in encoded_text)

    for bit in binary_encoded_text:
        if bit == '0':
            current = current.left
        else:
            current = current.right

        if current.char is not None:
            decoded_text += current.char
            current = huffman_root

    return decoded_text

class HuffmanCompressorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Huffman Compressor")

        self.text_label = tk.Label(root, text="Select a file to compress:")
        self.text_label.pack()

        self.compress_button = tk.Button(root, text="Compress File", command=self.compress_file, bg="blue", fg="white", relief=tk.GROOVE)
        self.compress_button.pack(pady=5)

        self.decompress_button = tk.Button(root, text="Decompress File", command=self.decompress_file, bg="green", fg="white", relief=tk.GROOVE)
        self.decompress_button.pack(pady=5)

    def compress_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                text = file.read()

                encoded_text, huffman_root = compress(text)

                compressed_file_path = filedialog.asksaveasfilename(defaultextension=".bin")
                if compressed_file_path:
                    with open(compressed_file_path, 'wb') as compressed_file:
                        compressed_file.write(encoded_text)

                    messagebox.showinfo("Compression", "File compressed successfully!")

    def decompress_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Binary files", "*.bin")])
        if file_path:
            with open(file_path, 'rb') as file:
                encoded_text = file.read()

                decompressed_text = decompress(encoded_text, None)  # For demonstration, pass None as huffman_root

                decompressed_file_path = filedialog.asksaveasfilename(defaultextension=".txt")
                if decompressed_file_path:
                    with open(decompressed_file_path, 'w') as decompressed_file:
                        decompressed_file.write(decompressed_text)

                    messagebox.showinfo("Decompression", "File decompressed successfully!")

def main():
    root = tk.Tk()
    app = HuffmanCompressorApp(root)
    image_icon = PhotoImage(file="icon.png")
    root.iconphoto(False, image_icon)
    root.geometry("350x150")  # Change the values as needed (width x height)
    root.resizable(False, False)
    root.mainloop()

if __name__ == "__main__":
    main()
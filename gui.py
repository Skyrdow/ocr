import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

from processor import transcribe_and_translate
from rasterize import rasterize_pdf


class OCRGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OCR PDF Processor")
        self.root.geometry("700x600")
        self.root.configure(bg="#f0f0f0")

        # Style
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 10), padding=5)
        style.configure("TLabel", font=("Arial", 10), background="#f0f0f0")
        style.configure("TCheckbutton", font=("Arial", 10), background="#f0f0f0")

        # Input PDF
        ttk.Label(root, text="Input PDF:").grid(
            row=0, column=0, sticky="w", padx=10, pady=5
        )
        self.input_entry = ttk.Entry(root, width=50)
        self.input_entry.grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(root, text="Browse", command=self.browse_input).grid(
            row=0, column=2, padx=10, pady=5
        )

        # Output Path
        ttk.Label(root, text="Output File (.txt):").grid(
            row=1, column=0, sticky="w", padx=10, pady=5
        )
        self.output_entry = ttk.Entry(root, width=50)
        self.output_entry.grid(row=1, column=1, padx=10, pady=5)
        ttk.Button(root, text="Browse", command=self.browse_output).grid(
            row=1, column=2, padx=10, pady=5
        )

        # Rasterize Option
        self.rasterize_var = tk.BooleanVar()
        ttk.Checkbutton(
            root, text="Rasterize PDF (simulate scan)", variable=self.rasterize_var
        ).grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=5)
        ttk.Label(root, text="DPI:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.dpi_entry = ttk.Entry(root, width=10)
        self.dpi_entry.insert(0, "200")
        self.dpi_entry.grid(row=3, column=1, sticky="w", padx=10, pady=5)

        # Progress Bar
        self.progress = ttk.Progressbar(root, orient="horizontal", mode="indeterminate")
        self.progress.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Process Button
        self.process_btn = ttk.Button(
            root, text="Process PDF", command=self.start_processing
        )
        self.process_btn.grid(row=5, column=0, columnspan=3, pady=10)

        # Log Area
        ttk.Label(root, text="Log/Results:").grid(
            row=6, column=0, sticky="w", padx=10, pady=5
        )
        self.log_text = scrolledtext.ScrolledText(
            root, width=80, height=15, font=("Courier", 9)
        )
        self.log_text.grid(row=7, column=0, columnspan=3, padx=10, pady=5)

    def browse_input(self):
        filename = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if filename:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, filename)

    def browse_output(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text files", "*.txt")]
        )
        if filename:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, filename)

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def start_processing(self):
        input_path = self.input_entry.get()
        output_path = self.output_entry.get()
        rasterize = self.rasterize_var.get()
        dpi = int(self.dpi_entry.get())

        if not input_path or not os.path.exists(input_path):
            messagebox.showerror("Error", "Please select a valid input PDF file.")
            return

        if not output_path:
            input_dir = os.path.dirname(input_path)
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            output_path = os.path.join(input_dir, f"ocr-{base_name}.txt")
            self.output_entry.insert(0, output_path)

        self.log("Starting processing...")
        self.process_btn.config(state="disabled")
        self.progress.start()
        threading.Thread(
            target=self.process_pdf, args=(input_path, output_path, rasterize, dpi)
        ).start()

    def process_pdf(self, input_path, output_path, rasterize, dpi):
        try:
            if rasterize:
                self.log(f"Rasterizing PDF at {dpi} DPI...")
                rasterized_path = input_path.replace(".pdf", "_scanned.pdf")
                rasterize_pdf(input_path, rasterized_path, dpi)
                input_path = rasterized_path
                self.log("Rasterization complete.")

            self.log("Transcribing and translating PDF...")
            result = transcribe_and_translate(input_path)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result)

            self.log(f"Processing complete. Output saved to {output_path}")
            self.log(
                "Results:\n" + result[:500] + "..." if len(result) > 500 else result
            )

        except Exception as e:
            self.log(f"Error: {e}")
            messagebox.showerror("Error", str(e))
        finally:
            self.process_btn.config(state="normal")
            self.progress.stop()


if __name__ == "__main__":
    root = tk.Tk()
    app = OCRGUI(root)
    root.mainloop()

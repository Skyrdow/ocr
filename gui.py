import sys
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from PIL import Image, ImageTk
from rasterize import rasterize_pdf

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class OCRGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Procesador PDF OCR")
        self.root.geometry("700x600")
        
        # Colors
        self.BG_COLOR = "#FFFFFF"
        self.PRIMARY_COLOR = "#00a499" # Teal
        self.SECONDARY_COLOR = "#ea7600" # Orange
        self.DARK_COLOR = "#394049" # Dark Grey
        
        self.root.configure(bg=self.BG_COLOR)

        # Style
        style = ttk.Style()
        style.theme_use('clam') # Use clam for better color customization
        
        style.configure("TFrame", background=self.BG_COLOR)
        style.configure("TLabel", font=("Arial", 10), background=self.BG_COLOR, foreground=self.DARK_COLOR)
        style.configure("TButton", font=("Arial", 10, "bold"), background=self.PRIMARY_COLOR, foreground="white", borderwidth=0, focuscolor=self.SECONDARY_COLOR)
        style.map("TButton", background=[("active", self.SECONDARY_COLOR)])
        style.configure("TRadiobutton", font=("Arial", 10), background=self.BG_COLOR, foreground=self.DARK_COLOR)
        
        # Main Frame to hold everything
        main_frame = ttk.Frame(root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # --- Header (Logo) ---
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 20))
        header_frame.columnconfigure(1, weight=1) # Make center column expand
        
        try:
            # Load Logo
            logo_path = resource_path(os.path.join("imagotipo", "drii_0.png"))
            if os.path.exists(logo_path):
                pil_image = Image.open(logo_path)
                # Resize if too big (optional, roughly header size)
                pil_image.thumbnail((200, 80)) 
                self.logo_img = ImageTk.PhotoImage(pil_image)
                logo_label = ttk.Label(header_frame, image=self.logo_img)
                logo_label.grid(row=0, column=0, sticky="w", padx=5)
            else:
                ttk.Label(header_frame, text="[Logo no encontrado]", foreground="red").grid(row=0, column=0, sticky="w")
        except Exception as e:
            print(f"Error loading logo: {e}")

        # App Name Label
        ttk.Label(
            header_frame, 
            text="OCR Convenios", 
            font=("Arial", 16, "bold"), 
            foreground=self.PRIMARY_COLOR,
            anchor="center"
        ).grid(row=0, column=1, sticky="ew", padx=5) # Center in remaining space

        # --- Content ---

        # Input PDF
        ttk.Label(main_frame, text="PDF de entrada:").grid(
            row=1, column=0, sticky="w", padx=10, pady=10
        )
        self.input_entry = ttk.Entry(main_frame, width=50)
        self.input_entry.grid(row=1, column=1, padx=10, pady=10)
        ttk.Button(main_frame, text="Explorar", command=self.browse_input).grid(
            row=1, column=2, padx=10, pady=10
        )

        # Output Path
        ttk.Label(main_frame, text="Archivo de salida:").grid(
            row=2, column=0, sticky="w", padx=10, pady=10
        )
        self.output_entry = ttk.Entry(main_frame, width=50)
        self.output_entry.grid(row=2, column=1, padx=10, pady=10)
        ttk.Button(main_frame, text="Explorar", command=self.browse_output).grid(
            row=2, column=2, padx=10, pady=10
        )

        # Output Format
        ttk.Label(main_frame, text="Formato de salida:").grid(
            row=3, column=0, sticky="w", padx=10, pady=10
        )
        self.format_var = tk.StringVar(value="docx")
        format_frame = ttk.Frame(main_frame)
        format_frame.grid(row=3, column=1, columnspan=2, sticky="w", padx=10, pady=10)
        
        ttk.Radiobutton(format_frame, text="Word (.docx)", variable=self.format_var, value="docx").pack(side="left", padx=10)
        ttk.Radiobutton(format_frame, text="PDF (.pdf)", variable=self.format_var, value="pdf").pack(side="left", padx=10)

        # Progress Bar
        self.progress = ttk.Progressbar(main_frame, orient="horizontal", mode="indeterminate")
        self.progress.grid(row=4, column=0, columnspan=3, padx=10, pady=20, sticky="ew")

        # Process Button
        self.process_btn = ttk.Button(
            main_frame, text="PROCESAR PDF", command=self.start_processing
        )
        self.process_btn.grid(row=5, column=0, columnspan=3, pady=10)

        # Log Area
        ttk.Label(main_frame, text="Registro/Resultados:").grid(
            row=6, column=0, sticky="w", padx=10, pady=5
        )
        self.log_text = scrolledtext.ScrolledText(
            main_frame, width=70, height=15, font=("Courier", 9), relief="flat", borderwidth=1
        )
        self.log_text.grid(row=7, column=0, columnspan=3, padx=10, pady=5)
        # Add a border frame for log text because flat relief might be too invisible
        self.log_text.config(background="#f5f5f5")

    def browse_input(self):
        filename = filedialog.askopenfilename(filetypes=[("Archivos PDF", "*.pdf")])
        if filename:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, filename)

    def browse_output(self):
        current_format = self.format_var.get()
        ext = f".{current_format}"
        filename = filedialog.asksaveasfilename(
            defaultextension=ext, filetypes=[(f"Archivos {current_format.upper()}", f"*{ext}")]
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
        # Removed rasterize and dpi vars
        output_format = self.format_var.get()

        if not input_path or not os.path.exists(input_path):
            messagebox.showerror("Error", "Por favor seleccione un archivo PDF de entrada válido.")
            return

        if not output_path:
            input_dir = os.path.dirname(input_path)
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            output_path = os.path.join(input_dir, f"ocr-{base_name}.{output_format}")
            self.output_entry.insert(0, output_path)
            
        # Ensure output path has correct extension
        if not output_path.lower().endswith(f".{output_format}"):
             output_path = os.path.splitext(output_path)[0] + f".{output_format}"
             self.output_entry.delete(0, tk.END)
             self.output_entry.insert(0, output_path)

        self.log("Iniciando procesamiento...")
        self.process_btn.config(state="disabled")
        self.progress.start()
        threading.Thread(
            target=self.process_pdf, args=(input_path, output_path, output_format)
        ).start()

    def process_pdf(self, input_path, output_path, output_format):
        try:
            # Removed rasterize logic
            
            self.log("Transcribiendo y traduciendo PDF...")

            from processor import transcribe_and_translate, save_to_file
            
            result = transcribe_and_translate(input_path)

            save_to_file(result, output_path, output_format)

            self.log(f"Procesamiento completo. Salida guardada en {output_path}")
            self.log(
                "Resultados:\n" + result[:500] + "..." if len(result) > 500 else result
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

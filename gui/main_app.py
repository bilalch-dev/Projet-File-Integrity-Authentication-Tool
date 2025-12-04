import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time

# --- Setup Project Path ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# --- Import Logic or Dummy for Testing ---
try:
    from crypto_core import aes_protection
except ImportError:
    class aes_protection:
        @staticmethod
        def file_encryption(i, o, p): time.sleep(2)
        @staticmethod
        def file_decryption(i, o, p): 
            time.sleep(2)
            # Simulate an error for testing if password is "wrong"
            if p == "wrong": raise ValueError("MAC check failed")

# --- VISUAL THEME DEFINITION ---
# UPDATED: Switched to "Courier New" for a futuristic/terminal aesthetic
THEME_COLORS = {
    "bg_root": "#050505",       # Deep Black
    "bg_input": "#141414",      # Dark Grey
    "accent": "#00E5FF",        # Electric Cyan
    "text_main": "#FFFFFF",     # White
    "text_dim": "#808080",      # Grey
    "font_primary": ("Courier New", 10),
    "font_header": ("Courier New", 20, "bold"),
    "font_label": ("Courier New", 10, "bold"),
    "font_button": ("Courier New", 11, "bold")
}

class SecureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Encryption Tool")
        self.root.geometry("680x580")
        self.root.minsize(600, 500)
        
        # Variables
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.password = tk.StringVar()
        self.show_password = tk.BooleanVar()
        self.status_msg = tk.StringVar(value="Ready")

        self.apply_theme()
        self.build_ui()

    def apply_theme(self):
        style = ttk.Style()
        style.theme_use('clam')
        c = THEME_COLORS
        
        # Global Backgrounds
        self.root.configure(bg=c["bg_root"])
        style.configure("TFrame", background=c["bg_root"])
        
        # Inputs
        style.configure("TEntry", 
                        fieldbackground=c["bg_input"],
                        foreground=c["accent"],
                        insertcolor=c["accent"],
                        borderwidth=0)

        # Primary Buttons (Solid Cyan)
        style.configure("Primary.TButton", 
                        background=c["accent"], 
                        foreground="#000000", 
                        borderwidth=0,
                        font=c["font_button"])
        style.map("Primary.TButton", 
                  background=[("active", c["text_main"])], 
                  foreground=[("active", "#000000")])

        # Secondary/Browse Buttons (Outline)
        style.configure("Secondary.TButton", 
                        background=c["bg_root"], 
                        foreground=c["accent"], 
                        bordercolor=c["accent"], 
                        borderwidth=1,
                        font=("Courier New", 9))
        style.map("Secondary.TButton", 
                  background=[("active", c["accent"])], 
                  foreground=[("active", c["bg_root"])])

        # Progress Bar
        style.configure("Cyan.Horizontal.TProgressbar", 
                        troughcolor=c["bg_input"], 
                        background=c["accent"], 
                        thickness=4, 
                        borderwidth=0)

    def build_ui(self):
        c = THEME_COLORS
        # Clean padding layout
        main = ttk.Frame(self.root, padding="40 30 40 40")
        main.pack(fill=tk.BOTH, expand=True)

        # --- Header ---
        header_lbl = tk.Label(main, text="SECURE FILE ENCRYPTION", 
                              bg=c["bg_root"], fg=c["text_main"], 
                              font=c["font_header"], anchor="w")
        header_lbl.pack(fill=tk.X, pady=(0, 30)) # More space after header

        # --- Fields Container ---
        
        # 1. Input Field
        self.create_file_field(main, "INPUT SOURCE PATH", self.input_path, self.browse_input)

        # 2. Output Field
        self.create_file_field(main, "OUTPUT DESTINATION", self.output_path, self.browse_output)

        # 3. Password Field
        pass_container = ttk.Frame(main)
        pass_container.pack(fill=tk.X, pady=(0, 25))

        # Label
        tk.Label(pass_container, text="ENCRYPTION KEY", 
                 bg=c["bg_root"], fg=c["accent"], 
                 font=c["font_label"], anchor="w").pack(fill=tk.X, pady=(0, 8))
        
        # Input Area
        pass_inner = ttk.Frame(pass_container)
        pass_inner.pack(fill=tk.X)
        
        # Updated font to Courier New
        self.pass_entry = ttk.Entry(pass_inner, textvariable=self.password, show="•", font=("Courier New", 12))
        self.pass_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15))
        
        # Updated font to Courier New
        tk.Checkbutton(pass_inner, text="Reveal", variable=self.show_password, command=self.toggle_pass,
                       bg=c["bg_root"], fg=c["text_dim"], selectcolor=c["bg_input"], 
                       activebackground=c["bg_root"], activeforeground=c["accent"],
                       font=("Courier New", 9)).pack(side=tk.LEFT)

        # --- Action Buttons ---
        action_grid = ttk.Frame(main)
        action_grid.pack(fill=tk.X, pady=(10, 0))
        action_grid.columnconfigure(0, weight=1)
        action_grid.columnconfigure(1, weight=1)

        b1 = ttk.Button(action_grid, text="ENCRYPT DATA", style="Primary.TButton", command=lambda: self.process("encrypt"))
        b1.grid(row=0, column=0, sticky="ew", padx=(0, 10), ipady=12)

        b2 = ttk.Button(action_grid, text="DECRYPT DATA", style="Primary.TButton", command=lambda: self.process("decrypt"))
        b2.grid(row=0, column=1, sticky="ew", padx=(10, 0), ipady=12)

        # --- Status Bar ---
        self.progress = ttk.Progressbar(main, mode='indeterminate', style="Cyan.Horizontal.TProgressbar")
        self.progress.pack(fill=tk.X, pady=(30, 10))

        tk.Label(main, textvariable=self.status_msg, bg=c["bg_root"], fg=c["text_dim"], font=("Courier New", 9)).pack(anchor="w")

    def create_file_field(self, parent, label_text, var, cmd):
        """Helper to create a Label + Entry + Button row"""
        container = ttk.Frame(parent)
        container.pack(fill=tk.X, pady=(0, 20))

        # The Field Name
        lbl = tk.Label(container, text=label_text, 
                       bg=THEME_COLORS["bg_root"], 
                       fg=THEME_COLORS["accent"], 
                       font=THEME_COLORS["font_label"], anchor="w")
        lbl.pack(fill=tk.X, pady=(0, 8))
        
        # The Input Row
        row = ttk.Frame(container)
        row.pack(fill=tk.X)
        
        ttk.Entry(row, textvariable=var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(row, text="BROWSE", style="Secondary.TButton", command=cmd).pack(side=tk.LEFT)

    def toggle_pass(self):
        self.pass_entry.config(show="" if self.show_password.get() else "•")

    def browse_input(self):
        f = filedialog.askopenfilename()
        if f:
            self.input_path.set(f)
            filename = os.path.basename(f)
            directory = os.path.dirname(f)
            
            if filename.endswith(".aeg"):
                # Decrypt: input.pdf.aeg -> decrypted_input.pdf
                new_name = f"decrypted_{filename[:-4]}"
            else:
                # Encrypt: input.pdf -> encrypted_input.pdf.aeg
                new_name = f"encrypted_{filename}.aeg"
            
            self.output_path.set(os.path.join(directory, new_name))

    def browse_output(self):
        initial_name = "output_file"
        if self.input_path.get():
            filename = os.path.basename(self.input_path.get())
            if filename.endswith(".aeg"):
                # Decrypt: input.pdf.aeg -> decrypted_input.pdf
                initial_name = f"decrypted_{filename[:-4]}"
            else:
                # Encrypt: input.pdf -> encrypted_input.pdf.aeg
                initial_name = f"encrypted_{filename}.aeg"

        f = filedialog.asksaveasfilename(initialfile=initial_name)
        if f: self.output_path.set(f)

    def process(self, mode):
        # Basic validation before starting thread
        if not self.input_path.get() or not self.output_path.get():
            messagebox.showerror("Error", "Please select input and output files.")
            return
        
        if not self.password.get():
            if not messagebox.askyesno("Warning", "No password provided. Continue?"):
                return
        
        self.progress.start(10)
        self.status_msg.set(f"Executing {mode.upper()}...")
        
        t = threading.Thread(target=self.run_crypto, args=(mode,))
        t.daemon = True
        t.start()

    def run_crypto(self, mode):
        i, o, p = self.input_path.get(), self.output_path.get(), self.password.get()
        try:
            if mode == "encrypt":
                aes_protection.file_encryption(i, o, p)
            else:
                aes_protection.file_decryption(i, o, p)
            
            # Successful completion
            self.root.after(0, lambda: self.finish(True))
            
        except Exception as e:
            # --- ERROR HANDLING LOGIC ---
            error_message = str(e)
            
            if mode == "decrypt":
                # Most crypto libs raise ValueError (Padding/MAC) or specific KeyErrors
                # We assume ANY error during decrypt is likely a password or corruption issue
                suggestion = "DECRYPTION FAILED!\n\nPossible reasons:\n1. INCORRECT PASSWORD (Most Likely)\n2. Corrupted file\n3. Not an encrypted file"
                full_error = f"{suggestion}\n\nTechnical Error: {error_message}"
            else:
                full_error = f"Encryption Failed.\nError: {error_message}"

            self.root.after(0, lambda: self.finish(False, full_error))

    def finish(self, success, msg=None):
        self.progress.stop()
        if success:
            self.status_msg.set("Operation Successful")
            messagebox.showinfo("Success", "Process Complete")
            self.password.set("") # Clear password for security
        else:
            self.status_msg.set("Operation Failed")
            messagebox.showerror("Error", msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = SecureApp(root)
    root.mainloop()
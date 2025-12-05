import tkinter as tk
from tkinter import ttk, messagebox
from aes_protection_gui import SecureApp

# --- THEME DEFINITION (Reused for consistency) ---
THEME_COLORS = {
    "bg_root": "#050505",       
    "bg_input": "#141414",      
    "accent": "#00E5FF",        
    "text_main": "#FFFFFF",     
    "font_header": ("Courier New", 24, "bold"),
    "font_button": ("Courier New", 14, "bold")
}

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("CyberSecurity Suite")
        self.root.geometry("600x450")
        
        self.apply_theme()
        self.build_ui()

    def apply_theme(self):
        style = ttk.Style()
        style.theme_use('clam')
        c = THEME_COLORS
        
        self.root.configure(bg=c["bg_root"])
        
        # Large Main Menu Button Style
        style.configure("Menu.TButton", 
                        background=c["bg_input"], 
                        foreground=c["accent"], 
                        bordercolor=c["accent"], 
                        borderwidth=2,
                        font=c["font_button"],
                        anchor="center")
        
        style.map("Menu.TButton", 
                  background=[("active", c["accent"])], 
                  foreground=[("active", c["bg_root"])])

    def build_ui(self):
        c = THEME_COLORS
        
        # Main Container
        container = tk.Frame(self.root, bg=c["bg_root"])
        container.pack(expand=True, fill='both', padx=60, pady=60)
        
        # Title
        tk.Label(container, text="SELECT MODULE", 
                 bg=c["bg_root"], fg=c["text_main"], 
                 font=c["font_header"]).pack(pady=(0, 50))

        # --- Option 1: Encryption ---
        # This redirects to the file encryption interface
        btn_encrypt = ttk.Button(container, text="FILE ENCRYPTION", style="Menu.TButton", 
                                 command=self.load_encryption_interface)
        btn_encrypt.pack(fill=tk.X, ipady=15, pady=15)

        # --- Option 2: Signature ---
        # This redirects to nothing (placeholder)
        btn_sign = ttk.Button(container, text="FILE SIGNATURE", style="Menu.TButton", 
                              command=self.load_signature_interface)
        btn_sign.pack(fill=tk.X, ipady=15, pady=15)

    def load_encryption_interface(self):
        """Clears the main menu and loads the SecureApp interface."""
        # 1. Clear current widgets (remove Main Menu)
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 2. Initialize the Encryption Interface (from gui_layout.py)
        # This class will automatically resize the window and build its own UI
        SecureApp(self.root)

    def load_signature_interface(self):
        """Placeholder for future configuration."""
        # Currently does nothing, or you can print to console
        print("Signature interface selected - Pending configuration.")
        # Optional: messagebox.showinfo("Info", "Module coming soon.")

def main():
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()
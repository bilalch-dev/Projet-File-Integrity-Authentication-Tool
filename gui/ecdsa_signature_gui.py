# gui/app.py
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import threading
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from crypto_core import (
    HashGeneration, ECDSA_KeyGeneration, Load_PrivateKey, Load_PublicKey,
    Sign_hash, save_signature, Load_signature, Verify_Signature,
    PRIVATE_KEY_PATH, PUBLIC_KEY_PATH
)

class IntegrityApp:
    def __init__(self, root, on_back=None):
        self.root = root
        self.on_back = on_back
        self.build_ui()

    def build_ui(self):
        self.root.title("🛡️ FILE INTEGRITY & AUTHENTICATION TOOL")
        self.root.geometry("750x480") # Slightly increased height for better spacing
        self.root.configure(bg="#000000")
        self.setup_ui()

    def setup_ui(self):
        # Titre
        tk.Label(
            self.root,
            text="SECURE FILE INTEGRITY & AUTHENTICATION",
            font=("Courier", 14, "bold"),
            fg="#00FFFF",
            bg="#000000"
        ).pack(pady=(20, 20))

        tk.Label(
            self.root,
            text="INPUT SOURCE PATH",
            font=("Courier", 10),
            fg="#00FFFF",
            bg="#000000",
            anchor="w"
        ).pack(pady=(5, 5), padx=50, anchor="w")

        frame_input = tk.Frame(self.root, bg="#000000")
        frame_input.pack(padx=50, fill=tk.X)

        self.entry_input = tk.Entry(
            frame_input,
            width=60,
            font=("Courier", 10),
            bg="#111111",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            relief=tk.SUNKEN,
            bd=2,
            highlightthickness=1,
            highlightcolor="#FFFFFF"
        )
        self.entry_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        btn_browse = tk.Button(
            frame_input,
            text="BROWSE",
            font=("Courier", 9, "bold"),
            bg="#00FFFF",
            fg="#000000",
            activebackground="#00DDDD",
            relief=tk.RAISED,
            bd=1,
            padx=10
        )
        btn_browse.config(command=self.browse_file)
        btn_browse.pack(side=tk.RIGHT)

        # Boutons
        btn_frame = tk.Frame(self.root, bg="#000000")
        btn_frame.pack(pady=30)

        btn_gen = tk.Button(
            btn_frame,
            text="🔑 Generate Keys",
            font=("Courier", 10, "bold"),
            bg="#333333",
            fg="#00FFFF",
            activebackground="#222222",
            relief=tk.RAISED,
            bd=1,
            padx=15,
            pady=8
        )
        btn_gen.config(command=self.generate_keys)
        btn_gen.grid(row=0, column=0, padx=15)

        btn_sign = tk.Button(
            btn_frame,
            text="SIGN DATA",
            font=("Courier", 11, "bold"),
            bg="#00FFFF",
            fg="#000000",
            activebackground="#00DDDD",
            relief=tk.RAISED,
            bd=1,
            padx=30,
            pady=10
        )
        btn_sign.config(command=self.start_sign)
        btn_sign.grid(row=0, column=1, padx=15)

        btn_verify = tk.Button(
            btn_frame,
            text="VERIFY DATA",
            font=("Courier", 11, "bold"),
            bg="#00FFFF",
            fg="#000000",
            activebackground="#00DDDD",
            relief=tk.RAISED,
            bd=1,
            padx=30,
            pady=10
        )
        btn_verify.config(command=self.start_verify)
        btn_verify.grid(row=0, column=2, padx=15)

        # Barre de progression + statut
        self.progress_bar = tk.Canvas(self.root, height=6, bg="#111111", bd=0, highlightthickness=0)
        self.progress_bar.pack(fill=tk.X, padx=50, pady=(25, 5))
        self.progress_fill = self.progress_bar.create_rectangle(0, 0, 0, 6, fill="#00FFFF", outline="")

        self.status_label = tk.Label(
            self.root,
            text="Ready",
            font=("Courier", 8),
            fg="#00FFCC",
            bg="#000000"
        )
        self.status_label.pack(pady=(5, 10))

        # --- Bottom controls (Back Button) ---
        # Fixed: Background is black, button uses tk.Button to match this class's style
        controls = tk.Frame(self.root, bg="#000000")
        controls.pack(side="bottom", fill="x", pady=(0, 20))

        back_btn = tk.Button(
            controls, 
            text="< RETURN TO MENU", 
            command=self._on_back,
            font=("Courier", 10, "bold"),
            bg="#000000",             # Black background
            fg="#00FFFF",             # Cyan text
            activebackground="#00FFFF", # Invert on hover
            activeforeground="#000000",
            relief=tk.RAISED,
            bd=1,
            padx=10,
            pady=5
        )
        back_btn.pack(side="left", padx=50)

    # --- Méthodes inchangées (browse_file, update_progress, etc.) ---
    def browse_file(self):
        path = filedialog.askopenfilename(title="Sélectionner un fichier")
        if path:
            self.entry_input.delete(0, tk.END)
            self.entry_input.insert(0, path)

    def update_progress(self, value):
        self.root.after(10, lambda v=value: self._update_progress_now(v))

    def _update_progress_now(self, value):
        width = self.progress_bar.winfo_width()
        if width > 10:
            x = int(width * value)
            self.progress_bar.coords(self.progress_fill, 0, 0, x, 6)

    def generate_keys(self):
        try:
            private_path, public_path = ECDSA_KeyGeneration()
            self.status_label.config(
                text=f"✅ Keys generated: {os.path.basename(private_path)}",
                fg="#00FFCC"
            )
        except Exception as e:
            self.status_label.config(
                text=f"❌ Key gen failed: {str(e)}",
                fg="#FF5555"
            )

    def start_sign(self):
        passwd = self.ask_password_dialog("🔐 Private Key Password", "Enter password:")
        if not passwd:
            self.status_label.config(text="⚠️ Cancelled", fg="#FFFF55")
            return
        file_path = self.entry_input.get().strip()
        if not file_path:
            self.status_label.config(text="❌ Input path required", fg="#FF5555")
            return
        self.update_progress(0.1)
        self.status_label.config(text="Signing...", fg="#FFFFAA")
        threading.Thread(target=self.sign_file, args=(passwd,), daemon=True).start()

    def start_verify(self):
        file_path = self.entry_input.get().strip()
        if not file_path:
            self.status_label.config(text="❌ Input path required", fg="#FF5555")
            return
        self.update_progress(0.1)
        self.status_label.config(text="Verifying...", fg="#FFFFAA")
        threading.Thread(target=self.verify_file, daemon=True).start()

    def ask_password_dialog(self, title, prompt):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x150")
        dialog.configure(bg="#000000")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)

        tk.Label(
            dialog,
            text=prompt,
            font=("Courier", 10),
            fg="#00FFFF",
            bg="#000000",
            anchor="w"
        ).pack(pady=(20, 5), padx=20, anchor="w")

        entry = tk.Entry(
            dialog,
            width=40,
            font=("Courier", 10),
            bg="#111111",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            relief=tk.SUNKEN,
            bd=2,
            highlightthickness=1,
            highlightcolor="#FFFFFF",
            show="*"
        )
        entry.pack(pady=(0, 15), padx=20, fill=tk.X)

        btn_frame = tk.Frame(dialog, bg="#000000")
        btn_frame.pack(pady=(0, 10))

        result = [None]

        def on_ok():
            result[0] = entry.get().strip()
            dialog.destroy()

        def on_cancel():
            dialog.destroy()

        tk.Button(
            btn_frame,
            text="OK",
            font=("Courier", 9, "bold"),
            bg="#00FFFF",
            fg="#000000",
            activebackground="#00DDDD",
            relief=tk.RAISED,
            bd=1,
            padx=15,
            command=on_ok
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            btn_frame,
            text="Cancel",
            font=("Courier", 9, "bold"),
            bg="#333333",
            fg="#FFFFFF",
            activebackground="#222222",
            relief=tk.RAISED,
            bd=1,
            padx=15,
            command=on_cancel
        ).pack(side=tk.RIGHT, padx=10)

        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (dialog.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        self.root.wait_window(dialog)
        return result[0]

    def sign_file(self, passwd):
        try:
            file_path = self.entry_input.get().strip()
            file_hash = HashGeneration(file_path)
            if not file_hash:
                raise Exception("File not found")
            private_key = Load_PrivateKey(PRIVATE_KEY_PATH, passwd.encode())
            if not private_key:
                raise Exception("Invalid password or key")
            signature_b64 = Sign_hash(private_key, file_hash)
            if not signature_b64:
                raise Exception("Signature failed")
            sig_path = save_signature(file_path, signature_b64)
            if not sig_path:
                raise Exception("Save failed")
            self.root.after(0, lambda: self.update_progress(1.0))
            self.root.after(0, lambda: self.status_label.config(
                text=f"✅ Signed → {os.path.basename(sig_path)}",
                fg="#00FFCC"
            ))
        except Exception as e:
            self.root.after(0, lambda e=e: self.status_label.config(
                text=f"❌ {str(e)}",
                fg="#FF5555"
            ))

    def verify_file(self):
        try:
            file_path = self.entry_input.get().strip()
            sig_path = file_path + ".sig"
            if not os.path.exists(sig_path):
                raise Exception("Signature not found (.sig)")
            signature_bytes = Load_signature(sig_path)
            if signature_bytes is None:
                raise Exception("Failed to load signature")
            file_hash = HashGeneration(file_path)
            if not file_hash:
                raise Exception("Failed to compute hash")
            public_key = Load_PublicKey(PUBLIC_KEY_PATH)
            if not public_key:
                raise Exception("Failed to load public key")
            is_valid = Verify_Signature(signature_bytes, public_key, file_hash)
            self.root.after(0, lambda: self.update_progress(1.0))
            self.root.after(0, lambda: self.status_label.config(
                text="✅ VALID — File intact & authentic" if is_valid
                else "❌ INVALID — File modified or forged",
                fg="#00FFCC" if is_valid else "#FF5555"
            ))
        except Exception as e:
            self.root.after(0, lambda e=e: self.status_label.config(
                text=f"❌ {str(e)}",
                fg="#FF5555"
            ))

    def _on_back(self):
        # clear current interface widgets
        for w in self.root.winfo_children():
            w.destroy()
        # call provided callback to rebuild main menu
        if callable(self.on_back):
            self.on_back()
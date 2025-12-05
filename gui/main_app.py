import tkinter as tk
from ecdsa_signature_gui import IntegrityApp

if __name__ == "__main__":
    root = tk.Tk()
    app = IntegrityApp(root)
    root.mainloop()
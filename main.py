import tkinter as tk
from ui import FinanceApp

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_app)
    root.mainloop()
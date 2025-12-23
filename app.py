import tkinter as tk
from tkinter import filedialog, ttk
from multiprocessing import Pool, cpu_count
import threading

from worker import process_file, build_jobs

def run():
    jobs = build_jobs(src.get(), dst.get(), fmt.get(), quality.get())
    total.set(len(jobs))

    with Pool(cpu_count() - 1) as pool:
        for i, _ in enumerate(pool.imap_unordered(process_file, jobs), 1):
            done.set(i)

def start():
    threading.Thread(target=run, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("HEIC Converter (Fast)")

    src = tk.StringVar()
    dst = tk.StringVar()
    fmt = tk.StringVar(value="jpeg")
    quality = tk.IntVar(value=90)
    done = tk.IntVar()
    total = tk.IntVar()

    tk.Button(root, text="Source Folder",
              command=lambda: src.set(filedialog.askdirectory())).pack()
    tk.Button(root, text="Output Folder",
              command=lambda: dst.set(filedialog.askdirectory())).pack()

    ttk.Progressbar(root, maximum=1, variable=done).pack(fill="x", padx=10)

    tk.Button(root, text="Start", command=start).pack()

    root.mainloop()

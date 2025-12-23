import os
import time
import threading
from multiprocessing import Pool, cpu_count

import tkinter as tk
from tkinter import ttk, filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD

from worker import process_file, build_jobs, count_images

# ------------------- Conversion Logic -------------------

def run_conversion():
    jobs = build_jobs(src_dir.get(), dst_dir.get(), fmt.get(), quality.get())
    total_files.set(len(jobs))
    progress.set(0)

    start_time = time.time()

    with Pool(cpu_count() - 1) as pool:
        for i, _ in enumerate(pool.imap_unordered(process_file, jobs), 1):
            progress.set(i)

            # Geschwindigkeit & ETA
            elapsed = time.time() - start_time
            speed = i / elapsed if elapsed > 0 else 0
            eta = (len(jobs) - i) / speed if speed > 0 else 0

            speed_var.set(f"{speed:.1f} img/s")
            eta_var.set(f"{int(eta // 60)}m {int(eta % 60)}s")


def start_conversion():
    threading.Thread(target=run_conversion, daemon=True).start()


# ------------------- UI Helpers -------------------

def select_source():
    path = filedialog.askdirectory()
    if path:
        set_source(path)


def set_source(path):
    src_dir.set(path)
    dst_dir.set(path + "_converted")
    update_stats()


def drop_event(event):
    path = event.data.strip("{}")
    if os.path.isdir(path):
        set_source(path)


def estimate_size_per_image(quality, width=4000, height=3000):
    # grobe HEIC/JPEG-Schätzung in MB
    base = width * height * 3 / (1024**2)  # unkomprimiert MB
    factor = 0.05 + (quality - 70) / 25 * 0.15  # Qualitätsabhängig
    return round(base * factor, 2)


def estimate_total_size(num_images, quality):
    size_per_image = estimate_size_per_image(quality)
    return round(size_per_image * num_images, 2)


def update_stats(*args):
    try:
        n = count_images(src_dir.get())
        image_count_var.set(f"{n} Bilder")
        per_mb = estimate_size_per_image(quality.get())
        total_mb = estimate_total_size(n, quality.get())
        size_est_var.set(f"Pro Bild: {per_mb} MB | Gesamt: {total_mb} MB")
    except:
        image_count_var.set("0 Bilder")
        size_est_var.set("Pro Bild: -- MB | Gesamt: -- MB")


# ------------------- UI -------------------

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    root.title("HEIC Converter")
    root.geometry("800x480")
    root.resizable(False, False)

    # Variablen
    src_dir = tk.StringVar()
    dst_dir = tk.StringVar()
    fmt = tk.StringVar(value="jpeg")
    quality = tk.IntVar(value=90)

    progress = tk.IntVar()
    total_files = tk.IntVar(value=1)

    image_count_var = tk.StringVar(value="0 Bilder")
    speed_var = tk.StringVar(value="0 img/s")
    eta_var = tk.StringVar(value="--")
    size_est_var = tk.StringVar(value="Pro Bild: -- MB | Gesamt: -- MB")

    # Frames
    main = ttk.Frame(root, padding=20)
    main.pack(fill="both", expand=True)

    # Source
    ttk.Label(main, text="Quellordner").pack(anchor="w")
    src_entry = ttk.Entry(main, textvariable=src_dir, width=100)
    src_entry.pack(fill="x", pady=4)
    src_entry.drop_target_register(DND_FILES)
    src_entry.dnd_bind("<<Drop>>", drop_event)
    ttk.Button(main, text="Durchsuchen…", command=select_source).pack(anchor="e", pady=2)

    # Destination
    ttk.Label(main, text="Zielordner").pack(anchor="w", pady=(10, 0))
    ttk.Entry(main, textvariable=dst_dir, width=100).pack(fill="x", pady=4)

    # Optionen
    options = ttk.Frame(main)
    options.pack(fill="x", pady=10)

    ttk.Label(options, text="Format").grid(row=0, column=0, padx=5)
    ttk.Combobox(options, textvariable=fmt, values=["jpeg", "png"], width=8).grid(row=0, column=1)

    # Slider mit Beschriftung links/rechts
    slider_frame = ttk.Frame(options)
    slider_frame.grid(row=0, column=2, columnspan=2, padx=10)

    ttk.Label(slider_frame, text="niedrige Qualität").pack(side="left")
    scale = ttk.Scale(slider_frame, from_=70, to=95, variable=quality, orient="horizontal", length=180)
    scale.pack(side="left", padx=5)
    ttk.Label(slider_frame, text="hohe Qualität").pack(side="left")


    # Stats
    stats = ttk.Frame(main)
    stats.pack(fill="x", pady=10)

    ttk.Label(stats, text="Bilder:").grid(row=0, column=0, sticky="w")
    ttk.Label(stats, textvariable=image_count_var).grid(row=0, column=1, sticky="w", padx=5)

    ttk.Label(stats, text="Geschätzte Größe:").grid(row=1, column=0, sticky="w")
    ttk.Label(stats, textvariable=size_est_var).grid(row=1, column=1, sticky="w", padx=5)

    ttk.Label(stats, text="Geschwindigkeit:").grid(row=2, column=0, sticky="w")
    ttk.Label(stats, textvariable=speed_var).grid(row=2, column=1, sticky="w", padx=5)

    ttk.Label(stats, text="Geschätzte Dauer:").grid(row=3, column=0, sticky="w")
    ttk.Label(stats, textvariable=eta_var).grid(row=3, column=1, sticky="w", padx=5)

    # Progress bar
    ttk.Progressbar(
        main,
        maximum=1,
        variable=progress,
        length=700
    ).pack(fill="x", pady=10)

    # Start
    ttk.Button(main, text="Conversion starten", command=start_conversion).pack(pady=10)

    # Trace Updates
    quality.trace_add("write", update_stats)
    src_dir.trace_add("write", update_stats)

    root.mainloop()

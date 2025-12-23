import os
import shutil
from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener()


def build_jobs(src_root, dst_root, fmt, quality):
    """
    Walks the source directory and builds a list of conversion jobs.
    Preserves folder structure.
    """
    jobs = []

    for root, _, files in os.walk(src_root):
        rel = os.path.relpath(root, src_root)

        for file in files:
            src = os.path.join(root, file)
            dst = os.path.join(dst_root, rel, file)

            jobs.append((src, dst, fmt, quality))

    return jobs


def process_file(args):
    """
    Converts a single file or copies it if conversion is not needed.
    """
    src, dst, fmt, quality = args
    os.makedirs(os.path.dirname(dst), exist_ok=True)

    ext = os.path.splitext(src)[1].lower()

    if ext == ".heic":
        img = Image.open(src)
        out = os.path.splitext(dst)[0] + "." + fmt

        if fmt == "jpeg":
            img.save(out, "JPEG", quality=quality, subsampling=0)
        else:
            img.save(out, "PNG")
    else:
        if not os.path.exists(dst):
            shutil.copy2(src, dst)

def count_images(path):
    count = 0
    for root, _, files in os.walk(path):
        for f in files:
            if f.lower().endswith((".heic", ".jpg", ".jpeg", ".png")):
                count += 1
    return count

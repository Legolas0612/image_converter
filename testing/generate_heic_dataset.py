import os
import random
from PIL import Image
import pillow_heif
from tqdm import tqdm

pillow_heif.register_heif_opener()

# ---------------- CONFIG ----------------
OUTPUT_DIR = "heic_test_data"
TARGET_SIZE_GB = 10
IMAGE_SIZE = (4000, 3000)   # 12 MP
QUALITY = 90
# ---------------------------------------

TARGET_BYTES = TARGET_SIZE_GB * 1024**3
os.makedirs(OUTPUT_DIR, exist_ok=True)


def random_image(size):
    """Generate noisy image (worst-case compression)."""
    w, h = size
    data = bytearray(random.getrandbits(8) for _ in range(w * h * 3))
    return Image.frombytes("RGB", size, bytes(data))


def folder_size(path):
    total = 0
    for root, _, files in os.walk(path):
        for f in files:
            total += os.path.getsize(os.path.join(root, f))
    return total


current_size = folder_size(OUTPUT_DIR)
index = 0

print(f"Target size: {TARGET_SIZE_GB} GB")
print(f"Starting at: {current_size / 1024**3:.2f} GB")

with tqdm(unit="img") as bar:
    while current_size < TARGET_BYTES:
        img = random_image(IMAGE_SIZE)

        filename = f"img_{index:06d}.heic"
        path = os.path.join(OUTPUT_DIR, filename)

        heif_img = pillow_heif.from_pillow(img)
        heif_img.save(path, quality=QUALITY)

        index += 1
        current_size = folder_size(OUTPUT_DIR)

        bar.update(1)
        bar.set_postfix(size=f"{current_size / 1024**3:.2f} GB")

print("Done.")
print(f"Final size: {current_size / 1024**3:.2f} GB")
print(f"Images generated: {index}")

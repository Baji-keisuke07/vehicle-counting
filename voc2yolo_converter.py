
import os
import shutil
from tqdm import tqdm
from pathlib import Path

def fix_filename(filename, image_dir):
    """Fix path by adding .jpg and handling _r suffix if needed."""
    if not filename.endswith(".jpg"):
        filename += ".jpg"
    full_path = os.path.join(image_dir, filename)
    if not os.path.exists(full_path) and "_r" in filename:
        filename = filename.replace("_r", "")
        full_path = os.path.join(image_dir, filename)
    if os.path.exists(full_path):
        return filename
    return None

def process_split(split_file, image_dir, label_dir, out_img_dir, out_lbl_dir):
    with open(split_file, "r") as f:
        lines = [line.strip() for line in f.readlines()]
    for line in tqdm(lines, desc=f"Processing {split_file.split('.')[0]}"):
        fixed_filename = fix_filename(line, image_dir)
        if not fixed_filename:
            print(f"⚠️  Skipping missing file: {line}")
            continue

        # Copy image
        src_img = os.path.join(image_dir, fixed_filename)
        dst_img = os.path.join(out_img_dir, fixed_filename)
        os.makedirs(os.path.dirname(dst_img), exist_ok=True)
        shutil.copy2(src_img, dst_img)

        # Copy label
        label_file = os.path.splitext(fixed_filename)[0] + ".txt"
        src_lbl = os.path.join(label_dir, label_file)
        dst_lbl = os.path.join(out_lbl_dir, label_file)
        if os.path.exists(src_lbl):
            os.makedirs(os.path.dirname(dst_lbl), exist_ok=True)
            shutil.copy2(src_lbl, dst_lbl)

def make_yolo_dataset(base_dir):
    out_base = os.path.join(base_dir, "YOLOv8_dataset")
    os.makedirs(out_base, exist_ok=True)

    sets = ["train", "val", "test"]
    for split in sets:
        os.makedirs(os.path.join(out_base, "images", split), exist_ok=True)
        os.makedirs(os.path.join(out_base, "labels", split), exist_ok=True)

    for split in sets:
        process_split(
            split_file=os.path.join(base_dir, f"{split}.txt"),
            image_dir=os.path.join(base_dir, "JPEGImages"),
            label_dir=os.path.join(base_dir, "YOLOLabels"),
            out_img_dir=os.path.join(out_base, "images", split),
            out_lbl_dir=os.path.join(out_base, "labels", split),
        )

    # Create data.yaml
    yaml_path = os.path.join(out_base, "data.yaml")
    with open(yaml_path, "w") as f:
        f.write(f"path: {out_base}\n")
        f.write("train: images/train\n")
        f.write("val: images/val\n")
        f.write("test: images/test\n")
        f.write("nc: 1\n")
        f.write("names: ['object']\n")

    print("\n✅ Conversion complete. YOLOv8 dataset ready!")

if __name__ == "__main__":
    base_directory = os.getcwd()
    make_yolo_dataset(base_directory)


#!/usr/bin/env python3
"""
prep_photo.py
Preprocesses the input portrait for ASCII art generation:
1. Trims letterbox black margins.
2. Removes background using rembg (u2netp model).
3. Crops gracefully to focus on upper torso / head / gesture.
4. Composites onto pure white background.
5. Boosts local facial and clothing contrast with OpenCV CLAHE.
6. Saves grayscale source-prepped.png.
"""

import sys
import os
import cv2
import numpy as np
from PIL import Image

try:
    from rembg import remove, new_session
except ImportError:
    remove = None


def prep_photo(input_path: str, output_path: str):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input image not found: {input_path}")
        
    print(f"Loading {input_path}...")
    img = Image.open(input_path)
    
    # 1. Trim black letterbox bars if present
    arr = np.array(img.convert("RGB"))
    row_means = np.mean(arr, axis=(1, 2))
    col_means = np.mean(arr, axis=(0, 2))
    valid_rows = np.where(row_means > 10)[0]
    valid_cols = np.where(col_means > 10)[0]
    
    if len(valid_rows) > 0 and len(valid_cols) > 0:
        arr = arr[valid_rows[0]:valid_rows[-1]+1, valid_cols[0]:valid_cols[-1]+1]
        img = Image.fromarray(arr)
        print(f"Trimmed letterbox to: {img.size}")
        
    # Resize down if very high resolution for fast & memory-efficient background removal
    max_dim = 640
    if max(img.size) > max_dim:
        img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
        print(f"Resized for segmentation: {img.size}")
        
    # 2. Remove background
    print("Extracting subject...")
    if remove is not None:
        try:
            session = new_session("u2netp")
            no_bg = remove(img, session=session)
        except Exception as e:
            print(f"u2netp session failed ({e}), trying default remove...")
            no_bg = remove(img)
    else:
        print("Warning: rembg not found, using raw image with alpha mask.")
        no_bg = img.convert("RGBA")
        
    # 3. Crop upper torso focusing on face, shoulders, and gesture
    alpha = np.array(no_bg.split()[-1])
    coords = np.argwhere(alpha > 40)
    if len(coords) > 0:
        y0, x0 = coords.min(axis=0)
        y1, x1 = coords.max(axis=0)
        
        # Crop from top of head to just below watch / waist
        target_h = int((y1 - y0) * 0.82)
        crop_y1 = min(y0 + target_h, no_bg.size[1])
        crop_x0 = max(0, x0 - 4)
        crop_x1 = min(no_bg.size[0], x1 + 4)
        
        cropped = no_bg.crop((crop_x0, y0, crop_x1, crop_y1))
    else:
        cropped = no_bg
        
    # 4. Composite onto pure white
    white_bg = Image.new("RGB", cropped.size, (255, 255, 255))
    mask = cropped.split()[-1]
    white_bg.paste(cropped, mask=mask)
    
    # 5. Contrast-limited adaptive histogram equalization (CLAHE)
    gray = cv2.cvtColor(np.array(white_bg), cv2.COLOR_RGB2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.4, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    # Ensure pure white background remains 255
    alpha_arr = np.array(mask)
    enhanced[alpha_arr < 120] = 255
    
    cv2.imwrite(output_path, enhanced)
    print(f"Saved prepped image to {output_path} (size: {enhanced.shape[1]}x{enhanced.shape[0]})!")


def main():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    input_file = os.path.join(base_dir, "source-photo.jpg")
    output_file = os.path.join(base_dir, "source-prepped.png")
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
        
    prep_photo(input_file, output_file)


if __name__ == "__main__":
    main()

import os
import numpy as np
from lib.raw_processing import read_image, simple_raw_process_pipeline
from lib.pipeline import salc_wb_pipeline
from lib.angular_error import compute_image_illuminant, angular_error, compute_color_checker_illuminant

INPUT_PATH = "Sony_IMX135/field_3_cameras/"
INPUT_FILE  = "S_IMX135_field3cam_067.plain16"

WIDTH  = 3264
HEIGHT = 2448

BLACK_LEVEL = 64
WHITE_LEVEL = 1023

files = [f for f in os.listdir(INPUT_PATH) if f.endswith(".plain16")]
files.sort()

angular_errors_arr = []

for file in files:
    print(f"Processing {file}...")
    raw_img = read_image(INPUT_PATH, file, WIDTH, HEIGHT)
    raw16 = simple_raw_process_pipeline(raw_img, BLACK_LEVEL, WHITE_LEVEL)
    balanced, gr_s, gg_s, gb_s = salc_wb_pipeline(raw16, debug=False)

    # Error Estimation
    e_pred = compute_image_illuminant(gr_s, gg_s, gb_s)
    e_gt, patch_rgb = compute_color_checker_illuminant(raw16, visualize=False)
    error_deg = angular_error(e_pred, e_gt)
    angular_errors_arr.append(error_deg)

angular_errors = np.array(angular_errors_arr)

print("Angular error statistics:")
print(f"Mean: {angular_errors.mean():.3f}°")
print(f"Std:  {angular_errors.std():.3f}°")
print(f"Min:  {angular_errors.min():.3f}°")
print(f"Max:  {angular_errors.max():.3f}°")

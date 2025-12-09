import numpy as np
import matplotlib.pyplot as plt

from lib.pipeline import salc_wb_pipeline
from lib.raw_processing import read_image, simple_raw_process_pipeline

INPUT_PATH = "Sony_IMX135/field_3_cameras/"
INPUT_FILE  = "S_IMX135_field3cam_067.plain16"

WIDTH  = 3264
HEIGHT = 2448

BLACK_LEVEL = 64
WHITE_LEVEL = 1023

# Raw Image Processing
raw_img = read_image(INPUT_PATH, INPUT_FILE, WIDTH, HEIGHT)
raw16 = simple_raw_process_pipeline(raw_img, BLACK_LEVEL, WHITE_LEVEL)

# White-Balance Algorithm
balanced, gr, gg, gb = salc_wb_pipeline(raw16, debug=True)

# Display Formatting
raw16 = np.flipud(raw16)
raw16 = np.fliplr(raw16)
balanced = np.flipud(balanced)
balanced = np.fliplr(balanced)

# Output Display
fig, axes = plt.subplots(1, 3, figsize=(18,6))
axes[0].imshow(raw_img)
axes[0].set_title("RAW Image (input)")
axes[1].imshow(raw16)
axes[1].set_title("Transformed RAW Image")
axes[2].imshow(balanced)
axes[2].set_title("Blockified WB result")

for ax in axes:
    ax.axis('off')
plt.show()
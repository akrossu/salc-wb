import numpy as np
import cv2

def read_image(INPUT_PATH, INPUT_FILE, WIDTH, HEIGHT):
    raw = np.fromfile(INPUT_PATH + INPUT_FILE, dtype=np.uint16)

    if raw.size != WIDTH * HEIGHT:
        raise ValueError(f"Raw size mismatch! Expected {WIDTH*HEIGHT}, got {raw.size}")

    return raw.reshape((HEIGHT, WIDTH))

def black_level(img, BLACK_LEVEL=64, WHITE_LEVEL=1023):
    img = img.astype(np.float32)
    img = np.clip(img - BLACK_LEVEL, 0, None)
    img /= (WHITE_LEVEL - BLACK_LEVEL)
    return np.clip(img, 0, 1)

def demosaic(img):
    img = (img * 65535).astype(np.uint16)

    img = cv2.cvtColor(img, cv2.COLOR_BayerGB2RGB)
    return img.astype(np.float32) / 65535.0


def simple_raw_process_pipeline(raw, BLACK_LEVEL, WHITE_LEVEL):
    raw = black_level(raw, BLACK_LEVEL, WHITE_LEVEL)
    return demosaic(raw)
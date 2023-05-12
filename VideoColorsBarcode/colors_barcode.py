# -*- coding: utf-8 -*-
import io

import numpy as np
import pandas as pd
import cv2
from colorthief import ColorThief
from tqdm import tqdm
from PIL import Image, ImageDraw


def __opencv_to_pil(image: np.ndarray) -> Image:
    img = np.copy(image)

    # Notice the COLOR_BGR2RGB which means that the color is
    # converted from BGR to RGB
    color_coverted = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return Image.fromarray(color_coverted)


def __process_frame(pil_image: Image) -> tuple[np.ndarray, list[tuple[int, int, int]]]:
    byte_io = io.BytesIO()
    pil_image.save(byte_io, "png")
    byte_io.seek(0)

    # Get dominant color
    ct = ColorThief(byte_io)
    palette = ct.get_palette(color_count=5, quality=10)

    # Draw rectangle for each color
    # for i, color in enumerate(palette):
    #     cv2.rectangle(frame, (i * 100, 0), ((i + 1) * 100, 100), color, -1)

    return pil_image, palette


def create_palette_from_df(df_palette: pd.DataFrame, color_size: int = 10):
    # For each column in the dataframe
    for col in df_palette.columns:
        # Get the color palette
        palette = df_palette[col].to_list()

        # Create a new empty image with the size of the palette using pillow
        palette_image = Image.new("RGB", (len(palette) * color_size, 100))

        # Draw a rectangle for each color using pillow
        for i, color in enumerate(palette):
            draw = ImageDraw.Draw(palette_image)
            draw.rectangle([i * color_size, 0, (i + 1) * color_size, 100], fill=color)

        # Save the image
        palette_image.save(f"palette_{col}.png")
        yield palette_image

    return


def sample_dominant_colors(video):
    # Read mp4 file
    cap = cv2.VideoCapture(video)

    # Check if camera opened successfully
    if not cap.isOpened():
        print("Unable to read video feed")

    # Get information about the video
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(round(cap.get(cv2.CAP_PROP_FPS), 0))
    duration = frame_count / fps
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    df_palette = pd.DataFrame(columns=[f"color_{i}" for i in range(5)])

    # Read every frame and save it
    for i in tqdm(range(frame_count)):
    # for i in tqdm(range(500)):
        ret, cv2_frame = cap.read()

        if not ret:
            break

        # Process frame every 1 second
        if i % fps == 0:
            pil_frame = __opencv_to_pil(cv2_frame)

            progress = i / frame_count

            pil_out_frame, colors_palette = __process_frame(pil_frame)

            # Create a dataframe with one row and len(colors_palette) columns
            df = pd.DataFrame([colors_palette], columns=[f"color_{i}" for i in range(len(colors_palette))])

            # concat the new row to the dataframe
            df_palette = pd.concat([df_palette, df], ignore_index=True)

            yield progress, pil_out_frame, df_palette

    cap.release()

    yield 100, None, df_palette

    return

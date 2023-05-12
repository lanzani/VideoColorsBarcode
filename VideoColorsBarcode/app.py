# -*- coding: utf-8 -*-
import streamlit as st
import utils
import tempfile
import cv2
from PIL import Image

import colors_barcode as colbar


def print_output_colors(container, colors):
    cols = container.columns(len(colors))

    for col, color in zip(cols, colors):
        c = Image.new(mode="RGB", size=(160, 120), color=color)
        col.image(c)


def app():
    uploaded_video = st.file_uploader("Upload file", type=["mp4", "avi", "mov"])

    if uploaded_video is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_video.read())

        st.video(tfile.name)

        progress_bar = st.progress(0, text="Operation in progress. Please wait.")

        df_palette = None

        image_placeholder = st.empty()
        colors_placeholder = st.empty()
        for progress, image, partial_palette in colbar.sample_dominant_colors(tfile.name):
            progress_bar.progress(progress)
            df_palette = partial_palette

            if image is not None:
                # convert image from bgr to rgb
                image_placeholder.image(image)

            print_output_colors(colors_placeholder, df_palette.tail(1).values.flatten().tolist())

        progress_bar.progress(100, text="Operation completed.")

        st.dataframe(df_palette)

        for palette_image in colbar.create_palette_from_df(df_palette):
            st.image(palette_image)


def main():
    # load_css("/.css")

    app()


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-


def save_video_to_disk(bytes_data):

    with open("video.mp4", "wb") as f:
        f.write(bytes_data)

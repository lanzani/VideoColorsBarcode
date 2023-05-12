![Logo](docs/imgs/logo_small.png)

# Video Colors Barcode

![Image](docs/imgs/cover.png)

## Description
This is a simple python script that generates a barcode from a video file. The barcode is created by extracting the
average color of each frame in the video and plotting it on a canvas. This visual representation of the video
provides a unique way to visualize its color distribution over time.

## Installation
Download or clone the repository.
```bash
git clone https://github.com/lanzani/VideoColorsBarcode
```

Install the dependencies with poetry.
```bash
poetry install
```

Or use pip.
```bash
pip install -r requirements.txt
```


## Streamlit UI

To run the streamlit UI, run the following command.
```bash
streamlit run VideoColorsBarcode/app.py
```


![Image](docs/imgs/ui1.png)

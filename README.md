# 🚗 OpenCV Parking Lot Detection

This project demonstrates the use of **OpenCV** to detect occupied and unoccupied parking spaces in a parking lot using image processing techniques.

## 📌 Purpose

The goal of this project is to build a computer vision system that:
- Automatically detects free and occupied parking spaces in real-time or from video/images.
- Uses traditional image processing techniques (e.g., grayscale, thresholding, contour detection).
- Can be deployed on edge devices or integrated with parking management systems.

## 📁 Dataset

The dataset used in this project is publicly available on Google Drive:

📎 [Parking Lot Dataset](https://drive.google.com/drive/folders/1jovc7oBMFV1DutrijBFDbEMIO7fWwh5o)

It contains:
- Video footage of a parking lot (`carPark.mp4`)
- A serialized file with parking spot positions (`CarParkPos`)

## 🛠 Technologies Used

- Python
- OpenCV
- Numpy

## 🧠 Key Features

- Detects parking space status frame-by-frame
- Configurable detection thresholds and parking slot definitions
- Overlay visualization of detection results

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/opencv-parking-lot-detection.git
   cd opencv-parking-lot-detection
   ```

2. Download the dataset from the [link above](https://drive.google.com/drive/folders/1jovc7oBMFV1DutrijBFDbEMIO7fWwh5o) and place the files in your working directory.

3. Install dependencies:
   ```bash
   pip install opencv-python numpy
   ```

4. Run the main script:
   ```bash
   python main.py
   ```

## 📷 Output Example

- Green boxes for empty spots
- Red boxes for occupied spots
- Optional counter of available spots

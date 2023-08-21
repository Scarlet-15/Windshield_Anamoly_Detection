import streamlit as st
import pandas as pd
import numpy as np
from ultralytics import YOLO
import cv2

st.title('Car windshild defect detection')
uploaded_file = st.file_uploader("Choose a image file", type=["jpg","jpeg"])
from PIL import Image
model1 = YOLO(r"best.pt")

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)
    res = model1(opencv_image)  # results list
    for r in res:
        im_array = r.plot()  # plot a BGR numpy array of predictions
        im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image

        st.image(im, channels="BGR")
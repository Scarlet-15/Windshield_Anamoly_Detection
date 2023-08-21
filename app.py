import streamlit as st
import pandas as pd
import numpy as np


st.title('Car windshild defect detection')
uploaded_file = st.file_uploader("Choose a image file", type=["jpg","jpeg"])

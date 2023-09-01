import streamlit as st
import pandas as pd
import numpy as np
import datetime
from ultralytics import YOLO
from PIL import Image
import cv2
import time
import hydralit_components as hc
from io import BytesIO


#Defining state variables
if 'n_defective' not in st.session_state:
    st.session_state.n_defective = 0

if 'non_defective' not in st.session_state:
    st.session_state.non_defective = 0

if 'flag' not in st.session_state:
    st.session_state.flag = False

st.set_page_config( page_title="Car windshield defect detector",initial_sidebar_state="expanded")
#To hide the made with streamlit and default streamlit running symbol
hide_streamlit_style = """
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
#Invoking load symbol
with hc.HyLoader('',hc.Loaders.standard_loaders,index=2):
    time.sleep(5)
st.write("## Car windshield defect detector using AI/ML")
st.write(
    "Upload the image of your car windshield to check if it has any defects in it or not. :car:"
)

#Defining the theme of hydraulit info card
theme_bad = {'bgcolor': '#FFF0F0','title_color': 'red','content_color': 'red','icon_color': 'red', 'icon': 'fa fa-times-circle'}
theme_neutral = {'bgcolor': '#f9f9f9','title_color': 'orange','content_color': 'orange','icon_color': 'orange', 'icon': 'fa fa-question-circle'}
theme_good = {'bgcolor': '#EFF8F7','title_color': 'green','content_color': 'green','icon_color': 'green', 'icon': 'fa fa-check-circle'}
col1,col2,col3 = st.columns(3)

model1 = YOLO(r"best.pt")
img=[]                #Image with bounding boxes
init_img=[]           #Initial Images
names=[]              #List with file names
caption=[]            #Caption below image
cap=[]                #Formatted name+status
df_lst=[]             #List to make report
defective_lst=[]      #Defective part images
non_defective_lst=[]  #Non defective part images
defective_names=[]    #Defective part names
non_defective_names=[]#Non-Defective part names
uploaded_files = st.file_uploader("Choose a image file", type=["jpg","jpeg","png"],accept_multiple_files=True,label_visibility="hidden")
n=len(uploaded_files)
if(n==0):
    click=st.button("## Check",use_container_width=True,disabled=True)  #Disable button when no data is uploaded
else:
    click=st.button("## Check",use_container_width=True,disabled=False)
defect=0 #Keep track of number of defective item
for uploaded_file in uploaded_files:
    st.session_state.flag=False
    if uploaded_file is not None:
        names.append(uploaded_file.name)  
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        opencv_image = cv2.imdecode(file_bytes, 1)
        res = model1(opencv_image,stream=True)  # Prediction results list
        init_img.append(opencv_image)
        for r in res:
            n_pred=len(r.boxes)
            im_array = r.plot()  # plot a BGR numpy array of predictions
            im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
            img.append(im)
        if(n_pred!=0):
            defect+=1
            caption.append("Defective")
            cap.append("Defective")
            defective_lst.append(im)
        else:
            caption.append("Non-Defective")
            cap.append("Non-Defective")
            non_defective_lst.append(im)

if(st.session_state.flag):
    click=True
if(click):
    st.write(
    "### Scroll down to view results :arrow_double_down:"
    )
    
    st.session_state.n_defective=defect
    st.session_state.non_defective=n-st.session_state.n_defective
    for i in range(len(names)):
        df_lst.append([names[i],caption[i]])
        if(caption[i]=="Defective"):
            defective_names.append(names[i])
            cap[i]=names[i]+'    '+cap[i]
            names[i]="- " +':red['+names[i]+'    '+caption[i]+']'
            
        else:
            non_defective_names.append(names[i])
            cap[i]=names[i]+'    '+cap[i]
            names[i]="- " +':green['+names[i]+'    '+caption[i]+']'
       
    option = st.selectbox('## View', ('All', 'Defective', 'Non-Defective'))
    if(option=='All'):
        st.image(img, channels="BGR",clamp=True,caption=cap,use_column_width=True)
    elif(option=='Defective'):
        st.image(defective_lst, channels="BGR",clamp=True,caption=defective_names,use_column_width=True)
    elif(option=='Non-Defective'):
        st.image(non_defective_lst, channels="BGR",clamp=True,caption=non_defective_names,use_column_width=True)

    
        

with st.sidebar:
        
        st.title("Dashboard")
        for i in range(len(names)):
            with st.expander(names[i]):
                st.image(init_img[i],use_column_width=True,channels='BGR',clamp=True)
        if(names==[]):
            st.write("No data yet")
        if(df_lst==[]):
            disable=True
        else:
            disable=False
        df=pd.DataFrame(df_lst,columns=["Product Name","Status"])
        def to_excel(df):                                                                     #Funtion to write in excel
            output = BytesIO()
            current_time = datetime.datetime.now()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer, index=True, sheet_name='Sheet1',index_label='SNo.',startrow=3)
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']
            cell_format = workbook.add_format({'bold': True})
            cell_format.set_align('center')
            cell_format.set_align('vcenter')
            worksheet.write('B1', 'CAR WINDSHILD DEFECT DETECTOR REPORT',cell_format)

            format2 = workbook.add_format({'num_format': 'hh:mm AM/PM'})
            current_date=current_time.strftime("%#d %B, %Y")
            format2.set_align('center')
            format2.set_align('vcenter')
            worksheet.write('B2','Run Time: '+current_date)
            worksheet.write('B3',current_time,format2)

            format3=workbook.add_format()
            format3.set_align('center')
            format3.set_align('vcenter')
            worksheet.set_column('B:B', 50,format3)  

            sum_row=n+6
            format4 = workbook.add_format({'bold': True})
            worksheet.merge_range('A'+str(n+5)+':C'+str(sum_row), 'SUMMARY', cell_format)
            worksheet.write('B'+str(sum_row+1),'Total pieces ',format4)
            worksheet.write('B'+str(sum_row+2),'Number of defective pieces ',format4)
            worksheet.write('B'+str(sum_row+3),'Number of non-defective pieces ',format4)
            
            worksheet.write('C'+str(sum_row+1),n,format3)
            worksheet.write('C'+str(sum_row+2),st.session_state.n_defective,format3)
            worksheet.write('C'+str(sum_row+3),st.session_state.non_defective,format3)
            writer.save()

            processed_data = output.getvalue()
            return processed_data
        df_xlsx = to_excel(df)
        
        st.download_button(label="## Generate Report :page_facing_up:",
                           data=df_xlsx,
                           use_container_width =True,
                           file_name='Report.xlsx',
                           disabled =disable)
        
        if(disable == False):
            st.session_state.flag=True
        
        with st.expander("## About this app "):
            st.write("- This software was created to inspect newly manufactured windshields for cracks by using a video stream of the constructed windshield.")
            st.write("- This model, trained with the Python framework YOLOv8, finds and highlights fractures in windshields using bounding boxes.")
            st.write("- It also creates an Excel (.xlsx) file with the contents of the user's current working session.")
with col1:
    hc.info_card(title=str(n), content='Number of images uploaded',theme_override=theme_neutral,sentiment='neutral')

with col2:
    hc.info_card(title=str(st.session_state.n_defective), content='Number of defective piece',theme_override=theme_bad,sentiment='bad')

with col3:
    hc.info_card(title=str(st.session_state.non_defective), content='Number of non-defective piece',theme_override=theme_good,sentiment='good')
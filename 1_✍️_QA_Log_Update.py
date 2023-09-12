

from operator import index
from os import write
import stat
from tracemalloc import start
import streamlit as st
import pandas as pd
import numpy as np
import gspread
from google.oauth2.service_account import Credentials
import json
from gspread_dataframe import get_as_dataframe, set_with_dataframe
import base64
from io import BytesIO
import xlsxwriter
import openpyxl

st.subheader('QA_LOg Sheet Update', divider='rainbow')

# Global variables
Tool_1 = None
Tool_4 = None
Tool_6 = None

def process_datasets(files):
    global Tool_1, Tool_4, Tool_6

    for file in files:
        file_name = file.name
        dataset_name = file_name.split('.')[0]

        if dataset_name == 'Tool1-3 Phase 2 CBE CLASSROOM Observastion':
            Tool_1 = pd.read_excel(file)
        elif dataset_name == 'Tool 4 Phase 2 Shura Member Checklist':
            Tool_4 = pd.read_excel(file)
        elif dataset_name == 'Tool 6 Phase 2 School Community ParticipationRole':
            Tool_6 = pd.read_excel(file)
            
        else:
            st.warning(f"Dataset '{dataset_name}' does not match the expected datasets. Please Upload the correct dataset",icon="⚠️")


# Main Streamlit app
def main():
    st.title('Datasets')


    # File uploader
    files = st.file_uploader('Please upload the datasets related to the project', type=['xlsx', 'xls'], accept_multiple_files=True)

    # Process uploaded files
    process_datasets(files)

    # Example usage of the datasets
    if Tool_1 is not None:
        st.subheader('Tool 1 Dataset')
        st.write(Tool_1)

    if Tool_4 is not None:
        st.subheader('Tool 4 Dataset')
        st.write(Tool_1)

    if Tool_6 is not None:
        st.subheader('Tool 6 Dataset')
        st.write(Tool_1)

if __name__ == '__main__':
    main()




Tool_1['Tool_Name'] = "Tool 1"
Tool_1 = Tool_1[['KEY','Tool_Name','Province','District','Village','CBE_Name','CBE_Key','Surveyor_Name','Surveyor_Id']]

Tool_4['Tool_Name'] = "Tool 4"
Tool_4 = Tool_4[['KEY','Tool_Name','Province','District','Village','CBE_Name','CBE_Key','Surveyor_Name','Surveyor_Id']]

Tool_6['Tool_Name'] = "Tool 1"
Tool_6 = Tool_6[['KEY','Tool_Name','Province','District','Village','CBE_Name','CBE_Key','Surveyor_Name','Surveyor_Id']]


Merge_datasets = pd.concat([Tool_1,Tool_4,Tool_6])
st.subheader('Merge All datasets')
st.write(Merge_datasets)

# Load data from Google sheet
sheet_id = "1UeqKgO4T3Gy9MqfB8qHfDFAHVoX7XD9cz82UP5CIjBg"
sheet_name = "QA_Log"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"


QA_log = pd.read_csv(url)
df_id = QA_log['KEY']


Merge_datasets = Merge_datasets[~Merge_datasets.KEY.isin(df_id)]
st.subheader('Removing Duplicate KEY from the dataset')
st.write(Merge_datasets)



gc = gspread.service_account(filename='waris.json')
tab_name = 'QA_Log'
sheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1UeqKgO4T3Gy9MqfB8qHfDFAHVoX7XD9cz82UP5CIjBg/edit#gid=1946290')

if st.button('Update QA_Log'):
 sheet.values_append(tab_name, {'valueInputOption': 'USER_ENTERED'},{'values': Merge_datasets.astype(str).values.tolist()})

 st.markdown(
    """
    <style>
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }

    @keyframes blink-caret {
        from, to { border-color: transparent }
        50% { border-color: #0099D8; }
    }

    .typewriter-text {
        overflow: hidden;
        border-right: .15em solid #0099D8;
        white-space: nowrap;
        margin: 0 auto;
        letter-spacing: .15em;
        color: #0099D8;
        animation: typing 3.5s steps(40, end), blink-caret .75s step-end infinite;
        font-size: 17px; /* Adjust the font size as desired */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <h1 class="typewriter-text">Once you finish the update, Please take a look at the QA Log.</h1>
    """,
    unsafe_allow_html=True
)

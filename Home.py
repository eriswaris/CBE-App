from heapq import merge
from msilib.schema import Icon
from operator import index
from os import write
from re import T 
import stat
from tracemalloc import start
from turtle import color
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

st.set_page_config(
    page_title="Multipage APP",
    page_icon=("Boom")
)
st.subheader('UNICEF CBE Project - ACT & PPC', divider='rainbow')

#text writer an
st.markdown('<h1 class="animate__animated animate__fadeInDown">Hello!</h1>', unsafe_allow_html=True)




st.markdown(
    """
    <style>
    .unicef-text {
        color: #0099D8;
    }
    </style>
    """,
    unsafe_allow_html=True
)




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
        font-size: 19px; /* Adjust the font size as desired */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <h1 class="typewriter-text">The purpose of this webApp is to maintain high-quality data.</h1>
    """,
    unsafe_allow_html=True
)


multi = '''
 If you run into any technical problems or difficulties, feel free to contact Abdul Waris Amini, the Senior Data Officer at Premium Performance Consulting.
'''
st.markdown(multi)




import streamlit as st
import pandas as pd
import gspread

def update_qa_log():
    st.subheader('QA_Log Sheet Update', divider='rainbow')

    # Global variables
    Tool_1 = None
    Tool_4 = None
    Tool_6 = None

    def process_datasets(files):
        nonlocal Tool_1, Tool_4, Tool_6

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
                st.warning(f"Dataset '{dataset_name}' does not match the expected datasets. Please upload the correct dataset", icon="⚠️")

    def page1():
        st.title('Page 1')

        # File uploader
        files = st.file_uploader('Please upload the datasets related to the project', type=['xlsx', 'xls'], accept_multiple_files=True)

        if files:
            # Process uploaded files
            process_datasets(files)

            # Example usage of the datasets
            if Tool_1 is not None:
                st.subheader('Tool 1 Dataset')
                st.write(Tool_1)

            if Tool_4 is not None:
                st.subheader('Tool 4 Dataset')
                st.write(Tool_4)

            if Tool_6 is not None:
                st.subheader('Tool 6 Dataset')
                st.write(Tool_6)
        else:
            st.info('Please upload the datasets before proceeding.')

    def page2():
        st.title('Page 2')

        st.subheader('Merge All datasets')
        st.write(Merge_datasets)

        st.subheader('Removing Duplicate KEY from the dataset')
        st.write(Merge_datasets)

        gc = gspread.service_account(filename='PATH_TO_SERVICE_ACCOUNT_JSON_FILE')
        tab_name = 'QA_Log'
        sheet = gc.open_by_key(sheet_id).worksheet(sheet_name)

        if st.button('Update QA_Log'):
            sheet.insert_rows(Merge_datasets.values.tolist(), 2)

    def main():
        st.sidebar.title('Menu')
        page = st.sidebar.selectbox('Select Page', ('', 'Page 1', 'Page 2'))

        if page == 'Page 1':
            page1()
        elif page == 'Page 2':
            page2()
        elif page == '':
            st.warning('Please select a page from the sidebar menu.')

    main()

    Tool_1['Tool_Name'] = "Tool 1"
    Tool_1 = Tool_1[['KEY', 'Tool_Name', 'Province', 'District', 'Village', 'CBE_Name', 'CBE_Key', 'Surveyor_Name', 'Surveyor_Id']]

    Tool_4['Tool_Name'] = "Tool 4"
    Tool_4 = Tool_4[['KEY', 'Tool_Name', 'Province', 'District', 'Village', 'CBE_Name', 'CBE_Key', 'Surveyor_Name', 'Surveyor_Id']]

    Tool_6['Tool_Name'] = "Tool 1"
    Tool_6 = Tool_6[['KEY', 'Tool_Name', 'Province', 'District', 'Village', 'CBE_Name', 'CBE_Key', 'Surveyor_Name', 'Surveyor_Id']]

    Merge_datasets = pd.concat([Tool_1, Tool_4, Tool_6])

    # Load data from Google Sheets
    sheet_id = "YOUR_SHEET_ID"
    sheet_name = "QA_Log"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

    QA_log = pd.read_csv(url)
    df_id = QA_log['KEY']

    Merge_datasets = Merge_datasets[~Merge_datasets.KEY.isin(df_id)]

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
            letter-spacing:```python
import streamlit as st
import pandas as pd
import gspread

def update_qa_log():
    st.subheader('QA_Log Sheet Update', divider='rainbow')

    # Global variables
    Tool_1 = None
    Tool_4 = None
    Tool_6 = None

    def process_datasets(files):
        nonlocal Tool_1, Tool_4, Tool_6

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
                st.warning(f"Dataset '{dataset_name}' does not match the expected datasets. Please upload the correct dataset", icon="⚠️")

    def page1():
        st.title('Page 1')

        # File uploader
        files = st.file_uploader('Please upload the datasets related to the project', type=['xlsx', 'xls'], accept_multiple_files=True)

        if files:
            # Process uploaded files
            process_datasets(files)

            # Example usage of the datasets
            if Tool_1 is not None:
                st.subheader('Tool 1 Dataset')
                st.write(Tool_1)

            if Tool_4 is not None:
                st.subheader('Tool 4 Dataset')
                st.write(Tool_4)

            if Tool_6 is not None:
                st.subheader('Tool 6 Dataset')
                st.write(Tool_6)
        else:
            st.info('Please upload the datasets before proceeding.')

    def page2():
        st.title('Page 2')

        st.subheader('Merge All datasets')
        st.write(Merge_datasets)

        st.subheader('Removing Duplicate KEY from the dataset')
        st.write(Merge_datasets)

        gc = gspread.service_account(filename='PATH_TO_SERVICE_ACCOUNT_JSON_FILE')
        tab_name = 'QA_Log'
        sheet = gc.open_by_key(sheet_id).worksheet(sheet_name)

        if st.button('Update QA_Log'):
            sheet.insert_rows(Merge_datasets.values.tolist(), 2)

    def main():
        st.sidebar.title('Menu')
        page = st.sidebar.selectbox('Select Page', ('', 'Page 1', 'Page 2'))

        if page == 'Page 1':
            page1()
        elif page == 'Page 2':
            page2()
        elif page == '':
            st.warning('Please select a page from the sidebar menu.')

    main()

    Tool_1['Tool_Name'] = "Tool 1"
    Tool_1 = Tool_1[['KEY', 'Tool_Name', 'Province', 'District', 'Village', 'CBE_Name', 'CBE_Key', 'Surveyor_Name', 'Surveyor_Id']]

    Tool_4['Tool_Name'] = "Tool 4"
    Tool_4 = Tool_4[['KEY', 'Tool_Name', 'Province', 'District', 'Village', 'CBE_Name', 'CBE_Key', 'Surveyor_Name', 'Surveyor_Id']]

    Tool_6['Tool_Name'] = "Tool 1"
    Tool_6 = Tool_6[['KEY', 'Tool_Name', 'Province', 'District', 'Village', 'CBE_Name', 'CBE_Key', 'Surveyor_Name', 'Surveyor_Id']]

    Merge_datasets = pd.concat([Tool_1, Tool_4, Tool_6])

    # Load data from Google Sheets
    sheet_id = "YOUR_SHEET_ID"
    sheet_name = "QA_Log"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

    QA_log = pd.read_csv(url)
    df_id = QA_log['KEY']

    Merge_datasets = Merge_datasets[~Merge_datasets.KEY.isin(df_id)]

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
            animation: 
                typing 3.5s steps(30, end),
                blink-caret .75s step-endinfinite





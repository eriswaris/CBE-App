from importlib.metadata import files
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
import base64
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import Workbook
import io
import datetime
import re


st.subheader('Please Upload the datasets to find the errors', divider='rainbow')
st.subheader('Select the dataset')



# Global variables
Tool_1 = None
Tool_4 = None
Tool_6 = None
Tool_9 = None
Tool_8 = None

def process_datasets(files):
    global Tool_1, Tool_4, Tool_6, Tool_9, Tool_8

    for file in files:
        file_name = file.name
        dataset_name = file_name.split('.')[0]

        if dataset_name == 'Tool1-3 Phase 2 CBE CLASSROOM Observastion':
            Tool_1 = pd.read_excel(file)
        elif dataset_name == 'Tool 4 Phase 2 Shura Member Checklist':
            Tool_4 = pd.read_excel(file)
        elif dataset_name == 'Tool 6 Phase 2 School Community ParticipationRole':
            Tool_6 = pd.read_excel(file)
        elif dataset_name == 'Tool 8 HUB School Teacher KII':
            Tool_8 = pd.read_excel(file)    
        
        elif dataset_name == 'Tool 9 Fomal School Checklist':
            Tool_9 = pd.read_excel(file)    
        else:
            st.warning(f"Dataset '{dataset_name}' does not match the expected datasets. Please Upload the correct dataset",icon="⚠️")


# Main Streamlit app
def main():

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
        st.write(Tool_4)

    if Tool_6 is not None:
        st.subheader('Tool 6 Dataset')
        st.write(Tool_6)

    if Tool_8 is not None:
        st.subheader('Tool 8 Dataset')
        st.write(Tool_8)
        
    if Tool_9 is not None:
        st.subheader('Tool 9 Dataset')
        st.write(Tool_9)




def Tool_4_fun():
        global Tool_4
 
        error_keys = []
        error_questions = []
        error_messages = []
        error_qa_status = []
        error_qa_by = []
        
        df=Tool_4
        # Rule 1: No_Consent_Reason
        no_consent_reason_error = (
            (df['No_Consent_Reason'] == 8888) & 
            df['No_Consent_Reason_Other'].isnull()
        )
        if no_consent_reason_error.any():
            error_keys.extend(df.loc[no_consent_reason_error, 'KEY'])
            error_questions.extend(['No_Consent_Reason'] * no_consent_reason_error.sum())
            error_messages.extend(['If No_Consent_Reason = 8888, then No_Consent_Reason_Other should not be blank.'] * no_consent_reason_error.sum())
            error_qa_status.extend(df.loc[no_consent_reason_error,'QA_status'])
            error_qa_by.extend(df.loc[no_consent_reason_error,'QA_By'])



        #Rule 2 : No consent
        consent_informed_error = (
            (df['Consent_Informed'] == 0) & 
            (df['No_Consent_Reason'].isnull())


        )
        if consent_informed_error.any():
            error_keys.extend(df.loc[consent_informed_error, 'KEY'])
            error_questions.extend(['Consent_Informed'] * consent_informed_error.sum())
            error_messages.extend(['If Consent_Informed == 0, No_Consent_Reason should not be blank.'] * consent_informed_error.sum())
            error_qa_status.extend(df.loc[consent_informed_error, 'QA_status'])
            error_qa_by.extend(df.loc[consent_informed_error,'QA_By'])


        # Rule 2: Shura_Members_Meet_Regularly
        shura_members_meet_error = (
            (df['Shura_Members_Meet_Regularly'] == 1) & (df['How_Often'].isnull()) | (df['Shura_Members_Meet_Regularly'] == 0) & (df['How_Often'].notnull())
            
        )
        if shura_members_meet_error.any():
            error_keys.extend(df.loc[shura_members_meet_error, 'KEY'])
            error_questions.extend(['Shura_Members_Meet_Regularly'] * shura_members_meet_error.sum())
            error_messages.extend(['If Shura_Members_Meet_Regularly = 1, then How_Often should not be blank and if If Shura_Members_Meet_Regularly = 0 then How_Often should not be blank .'] * shura_members_meet_error.sum())
            error_qa_status.extend(df.loc[shura_members_meet_error,'QA_status'])
            error_qa_by.extend(df.loc[shura_members_meet_error,'QA_By'])



        # Rule 3: Do_Shura_Meet_Regulary
        do_shura_meet_error = (
            (df['Do_Shura_Meet_Regulary'] == 1) & (df['How_Often_Do_You_Meet'].isnull()) | (df['Do_Shura_Meet_Regulary'] == 0 ) & (df['How_Often_Do_You_Meet'].notnull())
            
        )
        if do_shura_meet_error.any():
            error_keys.extend(df.loc[do_shura_meet_error, 'KEY'])
            error_questions.extend(['Do_Shura_Meet_Regulary'] * do_shura_meet_error.sum())
            error_messages.extend(['If Do_Shura_Meet_Regulary = 1, then How_Often_Do_You_Meet should not be blank and if Do_Shura_Meet_Regulary=0 How_Often_Do_You_Meet should be blank.'] * do_shura_meet_error.sum())
            error_qa_status.extend(df.loc[do_shura_meet_error,'QA_status'])
            error_qa_by.extend(df.loc[do_shura_meet_error,'QA_By'])




        # Rule 4: Main_Discussion
        main_discussion_error = (
            (df['Main_Discussion'] == 8888) & 
            df['Main_Discussion_Other'].isnull()
        )
        if main_discussion_error.any():
            error_keys.extend(df.loc[main_discussion_error, 'KEY'])
            error_questions.extend(['Main_Discussion'] * main_discussion_error.sum())
            error_messages.extend(['If Main_Discussion = 8888, then Main_Discussion_Other should not be blank.'] * main_discussion_error.sum())
            error_qa_status.extend(df.loc[main_discussion_error,'QA_status'])
            error_qa_by.extend(df.loc[main_discussion_error,'QA_By'])


            
        ############Translatin check

        # Rule 1: Village_Town_Name
        village_town_error = df['Village_Town_Name'].astype(str).str.contains('[آ-ی]', regex=True, na=False)
        if village_town_error.any():
            error_keys.extend(df.loc[village_town_error, 'KEY'])
            error_questions.extend(['Village_Town_Name'] * village_town_error.sum())
            error_messages.extend(['Translation Missing'] * village_town_error.sum())
            error_qa_status.extend(df.loc[village_town_error,'QA_status'])
            error_qa_by.extend(df.loc[village_town_error,'QA_By'])





        # Rule 2: No_Consent_Reason_Other
        no_consent_reason_error = df['No_Consent_Reason_Other'].astype(str).str.contains('[آ-ی]', regex=True, na=False)
        if no_consent_reason_error.any():
            error_keys.extend(df.loc[no_consent_reason_error, 'KEY'])
            error_questions.extend(['No_Consent_Reason_Other'] * no_consent_reason_error.sum())
            error_messages.extend(['Translation Missing'] * no_consent_reason_error.sum())
            error_qa_status.extend(df.loc[no_consent_reason_error,'QA_status'])
            error_qa_by.extend(df.loc[no_consent_reason_error,'QA_By'])



        # Rule 3: Name_Resp
        name_resp_error = df['Name_Resp'].astype(str).str.contains('[آ-ی]', regex=True, na=False)
        if name_resp_error.any():
            error_keys.extend(df.loc[name_resp_error, 'KEY'])
            error_questions.extend(['Name_Resp'] * name_resp_error.sum())
            error_messages.extend(['Translation Missing'] * name_resp_error.sum())
            error_qa_status.extend(df.loc[name_resp_error,'QA_status'])
            error_qa_by.extend(df.loc[name_resp_error,'QA_By'])





        # Rule 4: Main_Discussion_Other
        main_discussion_error = df['Main_Discussion_Other'].astype(str).str.contains('[آ-ی]', regex=True, na=False)
        if main_discussion_error.any():
            error_keys.extend(df.loc[main_discussion_error, 'KEY'])
            error_questions.extend(['Main_Discussion_Other'] * main_discussion_error.sum())
            error_messages.extend(['Translation Missing'] * main_discussion_error.sum())
            error_qa_status.extend(df.loc[main_discussion_error,'QA_status'])
            error_qa_by.extend(df.loc[main_discussion_error,'QA_By'])




        # Rule 5: Final_comments and Final_comments_Translation
        final_comments_error = df['Final_comments'].notnull() & df['Final_comments_Translation'].isnull()
        if final_comments_error.any():
            error_keys.extend(df.loc[final_comments_error, 'KEY'])
            error_questions.extend(['Final_comments_Translation'] * final_comments_error.sum())
            error_messages.extend(['Translation Missing'] * final_comments_error.sum())
            error_qa_status.extend(df.loc[final_comments_error,'QA_status'])
            error_qa_by.extend(df.loc[final_comments_error,'QA_By'])


        #Rule 6: Duplicate shcool ID

        TPM_CBE_ID = df['TPM_CBE_ID'].duplicated()
        if TPM_CBE_ID.any():

            error_keys.extend(df.loc[TPM_CBE_ID, 'KEY'])
            error_questions.extend(['TPM_CBE_ID'] * TPM_CBE_ID.sum())
            error_messages.extend(['Duplicate CBE School'] * TPM_CBE_ID.sum())
            error_qa_status.extend(df.loc[TPM_CBE_ID,'QA_status'])
            error_qa_by.extend(df.loc[error_keys,'QA_By'])




        qa_status_spell = (
            ((df['QA_status'].notnull()) & (~df['QA_status'].isin(['APP', 'REJ', 'PEN'])))
        )
            
        
        if qa_status_spell.any():
            error_keys.extend(df.loc[qa_status_spell, 'KEY'])
            error_questions.extend(['QA_status'] * qa_status_spell.sum())
            error_messages.extend(['Incorrect spelling.'] * qa_status_spell.sum())
            error_qa_status.extend(df.loc[qa_status_spell,'QA_status'])
            error_qa_by.extend(df.loc[qa_status_spell,'QA_By'])
       





        # Create a DataFrame to store the error details
        Trans = pd.DataFrame({
            'KEY': error_keys,
            'Question': error_questions,
            'Error Message': error_messages,
            'QA Status': error_qa_status,
            'QA_By': error_qa_by
        })


        df = pd.DataFrame(Trans)

        
        # Example usage of the dataset
        if Trans is not None:
            st.subheader('Dataset Errors')
            st.write(df)

            buffer = io.BytesIO()

            Trans.to_excel(buffer, sheet_name='Errors', index=False, engine='openpyxl')

            buffer.seek(0)

            st.download_button(
                label="Download data as Excel",
                data=buffer,
                file_name='Tool_4_Errors.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            


def Tool_6_fun():
        global Tool_6

        error_keys = []
        error_questions = []
        error_messages = []
        error_qa_status = []
        error_qa_by = []

        df = Tool_6



        #Rule 1 : No consent Other
        no_consent_reason_error = (
            (df['No_Consent_Reason'] == 8888) & 
            df['No_Consent_Reason_Other'].isnull()
        )
        if no_consent_reason_error.any():
            error_keys.extend(df.loc[no_consent_reason_error, 'KEY'])
            error_questions.extend(['No_Consent_Reason'] * no_consent_reason_error.sum())
            error_messages.extend(['If No_Consent_Reason = 8888, than No_Consent_Reason_Other should not be blank.'] * no_consent_reason_error.sum())
            error_qa_status.extend(df.loc[no_consent_reason_error, 'QA_status'])
            error_qa_by.extend(df.loc[no_consent_reason_error,'QA_By'])
        #Rule 2 : No consent
        consent_informed_error = (
            (df['Consent_Informed'] == 0) & 
            (df['No_Consent_Reason'].isnull())


        )
        if consent_informed_error.any():
            error_keys.extend(df.loc[consent_informed_error, 'KEY'])
            error_questions.extend(['Consent_Informed'] * consent_informed_error.sum())
            error_messages.extend(['If Consent_Informed == 0, No_Consent_Reason should not be blank.'] * consent_informed_error.sum())
            error_qa_status.extend(df.loc[consent_informed_error, 'QA_status'])
            consent_informed_error.extend(df.loc[no_consent_reason_error,'QA_By'])
            error_qa_by.extend(df.loc[consent_informed_error,'QA_By'])



        #Rule 3 How many children

        How_Many_Children = (
            ((df['Do_You_Have_Child_Attending_CBE'] == 1) & (df['How_Many_Children'].isnull())) | ((df['Do_You_Have_Child_Attending_CBE'] == 0 ) & (df['How_Many_Children'].notnull()))
        )
        
        if How_Many_Children.any():
            error_keys.extend(df.loc[How_Many_Children, 'KEY'])
            error_questions.extend(['How_Many_Children'] * How_Many_Children.sum())
            error_messages.extend(['Logic error'] * How_Many_Children.sum())
            error_qa_status.extend(df.loc[How_Many_Children, 'QA_status'])
            error_qa_by.extend(df.loc[How_Many_Children,'QA_By'])



        #Rule 4  Suddestion for Impro
        Suggestions_For_Improvement = (

            ((df['Satisfied_Service_School_CBE__ALC_Offer'] == 1) & (df['Suggestions_For_Improvement'].notnull())) | ((df['Satisfied_Service_School_CBE__ALC_Offer'] == 0 ) & (df['Suggestions_For_Improvement'].isnull()))
        )

        if Suggestions_For_Improvement.any():
            error_keys.extend(df.loc[Suggestions_For_Improvement, 'KEY'])
            error_questions.extend(['Suggestions_For_Improvement'] * Suggestions_For_Improvement.sum())
            error_messages.extend(['Logic error'] * Suggestions_For_Improvement.sum())
            error_qa_status.extend(df.loc[Suggestions_For_Improvement, 'QA_status' ])
            error_qa_by.extend(df.loc[Suggestions_For_Improvement,'QA_By'])

        #missing Tranlation check

        village_town_error = df['Village_Town_Name'].astype(str).str.contains('[آ-ی]', regex=True, na=False)
        if village_town_error.any():
            error_keys.extend(df.loc[village_town_error, 'KEY'])
            error_questions.extend(['Village_Town_Name'] * village_town_error.sum())
            error_messages.extend(['Translation Missing'] * village_town_error.sum())
            error_qa_status.extend(df.loc[village_town_error, 'QA_status' ])
            error_qa_by.extend(df.loc[village_town_error,'QA_By'])


        # Rule 2: No_Consent_Reason_Other
        no_consent_reason_error = df['No_Consent_Reason_Other'].astype(str).str.contains('[آ-ی]', regex=True, na=False)
        if no_consent_reason_error.any():
            error_keys.extend(df.loc[no_consent_reason_error, 'KEY'])
            error_questions.extend(['No_Consent_Reason_Other'] * no_consent_reason_error.sum())
            error_messages.extend(['Translation Missing'] * no_consent_reason_error.sum())
            error_qa_status.extend(df.loc[no_consent_reason_error, 'QA_status' ])
            error_qa_by.extend(df.loc[no_consent_reason_error,'QA_By'])




        # Rule 3: Name_Resp
        name_resp_error = df['Name_Resp'].astype(str).str.contains('[آ-ی]', regex=True, na=False)
        if name_resp_error.any():
            error_keys.extend(df.loc[name_resp_error, 'KEY'])
            error_questions.extend(['Name_Resp'] * name_resp_error.sum())
            error_messages.extend(['Translation Missing'] * name_resp_error.sum())
            error_qa_status.extend(df.loc[name_resp_error, 'QA_status' ])
            error_qa_by.extend(df.loc[name_resp_error,'QA_By'])


        #Rule 4: final comment

        final_comments_error = df['Final_comments'].notnull() & df['Final_comments_Translation'].isnull()
        if final_comments_error.any():
            error_keys.extend(df.loc[final_comments_error, 'KEY'])
            error_questions.extend(['Final_comments_Translation'] * final_comments_error.sum())
            error_messages.extend(['Translation Missing'] * final_comments_error.sum())
            error_qa_status.extend(df.loc[final_comments_error, 'QA_status' ])
            error_qa_by.extend(df.loc[final_comments_error,'QA_By'])



        #Rule 5: final comment

        Suggestions_For_Improvement_error = df['Suggestions_For_Improvement'].notnull() & df['Suggestions_For_Improvement_Translation'].astype(str).str.contains('-', regex=True, na=False)
        if Suggestions_For_Improvement_error.any():
            error_keys.extend(df.loc[Suggestions_For_Improvement_error, 'KEY'])
            error_questions.extend(['Suggestions_For_Improvement_Translation'] * Suggestions_For_Improvement_error.sum())
            error_messages.extend(['Translation Missing'] * Suggestions_For_Improvement_error.sum())
            error_qa_by.extend(df.loc[Suggestions_For_Improvement_error, 'QA_status' ])




        TPM_CBE_ID = df['TPM_CBE_ID'].duplicated()
        if TPM_CBE_ID.any():

            error_keys.extend(df.loc[TPM_CBE_ID, 'KEY'])
            error_questions.extend(['TPM_CBE_ID'] * TPM_CBE_ID.sum())
            error_messages.extend(['Duplicate CBE School'] * TPM_CBE_ID.sum())
            error_qa_status.extend(df.loc[TPM_CBE_ID, 'QA_status'])
            error_qa_by.extend(df.loc[TPM_CBE_ID, 'QA_status' ])            

        



        qa_status_spell = (
            ((df['QA_status'].notnull()) & (~df['QA_status'].isin(['APP', 'REJ', 'PEN'])))
        )
            
        
        if qa_status_spell.any():
            error_keys.extend(df.loc[qa_status_spell, 'KEY'])
            error_questions.extend(['QA_status'] * qa_status_spell.sum())
            error_messages.extend(['Incorrect spelling.'] * qa_status_spell.sum())
            error_qa_status.extend(df.loc[qa_status_spell,'QA_status'])
            error_qa_by.extend(df.loc[qa_status_spell, 'QA_status' ])




        # Create a DataFrame to store the error details
        Trans = pd.DataFrame({
            'KEY': error_keys,
            'Question': error_questions,
            'Error Message': error_messages,
            'QA Status': error_qa_status,
            'QA By': error_qa_by
        })


        df = pd.DataFrame(Trans)

        
        # Example usage of the dataset
        if Trans is not None:
            st.subheader('Dataset Errors')
            st.write(df)

            buffer = io.BytesIO()

            Trans.to_excel(buffer, sheet_name='Errors', index=False, engine='openpyxl')

            buffer.seek(0)

            st.download_button(
                label="Download data as Excel",
                data=buffer,
                file_name='Tool_6_Errors.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )


def Tool_1_fun():

        global Tool_1

        error_keys = []
        error_questions = []
        error_messages = []
        error_qa_status = []
        error_qa_by = []

        df = Tool_1



        #Rule 1 : No consent Other
        no_consent_reason_error = (
            (df['No_Consent_Reason'] == 8888) & 
            df['No_Consent_Reason_Other'].isnull()
        )
        if no_consent_reason_error.any():
            error_keys.extend(df.loc[no_consent_reason_error, 'KEY'])
            error_questions.extend(['No_Consent_Reason'] * no_consent_reason_error.sum())
            error_messages.extend(['If No_Consent_Reason = 8888, than No_Consent_Reason_Other should not be blank.'] * no_consent_reason_error.sum())
            error_qa_status.extend(df.loc[no_consent_reason_error, 'QA_status'])
            error_qa_by.extend(df.loc[no_consent_reason_error,'QA_By'])





        #Rule 2 : No consent
        consent_informed_error = (
            (df['Consent_Informed'] == 0) & 
            (df['No_Consent_Reason'].isnull())


        )
        if consent_informed_error.any():
            error_keys.extend(df.loc[consent_informed_error, 'KEY'])
            error_questions.extend(['Consent_Informed'] * consent_informed_error.sum())
            error_messages.extend(['If Consent_Informed == 0, No_Consent_Reason should not be blank.'] * consent_informed_error.sum())
            error_qa_status.extend(df.loc[consent_informed_error, 'QA_status'])
            error_qa_by.extend(df.loc[consent_informed_error,'QA_By'])





        
        Classroom_Infrastructure_Pic_QA = (
             
            ((df['Classroom_Infrastructure_Pic'].notnull()) & (~df['Classroom_Infrastructure_Pic_QA'].isin(['Blur/Not Visible Photo', 'Relevant Photo', 'Irrelevant Photo'])))    
        

        )

        if Classroom_Infrastructure_Pic_QA.any():
            error_keys.extend(df.loc[Classroom_Infrastructure_Pic_QA, 'KEY'])
            error_questions.extend(['Classroom_Infrastructure_Pic_QA'] * Classroom_Infrastructure_Pic_QA.sum())
            error_messages.extend(['Incorrect spelling/Missing Status.'] * Classroom_Infrastructure_Pic_QA.sum())
            error_qa_status.extend(df.loc[Classroom_Infrastructure_Pic_QA, 'QA_status'])
            error_qa_by.extend(df.loc[Classroom_Infrastructure_Pic_QA,'QA_By'])




            Students_picture_QA = (
             
            ((df['Students_picture'].notnull()) & (~df['Students_picture_QA'].isin(['Blur/Not Visible Photo', 'Relevant Photo', 'Irrelevant Photo'])))    
        

        )

        if Students_picture_QA.any():
            error_keys.extend(df.loc[Students_picture_QA, 'KEY'])
            error_questions.extend(['Students_picture_QA'] * Students_picture_QA.sum())
            error_messages.extend(['Incorrect spelling/Missing Status.'] * Students_picture_QA.sum())
            error_qa_status.extend(df.loc[Students_picture_QA, 'QA_status'])
            error_qa_by.extend(df.loc[Students_picture_QA,'QA_By'])

             

        When_Learning_Space_Established_error = df['When_Learning_Space_Established'] > datetime.datetime(2023, 8, 3)

        if When_Learning_Space_Established_error.any():
            error_keys.extend(df.loc[When_Learning_Space_Established_error, 'KEY'])
            error_questions.extend(['When_Learning_Space_Established'] * When_Learning_Space_Established_error.sum())
            error_messages.extend(['Date is greater than 8/3/2023.'] * When_Learning_Space_Established_error.sum())
            error_qa_status.extend(df.loc[When_Learning_Space_Established_error, 'QA_status'])
            error_qa_by.extend(df.loc[When_Learning_Space_Established_error,'QA_By'])


        date_formate = "%Y-%m-%d %H-%M"
        df['Date_And_Time'] = pd.to_datetime(df['Date_And_Time'], format = date_formate)

        
        Last_Time_Attendance_Was_Recorded_error = (
            (df['Last_Time_Attendance_Was_Recorded'].dt.date == df['Date_And_Time'].dt.date) &
            (df['Attendance_Record'].notnull())
        )


        if Last_Time_Attendance_Was_Recorded_error.any():
            error_keys.extend(df.loc[Last_Time_Attendance_Was_Recorded_error, 'KEY'])
            error_questions.extend(['Attendance_Record'] * Last_Time_Attendance_Was_Recorded_error.sum())
            error_messages.extend(['If Last_Time_Attendance_Was_Recorded date matches Date_And_Time, Attendance_Record should be blank.'] * Last_Time_Attendance_Was_Recorded_error.sum())
            error_qa_status.extend(df.loc[Last_Time_Attendance_Was_Recorded_error, 'QA_status'])
            error_qa_by.extend(df.loc[Last_Time_Attendance_Was_Recorded_error,'QA_By'])




        filtered_df = df[df['Attendance_Record'].notnull()]
        date_difference = (filtered_df['Date_And_Time'] - filtered_df['Last_Time_Attendance_Was_Recorded']).dt.days

        attendance_match = (date_difference == filtered_df['Attendance_Record'])
        attendance_match_error = filtered_df[~attendance_match]

        if not attendance_match_error.empty:
            error_keys.extend(attendance_match_error['KEY'].tolist())
            error_questions.extend(['Attendance_Record'] * attendance_match_error.shape[0])
            error_messages.extend(['Attendance_Record Integer does not match with date and time'] * attendance_match_error.shape[0])
            error_qa_status.extend(attendance_match_error['QA_status'].tolist())
            error_qa_by.extend(df.loc[attendance_match_error,'QA_By'])




        Reason_Absenteeism = (

            ((df['Students_Absent_Last_Three_Days'] == 1) & (df['Reason_Absenteeism'].isnull())) | ((df['Students_Absent_Last_Three_Days'] == 0 ) & (df['Reason_Absenteeism'].notnull()))
        )

        if Reason_Absenteeism.any():
            error_keys.extend(df.loc[Reason_Absenteeism, 'KEY'])
            error_questions.extend(['Reason_Absenteeism'] * Reason_Absenteeism.sum())
            error_messages.extend(['Logic error'] * Reason_Absenteeism.sum())
            error_qa_status.extend(df.loc[Reason_Absenteeism, 'QA_status' ])
            error_qa_by.extend(df.loc[Reason_Absenteeism,'QA_By'])



        Reason_Absenteeism_Translation = df['Reason_Absenteeism'].notnull() & df['Reason_Absenteeism_Translation'].astype(str).str.contains('-', regex=True, na=False)
        if Reason_Absenteeism_Translation.any():
            error_keys.extend(df.loc[Reason_Absenteeism_Translation, 'KEY'])
            error_questions.extend(['Suggestions_For_Improvement_Translation'] * Reason_Absenteeism_Translation.sum())
            error_messages.extend(['Translation Missing'] * Reason_Absenteeism_Translation.sum())
            error_qa_status.extend(df.loc[Reason_Absenteeism_Translation, 'QA_status' ])
            error_qa_by.extend(df.loc[Reason_Absenteeism_Translation,'QA_By'])





        Picture1_QA = (
             
            ((df['Picture1'].notnull()) & (~df['Picture1_QA'].isin(['Blur/Not Visible Photo', 'Relevant Photo', 'Irrelevant Photo'])))    
        

        )

        if Picture1_QA.any():
            error_keys.extend(df.loc[Picture1_QA, 'KEY'])
            error_questions.extend(['Picture1_QA'] * Picture1_QA.sum())
            error_messages.extend(['Incorrect spelling/Missing Status.'] * Picture1_QA.sum())
            error_qa_status.extend(df.loc[Picture1_QA, 'QA_status'])
            error_qa_by.extend(df.loc[Picture1_QA,'QA_By'])




            Picture2_QA = (
             
            ((df['Picture2'].notnull()) & (~df['Picture2_QA'].isin(['Blur/Not Visible Photo', 'Relevant Photo', 'Irrelevant Photo'])))    
        

        )

        if Picture2_QA.any():
            error_keys.extend(df.loc[Picture2_QA, 'KEY'])
            error_questions.extend(['Picture2_QA'] * Picture2_QA.sum())
            error_messages.extend(['Incorrect spelling/Missing Status.'] * Picture2_QA.sum())
            error_qa_status.extend(df.loc[Picture2_QA, 'QA_status'])
            error_qa_by.extend(df.loc[Picture2_QA,'QA_By'])




        Picture3_QA = (
             
            ((df['Picture3'].notnull()) & (~df['Picture3_QA'].isin(['Blur/Not Visible Photo', 'Relevant Photo', 'Irrelevant Photo'])))    
        

        )

        if Picture3_QA.any():
            error_keys.extend(df.loc[Picture3_QA, 'KEY'])
            error_questions.extend(['Picture3_QA'] * Picture3_QA.sum())
            error_messages.extend(['Incorrect spelling/Missing Status.'] * Picture3_QA.sum())
            error_qa_status.extend(df.loc[Picture3_QA, 'QA_status'])
            error_qa_by.extend(df.loc[Picture3_QA,'QA_By'])


        

        
        condition = (
            ((df['Education_Level_Learning_Space'] == 2) & (df['Attendance_Book_Available'] == 1)) & ((df['Total_Absent_Academic_Year_More_10Days'].isnull()) | 
            (df['Total_Absent_Academic_Year_More_10Days_Boys'].isnull()) |
            (df['Total_Absent_Academic_Year_More_10Days_Girls'].isnull()))
            
        )



        if condition.any():
            error_keys.extend(df.loc[condition, 'KEY'])
            error_questions.extend(['Absent_Registered_Students_Academic_Year_More_10_Days_Group'] * condition.sum())
            error_messages.extend(['Logic error please check the code book.'] * condition.sum())
            error_qa_status.extend(df.loc[condition, 'QA_status'])
            error_qa_by.extend(df.loc[condition,'QA_By'])




        condition_2 = (
            ((df['Education_Level_Learning_Space'] != 2) & (df['Attendance_Book_Available'] == 0)) & ((df['Total_Absent_Academic_Year_More_10Days'].notnull()) | 
            (df['Total_Absent_Academic_Year_More_10Days_Boys'].notnull()) |
            (df['Total_Absent_Academic_Year_More_10Days_Girls'].notnull()))
            
        )



        if condition_2.any():
            error_keys.extend(df.loc[condition_2, 'KEY'])
            error_questions.extend(['Absent_Registered_Students_Academic_Year_More_10_Days_Group'] * condition_2.sum())
            error_messages.extend(['Logic error please check the code book.'] * condition_2.sum())
            error_qa_status.extend(df.loc[condition_2, 'QA_status'])
            error_qa_by.extend(df.loc[condition_2,'QA_By'])





        
        condition_3 = (
            ((df['Education_Level_Learning_Space'] != 2) & (df['Attendance_Book_Available'] == 1)) & ((df['Total_Absent_Academic_Year_More_10Days'].notnull()) | 
            (df['Total_Absent_Academic_Year_More_10Days_Boys'].notnull()) |
            (df['Total_Absent_Academic_Year_More_10Days_Girls'].notnull()))
            
        )



        if condition_3.any():
            error_keys.extend(df.loc[condition_3, 'KEY'])
            error_questions.extend(['Absent_Registered_Students_Academic_Year_More_10_Days_Group'] * condition_3.sum())
            error_messages.extend(['Logic error please check the code book.'] * condition_3.sum())
            error_qa_status.extend(df.loc[condition_3, 'QA_status'])
            error_qa_by.extend(df.loc[condition_3,'QA_By'])




        Dropdown = (
            ((df['Education_Level_Learning_Space'].isin([2, 1])) & 
            ((df['Total_Number_Students_Drouput'].isnull()) & 
            (df['Total_Number_Students_Drouput_Boys'].isnull()) &
            (df['Total_Number_Students_Drouput_Girls'].isnull())))
        )


        if Dropdown.any():
            error_keys.extend(df.loc[Dropdown, 'KEY'])
            error_questions.extend(['Registered_Droupout_Students_Academic_Year_Group'] * Dropdown.sum())
            error_messages.extend(['Logic error please check the code book.'] * Dropdown.sum())
            error_qa_status.extend(df.loc[Dropdown, 'QA_status'])
            error_qa_by.extend(df.loc[Dropdown,'QA_By'])



        Dropdown_2 = (
            ((df['Education_Level_Learning_Space'].isin([3, 4, 5, 6, 7, 8])) & 
            ((df['Total_Number_Students_Drouput'].notnull()) & 
            (df['Total_Number_Students_Drouput_Boys'].notnull()) &
            (df['Total_Number_Students_Drouput_Girls'].notnull())))
        )


        if Dropdown_2.any():
            error_keys.extend(df.loc[Dropdown_2, 'KEY'])
            error_questions.extend(['Registered_Droupout_Students_Academic_Year_Group'] * Dropdown_2.sum())
            error_messages.extend(['Logic error please check the code book.'] * Dropdown_2.sum())
            error_qa_status.extend(df.loc[Dropdown_2, 'QA_status'])
            error_qa_by.extend(df.loc[Dropdown_2,'QA_By'])




        IP_Name = IP_Name = (df['IP_Name'].isnull() | (df['IP_Name'] != df['IP_Name'].str.upper()))


        if IP_Name.any():
            error_keys.extend(df.loc[IP_Name, 'KEY'])
            error_questions.extend(['IP_Name'] * IP_Name.sum())
            error_messages.extend(['IP Name is blank/ Not upper case.'] * IP_Name.sum())
            error_qa_status.extend(df.loc[IP_Name, 'QA_status'])
            error_qa_by.extend(df.loc[IP_Name,'QA_By'])





        Asaas_Number_Group = (
            ((df['Attendance_Book_Available'] == 1)) & ((df['Asaas_Number_Total'].isnull()) |
            (df['Asaas_Number_Boys'].isnull()) |
            (df['Asaas_Number_Girls'].isnull()))
    )



        if Asaas_Number_Group.any():
            error_keys.extend(df.loc[Asaas_Number_Group, 'KEY'])
            error_questions.extend(['Asaas_Number_Group'] * Asaas_Number_Group.sum())
            error_messages.extend(['Logic error please check the code book.'] * Asaas_Number_Group.sum())
            error_qa_status.extend(df.loc[Asaas_Number_Group, 'QA_status'])
            error_qa_by.extend(df.loc[Asaas_Number_Group,'QA_By'])





        Asaas_Number_Group_2 = (
            ((df['Attendance_Book_Available'] == 0)) & ((df['Asaas_Number_Total'].notnull()) |
            (df['Asaas_Number_Boys'].notnull()) |
            (df['Asaas_Number_Girls'].notnull()))
    )



        if Asaas_Number_Group_2.any():
            error_keys.extend(df.loc[Asaas_Number_Group_2, 'KEY'])
            error_questions.extend(['Asaas_Number_Group'] * Asaas_Number_Group_2.sum())
            error_messages.extend(['Logic error please check the code book.'] * Asaas_Number_Group_2.sum())
            error_qa_status.extend(df.loc[Asaas_Number_Group_2, 'QA_status'])
            error_qa_by.extend(df.loc[Asaas_Number_Group_2,'QA_By'])
        



        Dropouts_Reason = (
             ((df['Total_Number_Students_Drouput'] > 0) & (df['Dropouts_Reason'].isnull()))
    )



        if Dropouts_Reason.any():
            error_keys.extend(df.loc[Dropouts_Reason, 'KEY'])
            error_questions.extend(['Dropouts_Reason'] * Dropouts_Reason.sum())
            error_messages.extend(['Logic error please check the code book.'] * Dropouts_Reason.sum())
            error_qa_status.extend(df.loc[Dropouts_Reason, 'QA_status'])
            error_qa_by.extend(df.loc[Dropouts_Reason,'QA_By'])






        Dropouts_Reason_2 = (
             ((df['Total_Number_Students_Drouput'] == 0) & (df['Dropouts_Reason'].notnull()))
    )



        if Dropouts_Reason_2.any():
            error_keys.extend(df.loc[Dropouts_Reason_2, 'KEY'])
            error_questions.extend(['Dropouts_Reason'] * Dropouts_Reason_2.sum())
            error_messages.extend(['Logic error please check the code book.'] * Dropouts_Reason_2.sum())
            error_qa_status.extend(df.loc[Dropouts_Reason_2, 'QA_status'])
            error_qa_by.extend(df.loc[Dropouts_Reason_2,'QA_By'])




        

        Dropouts_Reason_Other = (
            (df['Dropouts_Reason'] == 8888) & 
            df['Dropouts_Reason_Other'].isnull()
        )
        if Dropouts_Reason_Other.any():
            error_keys.extend(df.loc[Dropouts_Reason_Other, 'KEY'])
            error_questions.extend(['Dropouts_Reason_Other'] * Dropouts_Reason_Other.sum())
            error_messages.extend(['Dropouts_Reason_Other is blank'] * Dropouts_Reason_Other.sum())
            error_qa_status.extend(df.loc[Dropouts_Reason_Other,'QA_status'])
            error_qa_by.extend(df.loc[Dropouts_Reason_Other,'QA_By'])






        Dropouts_Reason_Other_2 = (
            (df['Dropouts_Reason'] != 8888) & 
            df['Dropouts_Reason_Other'].notnull()
        )
        if Dropouts_Reason_Other_2.any():
            error_keys.extend(df.loc[Dropouts_Reason_Other_2, 'KEY'])
            error_questions.extend(['Dropouts_Reason_Other'] * Dropouts_Reason_Other_2.sum())
            error_messages.extend(['Dropouts_Reason_Other is not blank'] * Dropouts_Reason_Other_2.sum())
            error_qa_status.extend(df.loc[Dropouts_Reason_Other_2,'QA_status'])
            error_qa_by.extend(df.loc[Dropouts_Reason_Other_2,'QA_By'])







        Which_School_Obtained_Asaas_Number = (
            (df['Asaas_Number_Total'] > 0) & (df['Which_School_Obtained_Asaas_Number'].isnull() | (df['Which_School_Obtained_Asaas_Number'] == '-'))            
        )
    
        if Which_School_Obtained_Asaas_Number.any():
            error_keys.extend(df.loc[Which_School_Obtained_Asaas_Number, 'KEY'])
            error_questions.extend(['Which_School_Obtained_Asaas_Number'] * Which_School_Obtained_Asaas_Number.sum())
            error_messages.extend(['Which_School_Obtained_Asaas_Number is blank.'] * Which_School_Obtained_Asaas_Number.sum())
            error_qa_status.extend(df.loc[Which_School_Obtained_Asaas_Number, 'QA_status'])
            error_qa_by.extend(df.loc[Which_School_Obtained_Asaas_Number,'QA_By'])




        
        Which_School_Obtained_Asaas_Number_1 = (
            (df['Asaas_Number_Total'] == 0) & ~(df['Which_School_Obtained_Asaas_Number'].isnull() | (df['Which_School_Obtained_Asaas_Number'] == '-'))
        )
          
     
        
    
        if Which_School_Obtained_Asaas_Number_1.any():
            error_keys.extend(df.loc[Which_School_Obtained_Asaas_Number_1, 'KEY'])
            error_questions.extend(['Which_School_Obtained_Asaas_Number'] * Which_School_Obtained_Asaas_Number_1.sum())
            error_messages.extend(['Which_School_Obtained_Asaas_Number should be blank.'] * Which_School_Obtained_Asaas_Number_1.sum())
            error_qa_status.extend(df.loc[Which_School_Obtained_Asaas_Number_1, 'QA_status'])
            error_qa_by.extend(df.loc[Which_School_Obtained_Asaas_Number_1,'QA_By'])




        TPM_School_ID = (
            (df['Asaas_Number_Total'] > 0) & (df['TPM_School_ID'].isnull() | (df['TPM_School_ID'] == '-'))            
        )
    
        if TPM_School_ID.any():
            error_keys.extend(df.loc[TPM_School_ID, 'KEY'])
            error_questions.extend(['TPM_School_ID'] * TPM_School_ID.sum())
            error_messages.extend(['TPM_School_ID is blank.'] * TPM_School_ID.sum())
            error_qa_status.extend(df.loc[TPM_School_ID, 'QA_status'])
            error_qa_by.extend(df.loc[TPM_School_ID,'QA_By'])

        




        TPM_School_ID_1 = (
            (df['Asaas_Number_Total'] == 0) & ~(df['TPM_School_ID'].isnull() | (df['TPM_School_ID'] == '-'))            
        )
    
        if TPM_School_ID_1.any():
            error_keys.extend(df.loc[TPM_School_ID_1, 'KEY'])
            error_questions.extend(['TPM_School_ID_1'] * TPM_School_ID_1.sum())
            error_messages.extend(['TPM_School_ID is blank.'] * TPM_School_ID_1.sum())
            error_qa_status.extend(df.loc[TPM_School_ID_1, 'QA_status'])
            error_qa_by.extend(df.loc[TPM_School_ID_1,'QA_By'])
    



        



        EMIS_School_ID = (
            (df['Asaas_Number_Total'] > 0) & (df['EMIS_School_ID'].isnull() | (df['EMIS_School_ID'] == '-'))            
        )
    
        if EMIS_School_ID.any():
            error_keys.extend(df.loc[EMIS_School_ID, 'KEY'])
            error_questions.extend(['EMIS_School_ID'] * EMIS_School_ID.sum())
            error_messages.extend(['TPM_School_ID is blank.'] * EMIS_School_ID.sum())
            error_qa_status.extend(df.loc[EMIS_School_ID, 'QA_status'])
            error_qa_by.extend(df.loc[EMIS_School_ID,'QA_By'])

        




        EMIS_School_ID_1 = (
            (df['Asaas_Number_Total'] == 0) & ~(df['EMIS_School_ID'].isnull() | (df['EMIS_School_ID'] == '-'))            
        )
    
        if EMIS_School_ID_1.any():
            error_keys.extend(df.loc[EMIS_School_ID_1, 'KEY'])
            error_questions.extend(['EMIS_School_ID_1'] * EMIS_School_ID_1.sum())
            error_messages.extend(['TPM_School_ID is blank.'] * EMIS_School_ID_1.sum())
            error_qa_status.extend(df.loc[EMIS_School_ID_1, 'QA_status'])
            error_qa_by.extend(df.loc[EMIS_School_ID_1,'QA_By'])




        Board_In_Good_Condition_Or_need_Replaced = (
            ((df['School_Have_Board'] == 1) & (df['Board_In_Good_Condition_Or_need_Replaced'].isnull())) | ((df['School_Have_Board'] == 0 ) & (df['Board_In_Good_Condition_Or_need_Replaced'].notnull()))            
        )
    
        if Board_In_Good_Condition_Or_need_Replaced.any():
            error_keys.extend(df.loc[Board_In_Good_Condition_Or_need_Replaced, 'KEY'])
            error_questions.extend(['Board_In_Good_Condition_Or_need_Replaced'] * Board_In_Good_Condition_Or_need_Replaced.sum())
            error_messages.extend(['Logic error.'] * Board_In_Good_Condition_Or_need_Replaced.sum())
            error_qa_status.extend(df.loc[Board_In_Good_Condition_Or_need_Replaced, 'QA_status'])
            error_qa_by.extend(df.loc[Board_In_Good_Condition_Or_need_Replaced,'QA_By'])






        How_Frequently_Does_The_School_Gets_Replenishment_Of_Chalks_Markers = (
             ((df['Does_The_Class_Have_Sufficient_Chalk_Markers'] == 1) & (df['How_Frequently_Does_The_School_Gets_Replenishment_Of_Chalks_Markers'].isnull())) 
             | ((df['Does_The_Class_Have_Sufficient_Chalk_Markers'] == 0 ) & (df['How_Frequently_Does_The_School_Gets_Replenishment_Of_Chalks_Markers'].notnull()))


        )

        if How_Frequently_Does_The_School_Gets_Replenishment_Of_Chalks_Markers.any():
            error_keys.extend(df.loc[How_Frequently_Does_The_School_Gets_Replenishment_Of_Chalks_Markers, 'KEY'])
            error_questions.extend(['How_Frequently_Does_The_School_Gets_Replenishment_Of_Chalks_Markers'] * How_Frequently_Does_The_School_Gets_Replenishment_Of_Chalks_Markers.sum())
            error_messages.extend(['Logic error.'] * How_Frequently_Does_The_School_Gets_Replenishment_Of_Chalks_Markers.sum())
            error_qa_status.extend(df.loc[How_Frequently_Does_The_School_Gets_Replenishment_Of_Chalks_Markers, 'QA_status'])
            error_qa_by.extend(df.loc[How_Frequently_Does_The_School_Gets_Replenishment_Of_Chalks_Markers,'QA_By'])




        How_Frequently_Does_The_School_Gets_Replenishment_Of_Chalks_Markers_2 = (
             ((df['Does_The_Class_Have_Sufficient_Chalk_Markers'] == 2) & (df['How_Frequently_Does_The_School_Gets_Replenishment_Of_Chalks_Markers'].isnull()))


        )

        if How_Frequently_Does_The_School_Gets_Replenishment_Of_Chalks_Markers_2.any():
            error_keys.extend(df.loc[How_Frequently_Does_The_School_Gets_Replenishment_Of_Chalks_Markers_2, 'KEY'])
            error_questions.extend(['How_Frequently_Does_The_School_Gets_Replenishment_Of_Chalks_Markers_2'] * How_Frequently_Does_The_School_Gets_Replenishment_Of_Chalks_Markers_2.sum())
            error_messages.extend(['Logic error.'] * How_Frequently_Does_The_School_Gets_Replenishment_Of_Chalks_Markers_2.sum())
            error_qa_status.extend(df.loc[How_Frequently_Does_The_School_Gets_Replenishment_Of_Chalks_Markers_2, 'QA_status'])
            error_qa_by.extend(df.loc[How_Frequently_Does_The_School_Gets_Replenishment_Of_Chalks_Markers_2,'QA_By'])
        
        


        When_Was_The_Last_Time_The_School_Got_Chalks_Markers_Replenishment = (
             ((df['Does_The_Class_Have_Sufficient_Chalk_Markers'] == 1) & (df['When_Was_The_Last_Time_The_School_Got_Chalks_Markers_Replenishment'].isnull())) | ((df['Does_The_Class_Have_Sufficient_Chalk_Markers'] == 0 ) & (df['When_Was_The_Last_Time_The_School_Got_Chalks_Markers_Replenishment'].notnull()))


        )

        if When_Was_The_Last_Time_The_School_Got_Chalks_Markers_Replenishment.any():
            error_keys.extend(df.loc[When_Was_The_Last_Time_The_School_Got_Chalks_Markers_Replenishment, 'KEY'])
            error_questions.extend(['When_Was_The_Last_Time_The_School_Got_Chalks_Markers_Replenishment'] * When_Was_The_Last_Time_The_School_Got_Chalks_Markers_Replenishment.sum())
            error_messages.extend(['Logic error.'] * When_Was_The_Last_Time_The_School_Got_Chalks_Markers_Replenishment.sum())
            error_qa_status.extend(df.loc[When_Was_The_Last_Time_The_School_Got_Chalks_Markers_Replenishment, 'QA_status'])
            error_qa_by.extend(df.loc[When_Was_The_Last_Time_The_School_Got_Chalks_Markers_Replenishment,'QA_By'])







        When_Was_The_Last_Time_The_School_Got_Chalks_Markers_Replenishment_1 = (
             ((df['Does_The_Class_Have_Sufficient_Chalk_Markers'] == 2) & (df['When_Was_The_Last_Time_The_School_Got_Chalks_Markers_Replenishment'].isnull()))


        )

        if When_Was_The_Last_Time_The_School_Got_Chalks_Markers_Replenishment_1.any():
            error_keys.extend(df.loc[When_Was_The_Last_Time_The_School_Got_Chalks_Markers_Replenishment_1, 'KEY'])
            error_questions.extend(['When_Was_The_Last_Time_The_School_Got_Chalks_Markers_Replenishment_1'] * When_Was_The_Last_Time_The_School_Got_Chalks_Markers_Replenishment_1.sum())
            error_messages.extend(['Logic error.'] * When_Was_The_Last_Time_The_School_Got_Chalks_Markers_Replenishment_1.sum())
            error_qa_status.extend(df.loc[When_Was_The_Last_Time_The_School_Got_Chalks_Markers_Replenishment_1, 'QA_status'])
            error_qa_by.extend(df.loc[When_Was_The_Last_Time_The_School_Got_Chalks_Markers_Replenishment_1,'QA_By'])



    
        

        All_Children_Have_Notebooks_Pencils = (
            ((df['All_Children_Have_Notebooks_Pencils'] == 0) & (df['How_Many_Children_Lacking_Notebook_Pencil'].isnull())) | ((df['All_Children_Have_Notebooks_Pencils'] == 1 ) & (df['How_Many_Children_Lacking_Notebook_Pencil'].notnull()))            
        )
    
        if All_Children_Have_Notebooks_Pencils.any():
            error_keys.extend(df.loc[All_Children_Have_Notebooks_Pencils, 'KEY'])
            error_questions.extend(['All_Children_Have_Notebooks_Pencils'] * All_Children_Have_Notebooks_Pencils.sum())
            error_messages.extend(['Logic error.'] * All_Children_Have_Notebooks_Pencils.sum())
            error_qa_status.extend(df.loc[All_Children_Have_Notebooks_Pencils, 'QA_status'])
            error_qa_by.extend(df.loc[All_Children_Have_Notebooks_Pencils,'QA_By'])



        Reason_Some_Children_Missing_Notebook_Pencil = (
            ((df['All_Children_Have_Notebooks_Pencils'] == 0) & (df['Reason_Some_Children_Missing_Notebook_Pencil'].isnull())) | ((df['All_Children_Have_Notebooks_Pencils'] == 1 ) & (df['Reason_Some_Children_Missing_Notebook_Pencil'].notnull()))            
        )
    
        if Reason_Some_Children_Missing_Notebook_Pencil.any():
            error_keys.extend(df.loc[Reason_Some_Children_Missing_Notebook_Pencil, 'KEY'])
            error_questions.extend(['Reason_Some_Children_Missing_Notebook_Pencil'] * Reason_Some_Children_Missing_Notebook_Pencil.sum())
            error_messages.extend(['Logic error.'] * Reason_Some_Children_Missing_Notebook_Pencil.sum())
            error_qa_status.extend(df.loc[Reason_Some_Children_Missing_Notebook_Pencil, 'QA_status'])
            error_qa_by.extend(df.loc[Reason_Some_Children_Missing_Notebook_Pencil,'QA_By'])
    


        Reason_Some_Children_Missing_Notebook_Pencil_Tranlsation = df['Reason_Some_Children_Missing_Notebook_Pencil'].notnull() & (df['Reason_Some_Children_Missing_Notebook_Pencil_Tranlsation'].isnull() | 
         df['Reason_Some_Children_Missing_Notebook_Pencil_Tranlsation'].astype(str).str.contains('-', regex=True, na=False))
        


        if Reason_Some_Children_Missing_Notebook_Pencil_Tranlsation.any():
            error_keys.extend(df.loc[Reason_Some_Children_Missing_Notebook_Pencil_Tranlsation, 'KEY'])
            error_questions.extend(['Reason_Some_Children_Missing_Notebook_Pencil_Tranlsation'] * Reason_Some_Children_Missing_Notebook_Pencil_Tranlsation.sum())
            error_messages.extend(['Translation Missing'] * Reason_Some_Children_Missing_Notebook_Pencil_Tranlsation.sum())
            error_qa_status.extend(df.loc[Reason_Some_Children_Missing_Notebook_Pencil_Tranlsation,'QA_status'])
            error_qa_by.extend(df.loc[Reason_Some_Children_Missing_Notebook_Pencil_Tranlsation,'QA_By'])



        Teacher_Review_Homework_Put_Comments = (
            ((df['Children_Used_their_Notebook_Regular_Basis'] != 0) & (df['Teacher_Review_Homework_Put_Comments'].isnull()))
             | ((df['Children_Used_their_Notebook_Regular_Basis'] == 0) & (df['Teacher_Review_Homework_Put_Comments'].notnull()))
        )
    
        if Teacher_Review_Homework_Put_Comments.any():
            error_keys.extend(df.loc[Teacher_Review_Homework_Put_Comments, 'KEY'])
            error_questions.extend(['Teacher_Review_Homework_Put_Comments'] * Teacher_Review_Homework_Put_Comments.sum())
            error_messages.extend(['Logic error.'] * Teacher_Review_Homework_Put_Comments.sum())
            error_qa_status.extend(df.loc[Teacher_Review_Homework_Put_Comments, 'QA_status'])
            error_qa_by.extend(df.loc[Teacher_Review_Homework_Put_Comments,'QA_By'])







        Do_Children_Have_MOE_Appropriate_Textbook_Other = (
             ((df['Do_Children_Have_MOE_Appropriate_Textbook'] == 1) & (df['Do_Children_Have_MOE_Appropriate_Textbook_Other'].notnull())) 
             | ((df['Do_Children_Have_MOE_Appropriate_Textbook'] == 0 ) & (df['Do_Children_Have_MOE_Appropriate_Textbook_Other'].isnull()))


        )

        if Do_Children_Have_MOE_Appropriate_Textbook_Other.any():
            error_keys.extend(df.loc[Do_Children_Have_MOE_Appropriate_Textbook_Other, 'KEY'])
            error_questions.extend(['Do_Children_Have_MOE_Appropriate_Textbook_Other'] * Do_Children_Have_MOE_Appropriate_Textbook_Other.sum())
            error_messages.extend(['Logic error.'] * Do_Children_Have_MOE_Appropriate_Textbook_Other.sum())
            error_qa_status.extend(df.loc[Do_Children_Have_MOE_Appropriate_Textbook_Other, 'QA_status'])
            error_qa_by.extend(df.loc[Do_Children_Have_MOE_Appropriate_Textbook_Other,'QA_By'])





        Children_Have_Grade_Appropriate_Textbooks = (
             ((df['Do_Children_Have_MOE_Appropriate_Textbook'] == 1) & (df['Children_Have_Grade_Appropriate_Textbooks'].isnull())) 
             | ((df['Do_Children_Have_MOE_Appropriate_Textbook'] == 0 ) & (df['Children_Have_Grade_Appropriate_Textbooks'].notnull()))


        )

        if Children_Have_Grade_Appropriate_Textbooks.any():
            error_keys.extend(df.loc[Children_Have_Grade_Appropriate_Textbooks, 'KEY'])
            error_questions.extend(['Children_Have_Grade_Appropriate_Textbooks'] * Children_Have_Grade_Appropriate_Textbooks.sum())
            error_messages.extend(['Logic error.'] * Children_Have_Grade_Appropriate_Textbooks.sum())
            error_qa_status.extend(df.loc[Children_Have_Grade_Appropriate_Textbooks, 'QA_status'])
            error_qa_by.extend(df.loc[Children_Have_Grade_Appropriate_Textbooks,'QA_By'])





        
        Textbook_Appropriate_Language = (
             ((df['Children_Have_Grade_Appropriate_Textbooks'] == 1) & (df['Textbook_Appropriate_Language'].isnull())) | 
             ((df['Children_Have_Grade_Appropriate_Textbooks'] == 0 ) & (df['Textbook_Appropriate_Language'].notnull()))


        )

        if Textbook_Appropriate_Language.any():
            error_keys.extend(df.loc[Textbook_Appropriate_Language, 'KEY'])
            error_questions.extend(['Textbook_Appropriate_Language'] * Textbook_Appropriate_Language.sum())
            error_messages.extend(['Logic error.'] * Textbook_Appropriate_Language.sum())
            error_qa_status.extend(df.loc[Textbook_Appropriate_Language, 'QA_status'])
            error_qa_by.extend(df.loc[Textbook_Appropriate_Language,'QA_By'])


        
        Textbook_Appropriate_Language_1 = (
             ((df['Children_Have_Grade_Appropriate_Textbooks'] == 2) & (df['Textbook_Appropriate_Language'].isnull()))


        )

        if Textbook_Appropriate_Language_1.any():
            error_keys.extend(df.loc[Textbook_Appropriate_Language_1, 'KEY'])
            error_questions.extend(['Children_Have_Grade_Appropriate_Textbooks_2'] * Textbook_Appropriate_Language_1.sum())
            error_messages.extend(['Logic error.'] * Textbook_Appropriate_Language_1.sum())
            error_qa_status.extend(df.loc[Textbook_Appropriate_Language_1, 'QA_status'])
            error_qa_by.extend(df.loc[Textbook_Appropriate_Language_1,'QA_By'])





        Textbook_Latest_Update_Version = (
             ((df['Children_Have_Grade_Appropriate_Textbooks'] == 1) & (df['Textbook_Latest_Update_Version'].isnull())) | 
             ((df['Children_Have_Grade_Appropriate_Textbooks'] == 0 ) & (df['Textbook_Latest_Update_Version'].notnull()))


        )

        if Textbook_Latest_Update_Version.any():
            error_keys.extend(df.loc[Textbook_Latest_Update_Version, 'KEY'])
            error_questions.extend(['Textbook_Latest_Update_Version'] * Textbook_Latest_Update_Version.sum())
            error_messages.extend(['Logic error.'] * Textbook_Latest_Update_Version.sum())
            error_qa_status.extend(df.loc[Textbook_Latest_Update_Version, 'QA_status'])
            error_qa_by.extend(df.loc[Textbook_Latest_Update_Version,'QA_By'])


        
        Textbook_Latest_Update_Version_2 = (
             ((df['Children_Have_Grade_Appropriate_Textbooks'] == 2) & (df['Textbook_Latest_Update_Version'].isnull()))


        )

        if Textbook_Latest_Update_Version_2.any():
            error_keys.extend(df.loc[Textbook_Latest_Update_Version_2, 'KEY'])
            error_questions.extend(['Textbook_Latest_Update_Version_2'] * Textbook_Latest_Update_Version_2.sum())
            error_messages.extend(['Logic error.'] * Textbook_Latest_Update_Version_2.sum())
            error_qa_status.extend(df.loc[Textbook_Latest_Update_Version_2, 'QA_status'])
            error_qa_by.extend(df.loc[Textbook_Latest_Update_Version_2,'QA_By'])





        Children_Same_Version_Textbook_Lessons_Content = (
             ((df['Children_Have_Grade_Appropriate_Textbooks'] == 1) & (df['Children_Same_Version_Textbook_Lessons_Content'].isnull())) | 
             ((df['Children_Have_Grade_Appropriate_Textbooks'] == 0 ) & (df['Children_Same_Version_Textbook_Lessons_Content'].notnull()))


        )

        if Children_Same_Version_Textbook_Lessons_Content.any():
            error_keys.extend(df.loc[Children_Same_Version_Textbook_Lessons_Content, 'KEY'])
            error_questions.extend(['Children_Same_Version_Textbook_Lessons_Content'] * Children_Same_Version_Textbook_Lessons_Content.sum())
            error_messages.extend(['Logic error.'] * Children_Same_Version_Textbook_Lessons_Content.sum())
            error_qa_status.extend(df.loc[Children_Same_Version_Textbook_Lessons_Content, 'QA_status'])
            error_qa_by.extend(df.loc[Children_Same_Version_Textbook_Lessons_Content,'QA_By'])


        
        Children_Same_Version_Textbook_Lessons_Content_2 = (
             ((df['Children_Have_Grade_Appropriate_Textbooks'] == 2) & (df['Children_Same_Version_Textbook_Lessons_Content'].isnull()))


        )

        if Children_Same_Version_Textbook_Lessons_Content_2.any():
            error_keys.extend(df.loc[Children_Same_Version_Textbook_Lessons_Content_2, 'KEY'])
            error_questions.extend(['Children_Same_Version_Textbook_Lessons_Content_2'] * Children_Same_Version_Textbook_Lessons_Content_2.sum())
            error_messages.extend(['Logic error.'] * Children_Same_Version_Textbook_Lessons_Content_2.sum())
            error_qa_status.extend(df.loc[Children_Same_Version_Textbook_Lessons_Content_2, 'QA_status'])
            error_qa_by.extend(df.loc[Children_Same_Version_Textbook_Lessons_Content_2,'QA_By'])








        
        Water_Dispenser_Clean_Inside_Fit_For_Drinking = (
             ((df['Flast_Available_For_Children'] == 1) & (df['Water_Dispenser_Clean_Inside_Fit_For_Drinking'].isnull())) | 
             ((df['Flast_Available_For_Children'] == 0 ) & (df['Water_Dispenser_Clean_Inside_Fit_For_Drinking'].notnull()))


        )

        if Water_Dispenser_Clean_Inside_Fit_For_Drinking.any():
            error_keys.extend(df.loc[Water_Dispenser_Clean_Inside_Fit_For_Drinking, 'KEY'])
            error_questions.extend(['Water_Dispenser_Clean_Inside_Fit_For_Drinking'] * Water_Dispenser_Clean_Inside_Fit_For_Drinking.sum())
            error_messages.extend(['Logic error.'] * Water_Dispenser_Clean_Inside_Fit_For_Drinking.sum())
            error_qa_status.extend(df.loc[Water_Dispenser_Clean_Inside_Fit_For_Drinking, 'QA_status'])
            error_qa_by.extend(df.loc[Water_Dispenser_Clean_Inside_Fit_For_Drinking,'QA_By'])







        Toilet_Facillity_Accessible_To_Students = (
             ((df['Learning_Space_Toilet_Facility'] == 1) & (df['Toilet_Facillity_Accessible_To_Students'].isnull())) | 
             ((df['Learning_Space_Toilet_Facility'] == 0 ) & (df['Toilet_Facillity_Accessible_To_Students'].notnull()))


        )

        if Toilet_Facillity_Accessible_To_Students.any():
            error_keys.extend(df.loc[Toilet_Facillity_Accessible_To_Students, 'KEY'])
            error_questions.extend(['Toilet_Facillity_Accessible_To_Students'] * Toilet_Facillity_Accessible_To_Students.sum())
            error_messages.extend(['Logic error.'] * Toilet_Facillity_Accessible_To_Students.sum())
            error_qa_status.extend(df.loc[Toilet_Facillity_Accessible_To_Students, 'QA_status'])
            error_qa_by.extend(df.loc[Toilet_Facillity_Accessible_To_Students,'QA_By'])






        
        Toilet_Separated_Boy_Girls = (
             ((df['Toilet_Facillity_Accessible_To_Students'] == 1) & (df['Toilet_Separated_Boy_Girls'].isnull())) | 
             ((df['Toilet_Facillity_Accessible_To_Students'] == 0 ) & (df['Toilet_Separated_Boy_Girls'].notnull()))


        )

        if Toilet_Separated_Boy_Girls.any():
            error_keys.extend(df.loc[Toilet_Separated_Boy_Girls, 'KEY'])
            error_questions.extend(['Toilet_Separated_Boy_Girls'] * Toilet_Separated_Boy_Girls.sum())
            error_messages.extend(['Logic error.'] * Toilet_Separated_Boy_Girls.sum())
            error_qa_status.extend(df.loc[Toilet_Separated_Boy_Girls, 'QA_status'])
            error_qa_by.extend(df.loc[Toilet_Separated_Boy_Girls,'QA_By'])


        
        Toilet_Separated_Boy_Girls_1 = (
             ((df['Toilet_Facillity_Accessible_To_Students'] == 2) & (df['Toilet_Separated_Boy_Girls'].isnull()))


        )

        if Toilet_Separated_Boy_Girls_1.any():
            error_keys.extend(df.loc[Toilet_Separated_Boy_Girls_1, 'KEY'])
            error_questions.extend(['Toilet_Separated_Boy_Girls_1'] * Toilet_Separated_Boy_Girls_1.sum())
            error_messages.extend(['Logic error.'] * Toilet_Separated_Boy_Girls_1.sum())
            error_qa_status.extend(df.loc[Toilet_Separated_Boy_Girls_1, 'QA_status'])
            error_qa_by.extend(df.loc[Toilet_Separated_Boy_Girls_1,'QA_By'])







        Toilet_Clean_Well_Kept = (
             ((df['Toilet_Facillity_Accessible_To_Students'] == 1) & (df['Toilet_Clean_Well_Kept'].isnull())) | 
             ((df['Toilet_Facillity_Accessible_To_Students'] == 0 ) & (df['Toilet_Clean_Well_Kept'].notnull()))


        )

        if Toilet_Clean_Well_Kept.any():
            error_keys.extend(df.loc[Toilet_Clean_Well_Kept, 'KEY'])
            error_questions.extend(['Toilet_Clean_Well_Kept'] * Toilet_Clean_Well_Kept.sum())
            error_messages.extend(['Logic error.'] * Toilet_Clean_Well_Kept.sum())
            error_qa_status.extend(df.loc[Toilet_Clean_Well_Kept, 'QA_status'])
            error_qa_by.extend(df.loc[Toilet_Clean_Well_Kept,'QA_By'])


        
        Toilet_Clean_Well_Kept_1 = (
             ((df['Toilet_Facillity_Accessible_To_Students'] == 2) & (df['Toilet_Clean_Well_Kept'].isnull()))


        )

        if Toilet_Clean_Well_Kept_1.any():
            error_keys.extend(df.loc[Toilet_Clean_Well_Kept_1, 'KEY'])
            error_questions.extend(['Toilet_Clean_Well_Kept_1'] * Toilet_Clean_Well_Kept_1.sum())
            error_messages.extend(['Logic error.'] * Toilet_Clean_Well_Kept_1.sum())
            error_qa_status.extend(df.loc[Toilet_Clean_Well_Kept_1, 'QA_status'])
            error_qa_by.extend(df.loc[Toilet_Clean_Well_Kept_1,'QA_By'])




        Handwashing_Station = (
             ((df['School_CBE_Handwashing_Facility'] == 1) & (df['Handwashing_Station'].isnull())) | 
             ((df['School_CBE_Handwashing_Facility'] == 0 ) & (df['Handwashing_Station'].notnull()))


        )

        if Handwashing_Station.any():
            error_keys.extend(df.loc[Handwashing_Station, 'KEY'])
            error_questions.extend(['Handwashing_Station'] * Handwashing_Station.sum())
            error_messages.extend(['Logic error.'] * Handwashing_Station.sum())
            error_qa_status.extend(df.loc[Handwashing_Station, 'QA_status'])
            error_qa_by.extend(df.loc[Handwashing_Station,'QA_By'])



        Children_Wash_Hands_Soap_Using_Latrin = (
             ((df['School_CBE_Handwashing_Facility'] == 1) & (df['Children_Wash_Hands_Soap_Using_Latrin'].isnull())) | 
             ((df['School_CBE_Handwashing_Facility'] == 0 ) & (df['Children_Wash_Hands_Soap_Using_Latrin'].notnull()))


        )

        if Children_Wash_Hands_Soap_Using_Latrin.any():
            error_keys.extend(df.loc[Children_Wash_Hands_Soap_Using_Latrin, 'KEY'])
            error_questions.extend(['Children_Wash_Hands_Soap_Using_Latrin'] * Children_Wash_Hands_Soap_Using_Latrin.sum())
            error_messages.extend(['Logic error.'] * Children_Wash_Hands_Soap_Using_Latrin.sum())
            error_qa_status.extend(df.loc[Children_Wash_Hands_Soap_Using_Latrin, 'QA_status'])
            error_qa_by.extend(df.loc[Children_Wash_Hands_Soap_Using_Latrin,'QA_By'])





        What_Complaintfeedback_Mechanism_Is_Available = (
             ((df['Learning_Space_Info_Avail_About_Complaint_Feedback_Mechanism'] == 1) & (df['What_Complaintfeedback_Mechanism_Is_Available'].isnull())) | 
             ((df['Learning_Space_Info_Avail_About_Complaint_Feedback_Mechanism'] == 0 ) & (df['What_Complaintfeedback_Mechanism_Is_Available'].notnull()))


        )

        if What_Complaintfeedback_Mechanism_Is_Available.any():
            error_keys.extend(df.loc[What_Complaintfeedback_Mechanism_Is_Available, 'KEY'])
            error_questions.extend(['What_Complaintfeedback_Mechanism_Is_Available'] * What_Complaintfeedback_Mechanism_Is_Available.sum())
            error_messages.extend(['Logic error.'] * What_Complaintfeedback_Mechanism_Is_Available.sum())
            error_qa_status.extend(df.loc[What_Complaintfeedback_Mechanism_Is_Available, 'QA_status'])
            error_qa_by.extend(df.loc[What_Complaintfeedback_Mechanism_Is_Available,'QA_By'])





        What_Complaintfeedback_Mechanism_Is_Available_Other = (
            (df['No_Consent_Reason'] == 8888) & 
            df['What_Complaintfeedback_Mechanism_Is_Available_Other'].isnull()
        )
        if What_Complaintfeedback_Mechanism_Is_Available_Other.any():
            error_keys.extend(df.loc[What_Complaintfeedback_Mechanism_Is_Available_Other, 'KEY'])
            error_questions.extend(['What_Complaintfeedback_Mechanism_Is_Available_Other'] * What_Complaintfeedback_Mechanism_Is_Available_Other.sum())
            error_messages.extend(['What_Complaintfeedback_Mechanism_Is_Available_Other logic error.'] * What_Complaintfeedback_Mechanism_Is_Available_Other.sum())
            error_qa_status.extend(df.loc[What_Complaintfeedback_Mechanism_Is_Available_Other, 'QA_status'])
            error_qa_by.extend(df.loc[What_Complaintfeedback_Mechanism_Is_Available_Other,'QA_By'])


        
        



        Are_The_Students_Aware_Of_The_Available_Feedback_Mechanism_In_The_Learning_Space = (
             ((df['Learning_Space_Info_Avail_About_Complaint_Feedback_Mechanism'] == 1) & (df['Are_The_Students_Aware_Of_The_Available_Feedback_Mechanism_In_The_Learning_Space'].isnull())) | 
             ((df['Learning_Space_Info_Avail_About_Complaint_Feedback_Mechanism'] == 0 ) & (df['Are_The_Students_Aware_Of_The_Available_Feedback_Mechanism_In_The_Learning_Space'].notnull()))


        )

        if Are_The_Students_Aware_Of_The_Available_Feedback_Mechanism_In_The_Learning_Space.any():
            error_keys.extend(df.loc[Are_The_Students_Aware_Of_The_Available_Feedback_Mechanism_In_The_Learning_Space, 'KEY'])
            error_questions.extend(['Are_The_Students_Aware_Of_The_Available_Feedback_Mechanism_In_The_Learning_Space'] * Are_The_Students_Aware_Of_The_Available_Feedback_Mechanism_In_The_Learning_Space.sum())
            error_messages.extend(['Logic error.'] * Are_The_Students_Aware_Of_The_Available_Feedback_Mechanism_In_The_Learning_Space.sum())
            error_qa_status.extend(df.loc[Are_The_Students_Aware_Of_The_Available_Feedback_Mechanism_In_The_Learning_Space, 'QA_status'])
            error_qa_by.extend(df.loc[Are_The_Students_Aware_Of_The_Available_Feedback_Mechanism_In_The_Learning_Space,'QA_By'])





        Has_The_Teacher_Used_The_Feedback_Mechanism_In_The_Last_Three_Months = (
             ((df['Learning_Space_Info_Avail_About_Complaint_Feedback_Mechanism'] == 1) & (df['Has_The_Teacher_Used_The_Feedback_Mechanism_In_The_Last_Three_Months'].isnull())) | 
             ((df['Learning_Space_Info_Avail_About_Complaint_Feedback_Mechanism'] == 0 ) & (df['Has_The_Teacher_Used_The_Feedback_Mechanism_In_The_Last_Three_Months'].notnull()))


        )

        if Has_The_Teacher_Used_The_Feedback_Mechanism_In_The_Last_Three_Months.any():
            error_keys.extend(df.loc[Has_The_Teacher_Used_The_Feedback_Mechanism_In_The_Last_Three_Months, 'KEY'])
            error_questions.extend(['Are_The_Students_Aware_Of_The_Available_Feedback_Mechanism_In_The_Learning_Space'] * Has_The_Teacher_Used_The_Feedback_Mechanism_In_The_Last_Three_Months.sum())
            error_messages.extend(['Logic error.'] * Has_The_Teacher_Used_The_Feedback_Mechanism_In_The_Last_Three_Months.sum())
            error_qa_status.extend(df.loc[Has_The_Teacher_Used_The_Feedback_Mechanism_In_The_Last_Three_Months, 'QA_status'])
            error_qa_by.extend(df.loc[Has_The_Teacher_Used_The_Feedback_Mechanism_In_The_Last_Three_Months,'QA_By'])



        
        Have_The_Students_Used_The_Feedback_Mechanism_In_The_Last_Three_Months = (
             ((df['Learning_Space_Info_Avail_About_Complaint_Feedback_Mechanism'] == 1) & (df['Have_The_Students_Used_The_Feedback_Mechanism_In_The_Last_Three_Months'].isnull())) | 
             ((df['Learning_Space_Info_Avail_About_Complaint_Feedback_Mechanism'] == 0 ) & (df['Have_The_Students_Used_The_Feedback_Mechanism_In_The_Last_Three_Months'].notnull()))


        )

        if Have_The_Students_Used_The_Feedback_Mechanism_In_The_Last_Three_Months.any():
            error_keys.extend(df.loc[Have_The_Students_Used_The_Feedback_Mechanism_In_The_Last_Three_Months, 'KEY'])
            error_questions.extend(['Have_The_Students_Used_The_Feedback_Mechanism_In_The_Last_Three_Months'] * Have_The_Students_Used_The_Feedback_Mechanism_In_The_Last_Three_Months.sum())
            error_messages.extend(['Logic error.'] * Have_The_Students_Used_The_Feedback_Mechanism_In_The_Last_Three_Months.sum())
            error_qa_status.extend(df.loc[Have_The_Students_Used_The_Feedback_Mechanism_In_The_Last_Three_Months, 'QA_status'])
            error_qa_by.extend(df.loc[Have_The_Students_Used_The_Feedback_Mechanism_In_The_Last_Three_Months,'QA_By'])



   




        What_Are_The_Challenge_Issues_learning_Space = (
             ((df['Is_There_Any_Challenge_Issue_In_The_Learning_Space_You_Would_Like_To_Report'] == 1) & (df['What_Are_The_Challenge_Issues_learning_Space'].isnull())) | 
             ((df['Is_There_Any_Challenge_Issue_In_The_Learning_Space_You_Would_Like_To_Report'] == 0 ) & (df['What_Are_The_Challenge_Issues_learning_Space'].notnull()))


        )

        if What_Are_The_Challenge_Issues_learning_Space.any():
            error_keys.extend(df.loc[What_Are_The_Challenge_Issues_learning_Space, 'KEY'])
            error_questions.extend(['What_Are_The_Challenge_Issues_learning_Space'] * What_Are_The_Challenge_Issues_learning_Space.sum())
            error_messages.extend(['Logic error.'] * What_Are_The_Challenge_Issues_learning_Space.sum())
            error_qa_status.extend(df.loc[What_Are_The_Challenge_Issues_learning_Space, 'QA_status'])
            error_qa_by.extend(df.loc[What_Are_The_Challenge_Issues_learning_Space,'QA_By'])






        Is_There_Any_Translation = df['What_Are_The_Challenge_Issues_learning_Space'].notnull() & (df['Is_There_Any_Challenge_Issue_In_The_Learning_Space_You_Would_Like_To_Report_Translation'].isnull() | 
         df['Is_There_Any_Challenge_Issue_In_The_Learning_Space_You_Would_Like_To_Report_Translation'].astype(str).str.contains('-', regex=True, na=False))
        


        if Is_There_Any_Translation.any():
            error_keys.extend(df.loc[Is_There_Any_Translation, 'KEY'])
            error_questions.extend(['Is_There_Any_Challenge_Issue_In_The_Learning_Space_You_Would_Like_To_Report_Translation'] * Is_There_Any_Translation.sum())
            error_messages.extend(['Translation Missing'] * Is_There_Any_Translation.sum())
            error_qa_status.extend(df.loc[Is_There_Any_Translation,'QA_status'])
            error_qa_by.extend(df.loc[Is_There_Any_Translation,'QA_By'])




        What_Are_The_Names_Of_The_Clubs = (
             ((df['Does_The_School_Have_A_Childrens_Club'] == 1) & (df['What_Are_The_Names_Of_The_Clubs'].isnull())) | 
             ((df['Does_The_School_Have_A_Childrens_Club'] == 0 ) & (df['What_Are_The_Names_Of_The_Clubs'].notnull()))


        )


        if What_Are_The_Names_Of_The_Clubs.any():
            error_keys.extend(df.loc[What_Are_The_Names_Of_The_Clubs, 'KEY'])
            error_questions.extend(['What_Are_The_Names_Of_The_Clubs'] * What_Are_The_Names_Of_The_Clubs.sum())
            error_messages.extend(['Logic error'] * What_Are_The_Names_Of_The_Clubs.sum())
            error_qa_status.extend(df.loc[What_Are_The_Names_Of_The_Clubs,'QA_status'])
            error_qa_by.extend(df.loc[What_Are_The_Names_Of_The_Clubs,'QA_By'])



        How_Teacher_Received_Salary = (
             ((df['Did_Teacher_Receive_Last_Month_Salary'] == 1) & (df['How_Teacher_Received_Salary'].isnull())) | 
             ((df['Did_Teacher_Receive_Last_Month_Salary'] == 0 ) & (df['How_Teacher_Received_Salary'].notnull()))


        )


        if How_Teacher_Received_Salary.any():
            error_keys.extend(df.loc[How_Teacher_Received_Salary, 'KEY'])
            error_questions.extend(['How_Teacher_Received_Salary'] * How_Teacher_Received_Salary.sum())
            error_messages.extend(['Logic error'] * How_Teacher_Received_Salary.sum())
            error_qa_status.extend(df.loc[How_Teacher_Received_Salary,'QA_status'])
            error_qa_by.extend(df.loc[How_Teacher_Received_Salary,'QA_By'])







        How_Teacher_Received_Salary_Other = (
            (df['How_Teacher_Received_Salary'] == 8888) & 
            df['How_Teacher_Received_Salary_Other'].isnull()
        )
        if How_Teacher_Received_Salary_Other.any():
            error_keys.extend(df.loc[How_Teacher_Received_Salary_Other, 'KEY'])
            error_questions.extend(['How_Teacher_Received_Salary_Other'] * How_Teacher_Received_Salary_Other.sum())
            error_messages.extend(['How_Teacher_Received_Salary_Other is blank.'] * How_Teacher_Received_Salary_Other.sum())
            error_qa_status.extend(df.loc[How_Teacher_Received_Salary_Other, 'QA_status'])
            error_qa_by.extend(df.loc[How_Teacher_Received_Salary_Other,'QA_By'])





        Delay_In_receiving_Salary = (
             ((df['Did_Teacher_Receive_Last_Month_Salary'] == 1) & (df['Delay_In_receiving_Salary'].isnull())) | 
             ((df['Did_Teacher_Receive_Last_Month_Salary'] == 0 ) & (df['Delay_In_receiving_Salary'].notnull()))


        )


        if Delay_In_receiving_Salary.any():
            error_keys.extend(df.loc[Delay_In_receiving_Salary, 'KEY'])
            error_questions.extend(['Delay_In_receiving_Salary'] * Delay_In_receiving_Salary.sum())
            error_messages.extend(['Logic error'] * Delay_In_receiving_Salary.sum())
            error_qa_status.extend(df.loc[Delay_In_receiving_Salary,'QA_status'])
            error_qa_by.extend(df.loc[Delay_In_receiving_Salary,'QA_By'])




        What_Type_Training = (
             ((df['Teacher_Received_Training_Since_Recrutment'] == 1) & (df['What_Type_Training'].isnull())) | 
             ((df['Teacher_Received_Training_Since_Recrutment'] == 0 ) & (df['What_Type_Training'].notnull()))


        )


        if What_Type_Training.any():
            error_keys.extend(df.loc[What_Type_Training, 'KEY'])
            error_questions.extend(['What_Type_Training'] * What_Type_Training.sum())
            error_messages.extend(['Logic error'] * What_Type_Training.sum())
            error_qa_status.extend(df.loc[What_Type_Training,'QA_status'])
            error_qa_by.extend(df.loc[What_Type_Training,'QA_By'])





        What_Type_Training_Other = (
            (df['What_Type_Training'] == 8888) & 
            df['What_Type_Training_Other'].isnull()
        )
        if What_Type_Training_Other.any():
            error_keys.extend(df.loc[What_Type_Training_Other, 'KEY'])
            error_questions.extend(['What_Type_Training_Other'] * What_Type_Training_Other.sum())
            error_messages.extend(['What_Type_Training_Other is blank.'] * What_Type_Training_Other.sum())
            error_qa_status.extend(df.loc[What_Type_Training_Other, 'QA_status'])
            error_qa_by.extend(df.loc[What_Type_Training_Other,'QA_By'])




        When_Was_The_Last_Time_Social_Worker_Moblizer_Visited = (
             ((df['Social_Worker_Moblizer_Visited_Classroom_Last_Month'] == 1) & (df['When_Was_The_Last_Time_Social_Worker_Moblizer_Visited'].isnull())) | 
             ((df['Social_Worker_Moblizer_Visited_Classroom_Last_Month'] == 0 ) & (df['When_Was_The_Last_Time_Social_Worker_Moblizer_Visited'].notnull()))


        )


        if When_Was_The_Last_Time_Social_Worker_Moblizer_Visited.any():
            error_keys.extend(df.loc[When_Was_The_Last_Time_Social_Worker_Moblizer_Visited, 'KEY'])
            error_questions.extend(['When_Was_The_Last_Time_Social_Worker_Moblizer_Visited'] * When_Was_The_Last_Time_Social_Worker_Moblizer_Visited.sum())
            error_messages.extend(['Logic error'] * When_Was_The_Last_Time_Social_Worker_Moblizer_Visited.sum())
            error_qa_status.extend(df.loc[When_Was_The_Last_Time_Social_Worker_Moblizer_Visited,'QA_status'])
            error_qa_by.extend(df.loc[When_Was_The_Last_Time_Social_Worker_Moblizer_Visited,'QA_By'])





        Worker_Socail_Mobilizer_Provided_Teacher_With_Feedback_Observing_Lesson = (
             ((df['Social_Worker_Moblizer_Visited_Classroom_Last_Month'] == 1) & (df['Worker_Socail_Mobilizer_Provided_Teacher_With_Feedback_Observing_Lesson'].isnull())) | 
             ((df['Social_Worker_Moblizer_Visited_Classroom_Last_Month'] == 0 ) & (df['Worker_Socail_Mobilizer_Provided_Teacher_With_Feedback_Observing_Lesson'].notnull()))


        )


        if Worker_Socail_Mobilizer_Provided_Teacher_With_Feedback_Observing_Lesson.any():
            error_keys.extend(df.loc[Worker_Socail_Mobilizer_Provided_Teacher_With_Feedback_Observing_Lesson, 'KEY'])
            error_questions.extend(['Worker_Socail_Mobilizer_Provided_Teacher_With_Feedback_Observing_Lesson'] * Worker_Socail_Mobilizer_Provided_Teacher_With_Feedback_Observing_Lesson.sum())
            error_messages.extend(['Logic error'] * Worker_Socail_Mobilizer_Provided_Teacher_With_Feedback_Observing_Lesson.sum())
            error_qa_status.extend(df.loc[Worker_Socail_Mobilizer_Provided_Teacher_With_Feedback_Observing_Lesson,'QA_status'])
            error_qa_by.extend(df.loc[Worker_Socail_Mobilizer_Provided_Teacher_With_Feedback_Observing_Lesson,'QA_By'])






        How_Teacher_Assess_Support_Provided_Socail_Worker_Mobilizer = (
             ((df['Worker_Socail_Mobilizer_Provided_Teacher_With_Feedback_Observing_Lesson'] == 1) & (df['How_Teacher_Assess_Support_Provided_Socail_Worker_Mobilizer'].isnull())) | 
             ((df['Worker_Socail_Mobilizer_Provided_Teacher_With_Feedback_Observing_Lesson'] == 0 ) & (df['How_Teacher_Assess_Support_Provided_Socail_Worker_Mobilizer'].notnull()))


        )


        if How_Teacher_Assess_Support_Provided_Socail_Worker_Mobilizer.any():
            error_keys.extend(df.loc[How_Teacher_Assess_Support_Provided_Socail_Worker_Mobilizer, 'KEY'])
            error_questions.extend(['How_Teacher_Assess_Support_Provided_Socail_Worker_Mobilizer'] * How_Teacher_Assess_Support_Provided_Socail_Worker_Mobilizer.sum())
            error_messages.extend(['Logic error'] * How_Teacher_Assess_Support_Provided_Socail_Worker_Mobilizer.sum())
            error_qa_status.extend(df.loc[How_Teacher_Assess_Support_Provided_Socail_Worker_Mobilizer,'QA_status'])
            error_qa_by.extend(df.loc[How_Teacher_Assess_Support_Provided_Socail_Worker_Mobilizer,'QA_By'])








        Last_Time_Attendance_Was_Recorded_School_Managment_Shora_Visited = (
             ((df['School_Managment_Shora_Visited_Classroom_Last_Month'] == 1) & (df['Last_Time_Attendance_Was_Recorded_School_Managment_Shora_Visited'].isnull())) | 
             ((df['School_Managment_Shora_Visited_Classroom_Last_Month'] == 0 ) & (df['Last_Time_Attendance_Was_Recorded_School_Managment_Shora_Visited'].notnull()))


        )


        if Last_Time_Attendance_Was_Recorded_School_Managment_Shora_Visited.any():
            error_keys.extend(df.loc[Last_Time_Attendance_Was_Recorded_School_Managment_Shora_Visited, 'KEY'])
            error_questions.extend(['How_Teacher_Assess_Support_Provided_Socail_Worker_Mobilizer'] * Last_Time_Attendance_Was_Recorded_School_Managment_Shora_Visited.sum())
            error_messages.extend(['Logic error'] * Last_Time_Attendance_Was_Recorded_School_Managment_Shora_Visited.sum())
            error_qa_status.extend(df.loc[Last_Time_Attendance_Was_Recorded_School_Managment_Shora_Visited,'QA_status'])
            error_qa_by.extend(df.loc[Last_Time_Attendance_Was_Recorded_School_Managment_Shora_Visited,'QA_By'])







        Shcool_Managment_Shura_Provided_Teacher_With_Feedback_Observing_Lesson = (
             ((df['School_Managment_Shora_Visited_Classroom_Last_Month'] == 1) & (df['Shcool_Managment_Shura_Provided_Teacher_With_Feedback_Observing_Lesson'].isnull())) | 
             ((df['School_Managment_Shora_Visited_Classroom_Last_Month'] == 0 ) & (df['Shcool_Managment_Shura_Provided_Teacher_With_Feedback_Observing_Lesson'].notnull()))


        )


        if Shcool_Managment_Shura_Provided_Teacher_With_Feedback_Observing_Lesson.any():
            error_keys.extend(df.loc[Shcool_Managment_Shura_Provided_Teacher_With_Feedback_Observing_Lesson, 'KEY'])
            error_questions.extend(['Shcool_Managment_Shura_Provided_Teacher_With_Feedback_Observing_Lesson'] * Shcool_Managment_Shura_Provided_Teacher_With_Feedback_Observing_Lesson.sum())
            error_messages.extend(['Logic error'] * Shcool_Managment_Shura_Provided_Teacher_With_Feedback_Observing_Lesson.sum())
            error_qa_status.extend(df.loc[Shcool_Managment_Shura_Provided_Teacher_With_Feedback_Observing_Lesson,'QA_status'])
            error_qa_by.extend(df.loc[Shcool_Managment_Shura_Provided_Teacher_With_Feedback_Observing_Lesson,'QA_By'])






        How_Does_Teacher_Assess_Support_Provided_Shcool_Managment_Shura = (
             ((df['Shcool_Managment_Shura_Provided_Teacher_With_Feedback_Observing_Lesson'] == 1) & (df['How_Does_Teacher_Assess_Support_Provided_Shcool_Managment_Shura'].isnull())) | 
             ((df['Shcool_Managment_Shura_Provided_Teacher_With_Feedback_Observing_Lesson'] == 0 ) & (df['How_Does_Teacher_Assess_Support_Provided_Shcool_Managment_Shura'].notnull()))


        )


        if How_Does_Teacher_Assess_Support_Provided_Shcool_Managment_Shura.any():
            error_keys.extend(df.loc[How_Does_Teacher_Assess_Support_Provided_Shcool_Managment_Shura, 'KEY'])
            error_questions.extend(['How_Does_Teacher_Assess_Support_Provided_Shcool_Managment_Shura'] * How_Does_Teacher_Assess_Support_Provided_Shcool_Managment_Shura.sum())
            error_messages.extend(['Logic error'] * How_Does_Teacher_Assess_Support_Provided_Shcool_Managment_Shura.sum())
            error_qa_status.extend(df.loc[How_Does_Teacher_Assess_Support_Provided_Shcool_Managment_Shura,'QA_status'])
            error_qa_by.extend(df.loc[How_Does_Teacher_Assess_Support_Provided_Shcool_Managment_Shura,'QA_By'])







        
        How_Far_Is_The_HUB_From_Class = (
                ((df['Does_CBE_Has_HUB_School'] ==1) & (df['Type_Of_Learning_Space'] == 1) & (df['How_Far_Is_The_HUB_From_Class'].isnull())) |
                ((df['Does_CBE_Has_HUB_School'] ==1) & (df['Type_Of_Learning_Space'] == 3) & (df['How_Far_Is_The_HUB_From_Class'].notnull())) | 
                ((df['Does_CBE_Has_HUB_School'] ==0) & df['How_Far_Is_The_HUB_From_Class'].notnull())
    )

        if How_Far_Is_The_HUB_From_Class.any():
            error_keys.extend(df.loc[How_Far_Is_The_HUB_From_Class, 'KEY'])
            error_questions.extend(['How_Far_Is_The_HUB_From_Class'] * How_Far_Is_The_HUB_From_Class.sum())
            error_messages.extend(['Logic error.'] * How_Far_Is_The_HUB_From_Class.sum())
            error_qa_status.extend(df.loc[How_Far_Is_The_HUB_From_Class, 'QA_status'])
            error_qa_by.extend(df.loc[How_Far_Is_The_HUB_From_Class,'QA_By'])

        How_Far_Is_The_HUB_From_Class_1 = (
            ((df['Does_CBE_Has_HUB_School'] ==1) & (df['Type_Of_Learning_Space'] == 2) & (df['How_Far_Is_The_HUB_From_Class'].isnull()))
        )

        if How_Far_Is_The_HUB_From_Class_1.any():
            error_keys.extend(df.loc[How_Far_Is_The_HUB_From_Class_1, 'KEY'])
            error_questions.extend(['How_Far_Is_The_HUB_From_Class_1'] * How_Far_Is_The_HUB_From_Class_1.sum())
            error_messages.extend(['Logic error.'] * How_Far_Is_The_HUB_From_Class_1.sum())
            error_qa_status.extend(df.loc[How_Far_Is_The_HUB_From_Class_1, 'QA_status'])
            error_qa_by.extend(df.loc[How_Far_Is_The_HUB_From_Class_1,'QA_By'])






        

        HUB_School_Headmaster_Visited_CBE_ALC_Year = (
                ((df['Does_CBE_Has_HUB_School'] ==1) & (df['Type_Of_Learning_Space'] == 1) & (df['HUB_School_Headmaster_Visited_CBE_ALC_Year'].isnull())) |
                ((df['Does_CBE_Has_HUB_School'] ==1) & (df['Type_Of_Learning_Space'] == 3) & (df['HUB_School_Headmaster_Visited_CBE_ALC_Year'].notnull())) | 
                ((df['Does_CBE_Has_HUB_School'] ==0) & df['HUB_School_Headmaster_Visited_CBE_ALC_Year'].notnull())
    )

        if HUB_School_Headmaster_Visited_CBE_ALC_Year.any():
            error_keys.extend(df.loc[HUB_School_Headmaster_Visited_CBE_ALC_Year, 'KEY'])
            error_questions.extend(['HUB_School_Headmaster_Visited_CBE_ALC_Year'] * HUB_School_Headmaster_Visited_CBE_ALC_Year.sum())
            error_messages.extend(['Logic error.'] * HUB_School_Headmaster_Visited_CBE_ALC_Year.sum())
            error_qa_status.extend(df.loc[HUB_School_Headmaster_Visited_CBE_ALC_Year, 'QA_status'])
            error_qa_by.extend(df.loc[HUB_School_Headmaster_Visited_CBE_ALC_Year,'QA_By'])

        HUB_School_Headmaster_Visited_CBE_ALC_Year_1 = (
            ((df['Does_CBE_Has_HUB_School'] ==1) & (df['Type_Of_Learning_Space'] == 2) & (df['HUB_School_Headmaster_Visited_CBE_ALC_Year'].isnull()))
        )

        if HUB_School_Headmaster_Visited_CBE_ALC_Year_1.any():
            error_keys.extend(df.loc[HUB_School_Headmaster_Visited_CBE_ALC_Year_1, 'KEY'])
            error_questions.extend(['HUB_School_Headmaster_Visited_CBE_ALC_Year_1'] * HUB_School_Headmaster_Visited_CBE_ALC_Year_1.sum())
            error_messages.extend(['Logic error.'] * HUB_School_Headmaster_Visited_CBE_ALC_Year_1.sum())
            error_qa_status.extend(df.loc[HUB_School_Headmaster_Visited_CBE_ALC_Year_1, 'QA_status'])
            error_qa_by.extend(df.loc[HUB_School_Headmaster_Visited_CBE_ALC_Year_1,'QA_By'])

        


        

        How_Many_Times_Since_Beginning_Year = (
                ((df['Does_CBE_Has_HUB_School'] ==1) & (df['HUB_School_Headmaster_Visited_CBE_ALC_Year'] == 1) & (df['How_Many_Times_Since_Beginning_Year'].isnull())) |
                ((df['Does_CBE_Has_HUB_School'] ==1) & (df['HUB_School_Headmaster_Visited_CBE_ALC_Year'] == 0) & (df['How_Many_Times_Since_Beginning_Year'].notnull())) |
                ((df['Does_CBE_Has_HUB_School'] ==0) & df['HUB_School_Headmaster_Visited_CBE_ALC_Year'].notnull())

        )  


        if How_Many_Times_Since_Beginning_Year.any():
            error_keys.extend(df.loc[How_Many_Times_Since_Beginning_Year, 'KEY'])
            error_questions.extend(['How_Many_Times_Since_Beginning_Year'] * How_Many_Times_Since_Beginning_Year.sum())
            error_messages.extend(['Logic error.'] * How_Many_Times_Since_Beginning_Year.sum())
            error_qa_status.extend(df.loc[How_Many_Times_Since_Beginning_Year, 'QA_status'])
            error_qa_by.extend(df.loc[How_Many_Times_Since_Beginning_Year,'QA_By'])





        How_Many_Schools_CBE_Linked = (
             ((df['Does_CBE_Has_HUB_School'] == 1) & (df['How_Many_Schools_CBE_Linked'].isnull())) | 
             ((df['Does_CBE_Has_HUB_School'] == 0 ) & (df['How_Many_Schools_CBE_Linked'].notnull()))


        )


        if How_Many_Schools_CBE_Linked.any():
            error_keys.extend(df.loc[How_Many_Schools_CBE_Linked, 'KEY'])
            error_questions.extend(['How_Many_Schools_CBE_Linked'] * How_Many_Schools_CBE_Linked.sum())
            error_messages.extend(['Logic error'] * How_Many_Schools_CBE_Linked.sum())
            error_qa_status.extend(df.loc[How_Many_Schools_CBE_Linked,'QA_status'])
            error_qa_by.extend(df.loc[How_Many_Schools_CBE_Linked,'QA_By'])




        TPM_CBE_ID = df['TPM_CBE_ID'].duplicated()
        if TPM_CBE_ID.any():

            error_keys.extend(df.loc[TPM_CBE_ID, 'KEY'])
            error_questions.extend(['TPM_CBE_ID'] * TPM_CBE_ID.sum())
            error_messages.extend(['Duplicate CBE School'] * TPM_CBE_ID.sum())
            error_qa_status.extend(df.loc[TPM_CBE_ID, 'QA_status'])
            error_qa_by.extend(df.loc[error_keys,'QA_By'])            

        



        qa_status_spell = (
            ((df['QA_status'].notnull()) & (~df['QA_status'].isin(['APP', 'REJ', 'PEN'])))
        )
            
        
        if qa_status_spell.any():
            error_keys.extend(df.loc[qa_status_spell, 'KEY'])
            error_questions.extend(['QA_status'] * qa_status_spell.sum())
            error_messages.extend(['Incorrect spelling.'] * qa_status_spell.sum())
            error_qa_status.extend(df.loc[qa_status_spell,'QA_status'])
            error_qa_by.extend(df.loc[qa_status_spell,'QA_By'])


        #Translation Tool 1


        village_town_error = df['Village_Town_Name'].astype(str).str.contains('[آ-ی]', regex=True, na=False)
        if village_town_error.any():
            error_keys.extend(df.loc[village_town_error, 'KEY'])
            error_questions.extend(['Village_Town_Name'] * village_town_error.sum())
            error_messages.extend(['Translation Missing'] * village_town_error.sum())
            error_qa_status.extend(df.loc[village_town_error,'QA_status'])
            error_qa_by.extend(df.loc[village_town_error,'QA_By'])


        
        no_consent_reason_error = df['No_Consent_Reason_Other'].astype(str).str.contains('[آ-ی]', regex=True, na=False)
        if no_consent_reason_error.any():
            error_keys.extend(df.loc[no_consent_reason_error, 'KEY'])
            error_questions.extend(['No_Consent_Reason_Other'] * no_consent_reason_error.sum())
            error_messages.extend(['Translation Missing'] * no_consent_reason_error.sum())
            error_qa_status.extend(df.loc[no_consent_reason_error,'QA_status'])
            error_qa_by.extend(df.loc[no_consent_reason_error,'QA_By'])



        # Rule 3: Name_Resp
        IP_Name_1 = df['IP_Name'].astype(str).str.contains('[آ-ی]', regex=True, na=False)
        if IP_Name_1.any():
            error_keys.extend(df.loc[IP_Name_1, 'KEY'])
            error_questions.extend(['IP_Name'] * IP_Name_1.sum())
            error_messages.extend(['Translation Missing'] * IP_Name_1.sum())
            error_qa_status.extend(df.loc[IP_Name_1,'QA_status'])
            error_qa_by.extend(df.loc[IP_Name_1,'QA_By'])



        
        village_town_error = df['Village_Town_Name'].astype(str).str.contains('[آ-ی]', regex=True, na=False)
        if village_town_error.any():
            error_keys.extend(df.loc[village_town_error, 'KEY'])
            error_questions.extend(['Village_Town_Name'] * village_town_error.sum())
            error_messages.extend(['Translation Missing'] * village_town_error.sum())
            error_qa_status.extend(df.loc[village_town_error,'QA_status'])
            error_qa_by.extend(df.loc[village_town_error,'QA_By'])




        School_Name_Type_1 = df['School_Name_Type'].astype(str).str.contains('[آ-ی]', regex=True, na=False)
        if School_Name_Type_1.any():
            error_keys.extend(df.loc[School_Name_Type_1, 'KEY'])
            error_questions.extend(['School_Name_Type'] * School_Name_Type_1.sum())
            error_messages.extend(['Translation Missing'] * School_Name_Type_1.sum())
            error_qa_status.extend(df.loc[School_Name_Type_1,'QA_status'])
            error_qa_by.extend(df.loc[School_Name_Type_1,'QA_By'])




        


        Dropouts_Reason_Other_1 = df['Dropouts_Reason_Other'].astype(str).str.contains('[آ-ی]', regex=True, na=False)
        if Dropouts_Reason_Other_1.any():
            error_keys.extend(df.loc[Dropouts_Reason_Other_1, 'KEY'])
            error_questions.extend(['Dropouts_Reason_Other'] * Dropouts_Reason_Other_1.sum())
            error_messages.extend(['Translation Missing'] * Dropouts_Reason_Other_1.sum())
            error_qa_status.extend(df.loc[Dropouts_Reason_Other_1,'QA_status'])
            error_qa_by.extend(df.loc[Dropouts_Reason_Other_1,'QA_By'])



        
        Which_School_Obtained_Asaas_Number_Trans = df['Which_School_Obtained_Asaas_Number'].astype(str).str.contains('[آ-ی]', regex=True, na=False)
        if Which_School_Obtained_Asaas_Number_Trans.any():
            error_keys.extend(df.loc[Which_School_Obtained_Asaas_Number_Trans, 'KEY'])
            error_questions.extend(['Which_School_Obtained_Asaas_Number'] * Which_School_Obtained_Asaas_Number_Trans.sum())
            error_messages.extend(['Translation Missing'] * Which_School_Obtained_Asaas_Number_Trans.sum())
            error_qa_status.extend(df.loc[Which_School_Obtained_Asaas_Number_Trans,'QA_status'])
            error_qa_by.extend(df.loc[Which_School_Obtained_Asaas_Number_Trans,'QA_By'])


        Do_Children_Have_MOE_Appropriate_Textbook_Other_Tran = df['Do_Children_Have_MOE_Appropriate_Textbook_Other'].astype(str).str.contains('[آ-ی]', regex=True, na=False)
        if Do_Children_Have_MOE_Appropriate_Textbook_Other_Tran.any():
            error_keys.extend(df.loc[Do_Children_Have_MOE_Appropriate_Textbook_Other_Tran, 'KEY'])
            error_questions.extend(['Do_Children_Have_MOE_Appropriate_Textbook_Other'] * Do_Children_Have_MOE_Appropriate_Textbook_Other_Tran.sum())
            error_messages.extend(['Translation Missing'] * Do_Children_Have_MOE_Appropriate_Textbook_Other_Tran.sum())
            error_qa_status.extend(df.loc[Do_Children_Have_MOE_Appropriate_Textbook_Other_Tran,'QA_status'])
            error_qa_by.extend(df.loc[Do_Children_Have_MOE_Appropriate_Textbook_Other_Tran,'QA_By'])



        

        What_Complaintfeedback_Mechanism_Is_Available_Other_Trans = df['What_Complaintfeedback_Mechanism_Is_Available_Other'].astype(str).str.contains('[آ-ی]', regex=True, na=False)
        if What_Complaintfeedback_Mechanism_Is_Available_Other_Trans.any():
            error_keys.extend(df.loc[What_Complaintfeedback_Mechanism_Is_Available_Other_Trans, 'KEY'])
            error_questions.extend(['What_Complaintfeedback_Mechanism_Is_Available_Other'] * What_Complaintfeedback_Mechanism_Is_Available_Other_Trans.sum())
            error_messages.extend(['Translation Missing'] * What_Complaintfeedback_Mechanism_Is_Available_Other_Trans.sum())
            error_qa_status.extend(df.loc[What_Complaintfeedback_Mechanism_Is_Available_Other_Trans,'QA_status'])
            error_qa_by.extend(df.loc[What_Complaintfeedback_Mechanism_Is_Available_Other_Trans,'QA_By'])




        What_Are_The_Names_Of_The_Clubs_Trans = df['What_Are_The_Names_Of_The_Clubs'].astype(str).str.contains('[آ-ی]', regex=True, na=False)
        if What_Are_The_Names_Of_The_Clubs_Trans.any():
            error_keys.extend(df.loc[What_Are_The_Names_Of_The_Clubs_Trans, 'KEY'])
            error_questions.extend(['What_Are_The_Names_Of_The_Clubs'] * What_Are_The_Names_Of_The_Clubs_Trans.sum())
            error_messages.extend(['Translation Missing'] * What_Are_The_Names_Of_The_Clubs_Trans.sum())
            error_qa_status.extend(df.loc[What_Are_The_Names_Of_The_Clubs_Trans,'QA_status'])
            error_qa_by.extend(df.loc[What_Are_The_Names_Of_The_Clubs_Trans,'QA_By'])






        How_Teacher_Received_Salary_Other_Trans = df['How_Teacher_Received_Salary_Other'].astype(str).str.contains('[آ-ی]', regex=True, na=False)
        if How_Teacher_Received_Salary_Other_Trans.any():
            error_keys.extend(df.loc[How_Teacher_Received_Salary_Other_Trans, 'KEY'])
            error_questions.extend(['How_Teacher_Received_Salary_Other'] * How_Teacher_Received_Salary_Other_Trans.sum())
            error_messages.extend(['Translation Missing'] * How_Teacher_Received_Salary_Other_Trans.sum())
            error_qa_status.extend(df.loc[How_Teacher_Received_Salary_Other_Trans,'QA_status'])
            error_qa_by.extend(df.loc[How_Teacher_Received_Salary_Other_Trans,'QA_By'])





        What_Type_Training_Other_1 = df['What_Type_Training_Other'].astype(str).str.contains('[آ-ی]', regex=True, na=False)
        if What_Type_Training_Other_1.any():
                error_keys.extend(df.loc[What_Type_Training_Other_1, 'KEY'])
                error_questions.extend(['What_Type_Training_Other'] * What_Type_Training_Other_1.sum())
                error_messages.extend(['Translation Missing'] * What_Type_Training_Other_1.sum())
                error_qa_status.extend(df.loc[What_Type_Training_Other_1,'QA_status'])
                error_qa_by.extend(df.loc[What_Type_Training_Other_1,'QA_By'])



        # Create a DataFrame to store the error details
        Trans = pd.DataFrame({
            'KEY': error_keys,
            'Question': error_questions,
            'Error Message': error_messages,
            'QA Status': error_qa_status,
            'QA By': error_qa_by
        })


        df = pd.DataFrame(Trans)

        
        # Example usage of the dataset
        if Trans is not None:
            st.subheader('Dataset Errors')
            st.write(df)

            buffer = io.BytesIO()

            Trans.to_excel(buffer, sheet_name='Errors', index=False, engine='openpyxl')

            buffer.seek(0)

            st.download_button(
                label="Download data as Excel",
                data=buffer,
                file_name='Tool_1_Errors.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )  





if __name__ == '__main__':
    main()




if     st.button('Process Tool 1 dataset'):
          Tool_1_fun()


if     st.button('Process Tool 4 dataset'):
          Tool_4_fun()

if     st.button('Process Tool 6 dataset'):
          Tool_6_fun()

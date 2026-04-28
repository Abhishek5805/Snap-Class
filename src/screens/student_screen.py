import streamlit as st
from src.ui.base_layout import  style_background_dashboard,style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendence,get_face_embedding,train_classifier
from src.pipelines.voice_pippeline import get_voice_embedding
from src.database.db import get_all_students,create_student,get_student_subjects,get_student_attendence
import time

from src.components.dialog_enroll import enroll_dialog


def student_dashboard():
    student_data=st.session_state.student_data
    student_id=student_data['student_id']
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"Welcome, {student_data['name']}!")

        if st.button("Logout",type="secondary",key="loginbackbtn",shortcut="control+backspace"):
            st.session_state['is_logged_in']=False
            del st.session_state.student_data

            st.rerun()
    st.space()

    c1,c2=st.columns(2)
    with c1:
        st.header("you Enrolled Subjects")
    with c2:
        if st.button("enrolled in Subject",type="primary",width="stretch",icon=":material/add_circle:"):
            enroll_dialog()
    st.divider()
    with st.spinner("Loading your Enrolled Subjects..."):
        subjects=get_student_subjects(student_id)
        logs=get_student_attendence(student_id)

    stats_map={}
    for log in logs:
        sid=log['subject_id']

        if sid not in stats_map:
            stats_map[sid]={'total':0,'attended':0}

        stats_map[sid]['total']+=1

        if log.get('is_present'):
            stats_map[sid]['attended']+=1

    cols=st.columns(2)
    for i,sub_node in enumerate(subjects):
        sub=sub_node['subjects']
        sid=sub['subject_id']
        stat=stats_map.get(sid,{'total':0,'attended':0})
        with cols[i%2]:
            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=[
                    ('📅','Total',stat['total']),
                    ('✅','Attended',stat['attended'])
                ]
            )
            
    footer_dashboard()


def student_screen():

    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to home",type="secondary",key="loginbackbtn",shortcut="control+backspace"):
            st.session_state['login_type']=None
            st.rerun()
    
    st.header("Login using face id",text_alignment="center")

    st.space()
    st.space()
    show_registration=False
    photo_source=st.camera_input("Position your face in the center")
    if photo_source:
        img=np.array(Image.open(photo_source))

        with st.spinner("Processing..."):
            detected,all_ids,num_faces=predict_attendence(img)

        if num_faces==0:
            st.warning("No face detected. Please try again.")
        elif num_faces>1:
            st.warning("Multiple faces detected. Please ensure only your face is visible and try again.")
        else:
            if detected:
                student_id=list(detected.keys())[0]
                all_students=get_all_students()
                student=next((s for s in all_students if s['student_id']==student_id),None)
                if student:
                    st.session_state.is_logged_in=True
                    st.session_state.user_role='student'
                    st.session_state.student_data=student
                    st.toast(f"Welcome back, {student.get('name')}!",icon="👋")
                    time.sleep(1)
                    st.rerun()
            else:
                st.info("Face not recognized. You might be new srudent")
                show_registration=True

    if show_registration:
        with st.container(border=True):
            st.header("register new profile")
            new_name=st.text_input("Enter your name",placeholder="Abhishek Shinde")
            st.subheader('optional : voice Enrollment')
            st.info("enroll for voice only attendence")

            audio_data=None

            try:
                audio_data=st.audio_input("Record a short voice sample (5-10 seconds)")
            except Exception as e:
                st.error(f"Error accessing audio input: {e}")

            if st.button("create Acount",type="primary"):
                if new_name:
                    with st.spinner("Creating your account..."):
                        img=np.array(Image.open(photo_source))
                        encoding=get_face_embedding(img)
                        if encoding:
                            face_emb=encoding[0].tolist()

                            voice_emb=None
                            if audio_data:
                                voice_emb=get_voice_embedding(audio_data.read())
                            response_data=create_student(new_name,face_embedding=face_emb,voice_embedding=voice_emb)

                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in=True
                                st.session_state.user_role='student'
                                st.session_state.student_data=response_data[0]
                                st.toast(f"Profile created successfully, {new_name}!")
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error("Coudnt capture your facial features for registration. Please try again.")
                       



    footer_dashboard()
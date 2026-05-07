import streamlit as st
from src.ui.base_layout import  style_background_dashboard,style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import check_teacher_exists,create_teacher,teacher_login,get_teacher_subjects
from src.components.dialog_create_subject import create_subject_dialog
from src.components.subject_card import subject_card
from src.components.dialog_share_subject import share_subject_dialog
def teacher_screen():

    style_background_dashboard()
    style_base_layout()

    
    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=="login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type=='register':
        teacher_screen_register()

def teacher_dashboard():
    teacher_data=st.session_state.teacher_data
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"Welcome, {teacher_data['name']}!")

        if st.button("Logout",type="secondary",key="loginbackbtn",shortcut="control+backspace"):
            st.session_state['is_logged_in']=False
            del st.session_state.teacher_data

            st.rerun()
    st.space()

    if"current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab="take_attendance"
    tab1,tab2,tab3=st.columns(3)
    with tab1:
        type1="primary" if st.session_state.current_teacher_tab=="take_attendance" else "tertiary"
        if st.button(type=type1,width="stretch",icon=":material/ar_on_you:",label="View Attendance"):
            st.session_state.current_teacher_tab="take_attendance"
            st.rerun()
    with tab2:
        type2="primary" if st.session_state.current_teacher_tab=="manage_subjects" else "tertiary"
        if st.button(type=type2,width="stretch",icon=":material/book_ribbon:",label="Manage subjects"):
             st.session_state.current_teacher_tab="manage_subjects"
             st.rerun()
            
    with tab3:
        type3="primary" if st.session_state.current_teacher_tab=="attendance_records" else "tertiary"
        if st.button(type=type3,width="stretch",icon=":material/assignment:",label="Attendance records"):
            st.session_state.current_teacher_tab="attendance_records"
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab=="take_attendance":
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab=="manage_subjects":

        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab=="attendance_records":
        teacher_tab_attendance_records()

    footer_dashboard()

def teacher_tab_take_attendance():
    st.header("Take attendance AI for your class")

def teacher_tab_manage_subjects():
    teacher_id=st.session_state.teacher_data['teacher_id']
    col1,col2=st.columns(2)
    with col1:
        st.header("Manage subjects",width="stretch")
    with col2:
        if st.button("Add new subject",icon=":material/add:",width="stretch"):
            create_subject_dialog(teacher_id) 


    #list of subjects
    subjects=get_teacher_subjects(teacher_id)
    if subjects:
     for sub in subjects:
        stats = [
            ("", "Students", sub.get('total_students', 0)),
            ("", "Classes", sub.get('total_classes', 0)),
        ]

        def share_btn(sub=sub):
            if st.button(
                f"Share Code: {sub['name']}",
                key=f"share_{sub['subject_code']}",
                icon=":material/share:"
            ):
                share_subject_dialog(sub['name'], sub['subject_code'])

        subject_card(
            name=sub['name'],
            code=sub['subject_code'],
            section=sub['section'],
            stats=stats,
            footer_callback=share_btn
        )
    else:
        st.warning('no subjects found. Please create a subject to start taking attendance')

def teacher_tab_attendance_records():
    st.header("View and export attendance records")

def login_teacher(teacher_username, teacher_password):
    if not teacher_username or not teacher_password:
        return False
    teacher = teacher_login(teacher_username, teacher_password)
    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    return False

def teacher_screen_login():
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to home",type="secondary",key="loginbackbtn",shortcut="control+backspace"):
            st.session_state['login_type']=None
            st.rerun()

    st.header("Login using password",text_alignment="center")
    st.space()
    st.space()
    teacher_username=st.text_input("enter name",placeholder="ananyaroy")
    teacher_password=st.text_input("enter password",type="password",placeholder="enter password")
    
    st.divider()
    btnc1,btnc2=st.columns(2)

    with btnc1:
        if st.button("login",icon=":material/passkey:",shortcut="control+enter",width="stretch"):
            if login_teacher(teacher_username, teacher_password):
                st.toast("Login successful!",icon="✅")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username or password")
    with btnc2:
        if st.button("Register",type="primary",icon=":material/passkey:",width="stretch"):
            st.session_state.teacher_login_type='register'
    footer_dashboard()


def register_teacher(teacher_username,teacher_name,teacher_password,teacher_password_confirm):
    if not teacher_username or not teacher_name or not teacher_password :
        return False,"All fields are required"
    if check_teacher_exists(teacher_username):
        return False,"Teacher with this username already exists"
    if teacher_password != teacher_password_confirm:
        return False,"Passwords do not match"
    try:
        create_teacher(teacher_username,teacher_name,teacher_password)
        return True,"Teacher registered successfully! Please login now."
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"
    

def teacher_screen_register():
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to home",type="secondary",key="loginbackbtn",shortcut="control+backspace"):
            st.session_state['login_type']=None
            st.rerun()

    st.header("Register your teacher profile")
    st.space()
    st.space()

    teacher_username=st.text_input("enter username",placeholder="ananyaroy")
    teacher_name=st.text_input("enter name",placeholder="Abhishek Shinde")

    teacher_password=st.text_input("enter password",type="password",placeholder="enter password")
    teacher_password_confirm=st.text_input("confirm your password",type="password",placeholder="enter password")

    st.divider()
    btnc1,btnc2=st.columns(2)

    with btnc1:
        if st.button("Register",icon=":material/passkey:",shortcut="control+enter",width="stretch"):
            success,message=register_teacher(teacher_username,teacher_name,teacher_password,teacher_password_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type="login"
                st.rerun()
            else:
                st.error(message)
    with btnc2:
        if st.button("Login",type="primary",icon=":material/passkey:",width="stretch"):
            st.session_state.teacher_login_type="login"
    footer_dashboard()
    
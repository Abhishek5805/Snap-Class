import streamlit as st
from src.ui.base_layout import  style_background_dashboard,style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
def teacher_screen():

    style_background_dashboard()
    style_base_layout()

    

    if 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=="login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type=='register':
        teacher_screen_register()

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
        st.button("login",icon=":material/passkey:",shortcut="control+enter",width="stretch")
    with btnc2:
        if st.button("Register",type="primary",icon=":material/passkey:",width="stretch"):
            st.session_state.teacher_login_type='register'
    footer_dashboard()

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
        st.button("Register",icon=":material/passkey:",shortcut="control+enter",width="stretch")
    with btnc2:
        if st.button("Login",type="primary",icon=":material/passkey:",width="stretch"):
            st.session_state.teacher_login_type="login"
    footer_dashboard()
    
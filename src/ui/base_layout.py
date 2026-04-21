import streamlit as st

def style_background_home():
    st.markdown(
        """
         <style>

                .stApp {
                    background: #5865F2 !important;
                }

                .stApp div[data-testid="stColumn"]{
                    background-color:#E0E3FF !important;
                    padding:2.5rem !important;
                    border-radius: 5rem !important;
                    }
        </style>  
        """,
        unsafe_allow_html=True
    )


def style_background_dashboard():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #E0E3FF !important;
            font-family: 'Arial', sans-serif;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def style_base_layout():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&family=Plus+Jakarta+Sans:ital,wght@0,200..800;1,200..800&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&family=Outfit:wght@100..900&family=Plus+Jakarta+Sans:ital,wght@0,200..800;1,200..800&display=swap');
        #MainMenu, footer, header {visibility: hidden;}

        .block-container {
            padding-top: 1.5rem;
            }
        h1{
            font-family: 'Climate Crisis', sans-serif !important;
            font-size: 3.5rem !important;
            line-height: 1.2 !important;
            margin-bottom: 1rem !important;

          
        }
        h2{
            font-family: 'Climate Crisis', sans-serif !important;
            font-size: 2rem !important;
            line-height: 1.2 !important;
            margin-bottom: 1rem !important;
            }
        h3,h4,h5,h6{
            font-family: 'Outfit', sans-serif;
            font-weight: 600 !important;
        }
        BUTTON[kind="primary"] {
            border-radius: 1.5rem !important;
            background:#5865F2 !important;
            color: white !important;
            border: none !important;
            padding: 10px 20px !important;
            transition:transform 0.25s ease-in-out !important;
        }
        BUTTON[kind="secondary"] {
            border-radius: 1.5rem !important;
            background:#EB459E !important;
            color: white !important;
            border: none !important;
            padding: 10px 20px !important;
            transition:transform 0.25s ease-in-out !important;
        }
        BUTTON[kind="tertiary"] {
            border-radius: 1.5rem !important;
            background:black !important;
            color: white !important;
            border: none !important;
            padding: 10px 20px !important;
            transition:transform 0.25s ease-in-out !important;
        }
        button:hover {
            transform: scale(1.05) !important;  
        }
        </style>
        """,
        unsafe_allow_html=True
    )
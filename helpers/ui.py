import streamlit as st

def remove_top_padding():
    st.markdown("""
    <style>
        /* Reduce top margin and padding */
        .block-container {
            padding-top: 1rem !important;
        }
    </style>
    """, unsafe_allow_html=True)
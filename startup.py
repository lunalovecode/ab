import streamlit as st

st.set_page_config(
    page_title="Log in or create an account to see Adventure Board"
)

from db import get_connection
import sqlite3
from time import sleep

if "current_user" not in st.session_state:
    st.session_state.current_user = None

with st.container(border=True):
    col1, col2, col3 = st.columns([0.2, 0.6, 0.2])
    with col2:
        login_button = st.button("Login", type="primary", use_container_width=True)
        st.button("or", type="tertiary", use_container_width=True)
        create_account_button = st.button("Create an account", use_container_width=True)
        st.button("to access Adventure Board", type="tertiary", use_container_width=True)

    if login_button:
        st.switch_page("pages/login.py")
    
    if create_account_button:
        st.switch_page("pages/create-account.py")

with get_connection() as conn:
    cursor = conn.cursor()
    accounts_exist = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Accounts';").fetchone()
    if not accounts_exist:
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Accounts (
                    name TEXT NOT NULL,
                    username TEXT NOT NULL UNIQUE,
                    profile_pic BLOB UNIQUE,
                    password BLOB);''')
        conn.commit()
    
    posts_exist = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Posts';").fetchone()
    if not posts_exist:
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    start_date TEXT NOT NULL,
                    end_date TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT NOT NULL,
                    location_name TEXT NOT NULL,
                    location_link TEXT NOT NULL,
                    details TEXT NOT NULL,
                    creator TEXT NOT NULL
                    );
                    ''')
        conn.commit()
    
    signups_exists = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Signups';").fetchone()
    if not signups_exists:
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Signups (
                    user_id TEXT,
                    post_id INTEGER,
                    status TEXT CHECK(status IN ('pending', 'approved', 'rejected')) DEFAULT 'pending',
                    PRIMARY KEY (user_id, post_id),
                    FOREIGN KEY (user_id) REFERENCES Accounts(username),
                    FOREIGN KEY (post_id) REFERENCES POSTS(id)
                    );
                    ''')
        conn.commit()

st.write("or")
login_google = st.button("Login with Google", on_click=st.login)

if login_google:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO Accounts (name, username) VALUES (?, ?)", (st.user.name, st.user.email))
        conn.commit()
        st.login

if st.user.is_logged_in:
    st.session_state.current_user = st.user.email
    st.switch_page("pages/home.py")

if st.session_state.current_user is not None:
    st.switch_page("pages/home.py")
@echo off
start cmd /k uvicorn src.api.main:app --reload
streamlit run frontend/app.py

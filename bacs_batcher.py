import streamlit as st
from utils.bacs_processor import BacsProcessor

st.title("Payroll File Splitter")
uploaded_file = st.file_uploader("Choose a BACS Payroll file")
st.divider()
threshold = st.number_input('Insert max sum of amounts in each output file', value=25000)
pay_ref = st.text_input('Insert payment reference for output files', value='Reference')
if uploaded_file is not None:
    bacs_processor = BacsProcessor(uploaded_file, pay_ref, threshold)
    bacs_processor.create_batches()
    bacs_processor.create_output_files()


import streamlit as st
from split_bacs import section_bacs_file, create_batches, create_output_files

st.title("Payroll File Splitter")
uploaded_file = st.file_uploader("Choose a BACS Payroll file")
st.divider()
threshold = st.number_input('Insert max sum of amounts in each output file', value=25000)
if uploaded_file is not None:
    header, footer, middle = section_bacs_file(uploaded_file)
    batches = create_batches(middle, threshold)
    create_output_files(batches, header, footer, uploaded_file.name)


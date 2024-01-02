import streamlit as st
from split_bacs import section_bacs_file, create_batches, create_output_files, change_payment_ref

st.title("Payroll File Splitter")
uploaded_file = st.file_uploader("Choose a BACS Payroll file")
st.divider()
threshold = st.number_input('Insert max sum of amounts in each output file', value=25000)
pay_ref = st.text_input('Insert payment reference for output files', value='Reference')
if uploaded_file is not None:
    header, footer, middle = section_bacs_file(uploaded_file)
    middle = change_payment_ref(pay_ref, middle)
    batches = create_batches(middle, threshold)
    create_output_files(batches, header, footer, uploaded_file.name)


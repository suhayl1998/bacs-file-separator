from io import StringIO
import streamlit as st
import pandas as pd

HEADER = 4
FOOTER = 5

# BACS File constants
AMOUNT_START = 35
AMOUNT_END = 46
REF_START = 64
REF_END = 82
PAYEE_START = 82
PAYEE_END = 100

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')

def section_bacs_file(uploaded_file):
    file = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
    full_file = file.split("\n")
    header = full_file[:HEADER]
    footer = full_file[-FOOTER:]
    middle = full_file[HEADER:-FOOTER]
    return header, footer, middle

def change_line(new_ref, line):
    new_ref_length = len(new_ref)
    pad_length = REF_END - REF_START - new_ref_length
    padded_ref = new_ref + (" " * pad_length)
    return line[:REF_START] + padded_ref + line[REF_END:]

def change_payment_ref(new_ref, payment_lines):
    if len(new_ref) >= REF_END - REF_START:
        st.write("Please ensure your reference is under 18 characters.")
        return payment_lines
    else:
        st.write(f"Payment reference changed to '{new_ref}'.")
        return [change_line(new_ref, line) for line in payment_lines]

# amounts = {line[82:100].strip():float(line[35:46])/100 for line in middle}
def create_batches(middle, threshold):
    batches = []
    batch = []
    batch_details = []
    batch_sum = 0
    for line in middle:
        amount = float(line[AMOUNT_START:AMOUNT_END])/100
        reference = line[REF_START:REF_END].strip()
        payee = line[PAYEE_START:PAYEE_END].strip()
        details_dict = {
            "Employee Name": payee,
            "Net Pay": round(amount, 2),
            "Reference": reference
        }
        if batch_sum + amount < threshold:
            batch.append(line)
            batch_details.append(details_dict)
            batch_sum += amount
        else:
            batches.append((batch, batch_details, batch_sum))
            batch = [line]
            batch_details = [details_dict]
            batch_sum = amount
    batches.append((batch, batch_details, batch_sum))
    return batches

def create_output_files(batches, header, footer, initial_file, pay_ref):
    for i, (batch, batch_details, batch_sum) in enumerate(batches):
        file_name = f"{initial_file.split('.')[0]} - Batch {i+1}.txt"
        csv_file_name = f"{pay_ref}-Batch {i+1}-{round(batch_sum, 2)}.csv"
        df = pd.DataFrame(batch_details)
        full_batch = header + batch + footer
        with st.container(border = True):
            col1, col2 = st.columns(2)
            with col1:
                st.write(file_name)
                st.download_button("Download File",'\n'.join(str(i) for i in full_batch), file_name)
            with col2:
                st.write(f"£{round(batch_sum, 2)}")
                csv = convert_df(df)
                st.download_button(
                    label="Download payment batch as CSV",
                    data=csv,
                    file_name=csv_file_name,
                    mime='text/csv',
                    )







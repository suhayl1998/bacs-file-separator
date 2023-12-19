from io import StringIO
from zipfile import ZipFile
import streamlit as st

HEADER = 4
FOOTER = 5

def section_bacs_file(uploaded_file):
    file = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
    full_file = file.split("\n")
    header = full_file[:HEADER]
    footer = full_file[-FOOTER:]
    middle = full_file[HEADER:-FOOTER]
    return header, footer, middle


# amounts = {line[82:100].strip():float(line[35:46])/100 for line in middle}
def create_batches(middle, threshold):
    batches = []
    batch = []
    batch_sum = 0
    for line in middle:
        amount = float(line[35:46])/100
        if batch_sum + amount < threshold:
            batch.append(line)
            batch_sum += amount
        else:
            batches.append(batch)
            batch = [line]
            batch_sum = amount
    batches.append(batch)
    return batches

def create_output_files(batches, header, footer, initial_file):
    for i, batch in enumerate(batches):
        file_name = f"{initial_file.split('.')[0]} - Batch {i+1}.txt"
        full_batch = header + batch + footer
        with st.container(border = True):
            st.write(file_name)
            st.download_button("Download File",'\n'.join(str(i) for i in full_batch), file_name)







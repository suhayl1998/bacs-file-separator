import utils.constants as constants
from io import StringIO
import streamlit as st
import pandas as pd

class BacsProcessor:
    def __init__(self, uploaded_file, pay_ref, threshold):
        file = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
        self.filename = uploaded_file.name
        self.full_file = file.split("\n")
        self.header = self.full_file[:constants.HEADER]
        self.footer = self.full_file[:constants.FOOTER:]
        self.middle = self.full_file[constants.HEADER:-constants.FOOTER]
        self.pay_ref = pay_ref
        self.threshold = threshold
        self.change_payment_ref()
        self.batches = []
    
    def change_line(self, new_ref, line):
        new_ref_length = len(new_ref)
        pad_length = constants.REF_END - constants.REF_START - new_ref_length
        padded_ref = new_ref + (" " * pad_length)
        return line[:constants.REF_START] + padded_ref + line[constants.REF_END:]
    
    def change_payment_ref(self):
        if len(self.pay_ref) >= constants.REF_END - constants.REF_START:
            st.write("Please ensure your reference is under 18 characters.")
        else:
            st.write(f"Payment reference changed to '{self.pay_ref}'.")
            self.middle = [self.change_line(self.pay_ref, line) for line in self.middle]
    
    @st.cache_data
    def convert_df(_self, df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv(index=False).encode('utf-8')
    
    def create_batches(self):
        batches = []
        batch = []
        batch_details = []
        batch_sum = 0
        for line in self.middle:
            amount = float(line[constants.AMOUNT_START:constants.AMOUNT_END])/100
            reference = line[constants.REF_START:constants.REF_END].strip()
            payee = line[constants.PAYEE_START:constants.PAYEE_END].strip()
            details_dict = {
                "Employee Name": payee,
                "Net Pay": round(amount, 2),
                "Reference": reference
            }
            if batch_sum + amount < self.threshold:
                batch.append(line)
                batch_details.append(details_dict)
                batch_sum += amount
            else:
                batches.append((batch, batch_details, batch_sum))
                batch = [line]
                batch_details = [details_dict]
                batch_sum = amount
        batches.append((batch, batch_details, batch_sum))
        self.batches = batches
    
    def create_output_files(self):
        for i, (batch, batch_details, batch_sum) in enumerate(self.batches):
            file_name = f"{self.filename.split('.')[0]} - Batch {i+1}.txt"
            csv_file_name = f"{self.pay_ref}-Batch {i+1}-{round(batch_sum, 2)}.csv"
            df = pd.DataFrame(batch_details)
            full_batch = self.header + batch + self.footer
            with st.container(border = True):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(file_name)
                    st.download_button("Download File",'\n'.join(str(i) for i in full_batch), file_name)
                with col2:
                    st.write(f"£{round(batch_sum, 2)}")
                    csv = self.convert_df(df)
                    st.download_button(
                        label="Download payment batch as CSV",
                        data=csv,
                        file_name=csv_file_name,
                        mime='text/csv',
                        )














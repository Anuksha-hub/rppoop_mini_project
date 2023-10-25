import streamlit as st
import pandas as pd
import tempfile
import io
import re
# Function to upload a CSV file
# adding 1 comment
#adding 2 comment
def upload_csv():
    st.sidebar.markdown("### Upload CSV File")
    uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("CSV file uploaded successfully!")
            return df
        except Exception as e:
            st.error(f"Error uploading CSV file: {str(e)}")
    return None
# Function to filter the data based on the search criteria
def filter_data(df):
    search_criteria = st.text_input("Enter search criteria:")
    filter_button = st.button("Filter 📊")
    if filter_button:
        filters = [c.strip() for c in search_criteria.split(',')]

        filtered_df = df.copy()
        for f in filters:
            if f in df['Category'].values:
                filtered_df = filtered_df.loc[filtered_df['Category'] == f]
            elif "Div" in f:
                filtered_df = filtered_df.loc[filtered_df['Division'] == f]
            elif f == 'M' or f == 'F':
                filtered_df = filtered_df.loc[filtered_df['Gender'] == f]
            else:
                operator_match = re.match(r"([<>])?(\d+\.?\d*)", f)
                if operator_match:
                    operator = operator_match.group(1)
                    value = float(operator_match.group(2))

                    if operator == '>':
                        filtered_df = filtered_df.loc[filtered_df['Cgpa'] > value]
                    elif operator == '<':
                        filtered_df = filtered_df.loc[filtered_df['Cgpa'] < value]
                    else:
                        filtered_df = filtered_df.loc[filtered_df['Cgpa'] == value]
                else:
                    # Filter based on first word of Course name
                    first_word = f.split()[0]
                    filtered_df = filtered_df.loc[df['Course'].str.contains(first_word, na=False, case=False)]
        if len(filtered_df) == 0:
            st.info("No matching records found.")
        else:
            display_data(filtered_df)
    
            # Save filtered data
            save_data(filtered_df)

# Function to display the filtered data
def display_data(filtered_df):
    st.dataframe(filtered_df)

    # Show count
    st.markdown("Total Entries: {}".format(len(filtered_df)))

# Function to save the filtered data as an Excel file
def save_data(filtered_df):
    excel_file = io.BytesIO()
    with pd.ExcelWriter(excel_file, engine="xlsxwriter") as writer:
        filtered_df.to_excel(writer, index=False, sheet_name="Filtered Data")
        writer.save()

    excel_file.seek(0)
    st.download_button("Download Excel 📥", data=excel_file, file_name="filtered_data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")



# Main program
st.title("Student Data Filter")
st.markdown("""<style>.stTextInput label { font-size: 16px; margin-bottom: 6px; }</style>""", unsafe_allow_html=True)
st.text("This is multilevel filtering of data")
st.markdown("To get a single criteria, simply enter it")
st.markdown("To get more than one filter, separate your criteria using ' , '")
st.markdown("For CGPA:")
st.markdown("- If you want a particular CGPA, enter that value.")
st.markdown("- If you want CGPA greater than the value, use '>' symbol before your value.")
st.markdown("- If you want CGPA less than the value, use '<' symbol before your value.")

# Upload CSV file
df = upload_csv()

if df is not None:
    # Filter data
    filter_data(df)

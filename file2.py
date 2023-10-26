import streamlit as st
import pandas as pd
from PIL import Image
import tempfile
import io
import re
import base64
# Function to filter the data based on the search criteria
def filter_data():
    search_criteria = st.text_input("Enter search criteria:")
    filter_button = st.button("Filter 📊")
    if filter_button:
        filters = [c.strip() for c in search_criteria.split(',')]

        filtered_df = df.copy()
        for f in filters:
            if ";" in f:
                entries = [e.strip() for e in f.split(';')]
                temp_df = pd.DataFrame()
                for entry in entries:
                    if entry in df['Category'].values:
                        temp_df = temp_df.append(filtered_df.loc[filtered_df['Category'] == entry])
                    elif entry in df['Course'].values:
                        temp_df = temp_df.append(filtered_df.loc[filtered_df['Course'] == entry])
                    elif entry in df['Division'].values:
                        temp_df = temp_df.append(filtered_df.loc[filtered_df['Division'] == entry])
                filtered_df = temp_df.drop_duplicates()
            elif f in df['Category'].values:
                filtered_df = filtered_df.loc[filtered_df['Category'] == f]
            elif "Div" in f:
                filtered_df = filtered_df.loc[filtered_df['Division'] == f]
            elif f == 'M' or f == 'F':
                filtered_df = filtered_df.loc[filtered_df['Gender'] == f]
            elif f in df['Course'].values:
                filtered_df = filtered_df.loc[filtered_df['Course'] == f]
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

    # Show total count
    st.markdown("Total Entries: {}".format(len(filtered_df)))

# Function to save the filtered data as an Excel file
def save_data(filtered_df):
    excel_file = io.BytesIO()
    with pd.ExcelWriter(excel_file, engine="xlsxwriter") as writer:
        filtered_df.to_excel(writer, index=False, sheet_name="Filtered Data")
        writer.save()
    
    excel_file.seek(0)
    st.download_button("Download Excel 📥", data=excel_file, file_name="filtered_data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# Load the student data from a CSV file
df = pd.read_csv('FYList.csv')

# Load and display an image
image = Image.open("C:\\Users\\Sanjogta Koul\\Desktop\\RRPOOP\\filtericon.png")
st.image(image, width=100)

st.title("Student Data Filtering")
st.markdown("""<style>.stTextInput label { font-size: 16px; margin-bottom: 6px; }</style>""", unsafe_allow_html=True)
st.text("This is multilevel filtering of data")
st.text("Get all COEP student data simplified and without having to search through huge data!")
st.markdown("To get a single criteria, simply enter it")
st.markdown("To get multiple filters for different columns, separate your criteria using ' , '")
st.markdown("To get multiple filters within the same column, separate your criteria using ' ; '")
st.divider()
st.markdown("For CGPA:")
st.markdown("- If you want a particular CGPA, enter that value.")
st.markdown("- If you want CGPA greater than the value, use '>' symbol before your value.")
st.markdown("- If you want CGPA less than the value, use '<' symbol before your value.")
st.divider()
st.markdown("Criteria- Course, Category, Division, Cgpa")
gif=Image.open("C:\\Users\\Sanjogta Koul\\Desktop\\RRPOOP\\stats.gif")
st.image(gif, width=90)

#Filter data
# Filter data
filter_data()

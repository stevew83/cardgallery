import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the default CSV file
default_csv_path = "sportscards.csv"
default_df = pd.read_csv(default_csv_path)

# Function to extract the last name from the "Name" column
def extract_last_name(name):
    parts = name.split()
    if len(parts) > 1:
        return parts[-1].lower()
    else:
        return parts[0][0].lower()  # Use the first letter of the first name if no space

# Function to create a blank CSV with the same columns
def create_blank_csv():
    columns = default_df.columns
    blank_df = pd.DataFrame(columns=columns)
    return blank_df

# Add HTML for title and CSS for layout
st.markdown("""
    <h1 style="text-align: center; color: #333;">Online Toploader Binder</h1>
    <br>
    <p>This site was created as a way to organize and display trading cards. You can search for particular players, sets, and years.
     Charts below will change dynamically based on the filters.
     In the sidebar, you may also upload a CSV (comma separated value - *.csv) file to display and organize your own cards.</p>
                            

   <style>
         
       .flip-card {
    background-color: transparent;
    width: 200px; /* Adjusted width */
    height: 300px; /* Adjusted height */
    perspective: 1000px;
    margin: 10px;
    display: inline-block;
}
.flip-card-inner {
    position: relative;
    width: 100%;
    height: 100%;
    text-align: center;
    transition: transform 0.8s;
    transform-style: preserve-3d;
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
}
.flip-card:hover .flip-card-inner {
    transform: rotateY(180deg);
}
.flip-card-front, .flip-card-back {
    position: absolute;
    width: 100%;
    height: 100%;
    -webkit-backface-visibility: hidden;
    backface-visibility: hidden;
}
.flip-card-front img, .flip-card-back img {
    width: 100%;
    height: 100%;
    object-fit: cover; /* Fill the container while maintaining the aspect ratio */
}
.flip-card-front {
    background-color: transparent;
}
.flip-card-back {
    background-color: transparent;
    transform: rotateY(180deg);
}
    
    .chart-container {
        display: flex;
        justify-content: space-between;
        margin-bottom: 20px;
    }
    .card-gallery {
        border: 2px solid #333;
        border-radius: 10px;
        padding: 10px;
        background-color: #f9f9f9;
        margin: 0 auto;
        width: fit-content;
    }
</style>
""", unsafe_allow_html=True)


# Download blank CSV section
with st.sidebar:
    st.markdown("### Download Blank CSV Template")
    st.markdown("Populate the template using Excel, Google Sheets, or VS Code:")
    blank_df = create_blank_csv()
    csv_data = blank_df.to_csv(index=False)
    st.download_button(label="Download Blank CSV", data=csv_data, file_name='blank_template.csv', mime='text/csv')

# User Guide for Populating CSV
with st.sidebar:
    with st.expander("How to Populate the CSV Correctly"):
        st.markdown("""
        Follow these tips to ensure the CSV is populated correctly:

        1. **Complete Each Column**: Each row should have data in every column to avoid errors.
        
        2. **Card Representation**: Each card in the app corresponds to a row in the CSV.
        
        3. **Sample Row Format**:
        ```
        Year,Category,Set,Name,Condition,Approx Value,Front Image,Back Image,Notes
        1974,Hockey,Topps,Bobby Orr,EX,15,"https://res.cloudinary.com/image/orr74.jpg","https://res.cloudinary.com/image/orr74back.jpg",Norris Winner.
        ```
        4. **Field-Specific Instructions**:
           - **Year**: Four digits (e.g., 1997 for 1997-98).
           - **Category**: Sport name (e.g., hockey, football).
           - **Set**: Set name (be consistent).
           - **Name**: Full name (first and last).
           - **Condition**: Use one of these: PR, GD, VG, VG-EX, EX, EX-MT, NM, NM-MT, MT, GEM MT.
           - **Approx Value**: Numeric (e.g., 50), no dollar sign.
           - **Front/Back Image**: URL in quotes (e.g., "https://example.com/image.jpg").
           - **Notes**: Any additional information.
        
        5. **Image Hosting**: Use a service like Cloudinary.com for hosting images.
        
        After filling the CSV, upload it to the app to display your collection. Enjoy!
        """)


# Move the File Upload to the sidebar
with st.sidebar:
    # Upload CSV section
    st.markdown("### Upload your own CSV to display your collection:")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    st.markdown("""
        <p style="font-size: 12px; color: #555;">Privacy Note: This tool is designed for personal use only. Any data you upload is private and remains accessible only to you during your session. If you wish to share your data, consider recording a screencast or setting up your own website.</p>
    """, unsafe_allow_html=True)

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        df = default_df.copy()



# Create columns with buffer space on the sides
col1, col2, col3 = st.columns([3, 2, 2])

with col1:
    search_query = st.text_input("Search", "")  # Shortened label

with col2:
    selected_category = st.selectbox("Category", options=["All"] + sorted(df['Category'].unique()))  # Shortened label

with col3:
    sort_option = st.selectbox(
        "Sort",
        options=[
            "Value (High-Low)",
            "Value (Low-High)",
            "Year (New-Old)",
            "Year (Old-New)",
            "Name (A-Z)",
            "Name (Z-A)"
        ]  # Shortened options
    )

# Filter the DataFrame based on the selected category and search query
filtered_df = df.copy()
if selected_category != "All":
    filtered_df = filtered_df[filtered_df['Category'] == selected_category]

if search_query:
    filtered_df = filtered_df[
        filtered_df['Name'].str.contains(search_query, case=False, na=False) |
        filtered_df['Year'].astype(str).str.contains(search_query, case=False, na=False) |
        filtered_df['Set'].str.contains(search_query, case=False, na=False)
    ]

# Sort the DataFrame based on the selected sort option
if sort_option == "Value (High-Low)":
    filtered_df = filtered_df.sort_values(by='Approx Value', ascending=False)
elif sort_option == "Value (Low-High)":
    filtered_df = filtered_df.sort_values(by='Approx Value', ascending=True)
elif sort_option == "Year (New-Old)":
    filtered_df = filtered_df.sort_values(by='Year', ascending=False)
elif sort_option == "Year (Old-New)":
    filtered_df = filtered_df.sort_values(by='Year', ascending=True)
elif sort_option == "Name (A-Z)":
    filtered_df['Last Name'] = filtered_df['Name'].apply(extract_last_name)
    filtered_df = filtered_df.sort_values(by='Last Name', ascending=True)
elif sort_option == "Name (Z-A)":
    filtered_df['Last Name'] = filtered_df['Name'].apply(extract_last_name)
    filtered_df = filtered_df.sort_values(by='Last Name', ascending=False)

# Display summary statistics
total_cards = len(filtered_df)
highest_value_card = filtered_df.loc[filtered_df['Approx Value'].idxmax()] if total_cards > 0 else None
average_value = filtered_df['Approx Value'].mean()

# Create a markdown formatted string
summary_text = f"""
**Summary Statistics**

- **Total Cards:** {total_cards}
- **Highest Value Card:** {f"{highest_value_card['Year']} {highest_value_card['Set']} - {highest_value_card['Name']} (${highest_value_card['Approx Value']})" if highest_value_card is not None else "N/A"}
- **Average Value:** {f"${average_value:.2f}" if total_cards > 0 else "N/A"}
"""

# Display the markdown text
st.markdown(summary_text)

# Create charts
col1, col2 = st.columns(2)
with col1:
    set_counts = filtered_df['Set'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 8))
    pastel_colors = sns.color_palette("pastel", len(set_counts))
    ax.pie(set_counts, labels=set_counts.index, autopct='%1.1f%%', startangle=140, colors=pastel_colors)
    ax.set_title('Distribution of Cards by Set Name')
    st.pyplot(fig)
with col2:
    condition_order = ['PR', 'GD', 'VG', 'VG-EX', 'EX', 'EX-MT', 'NM', 'NM-MT', 'MT', 'GEM MT']
    condition_counts = filtered_df['Condition'].value_counts().reindex(condition_order, fill_value=0)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.bar(condition_order, condition_counts, color=sns.color_palette("pastel"))
    ax.set_title('Distribution of Card Conditions')
    ax.set_xlabel('Condition')
    ax.set_ylabel('Number of Cards')
    st.pyplot(fig)



st.markdown("<h2 style='text-align: center;'>Card Gallery</h2>", unsafe_allow_html=True)

# Pagination and card gallery
items_per_page = 9
total_items = len(filtered_df)
total_pages = (total_items + items_per_page - 1) // items_per_page

if total_pages > 1:
    page_number = st.slider('Page', 1, total_pages, 1)
    start_index = (page_number - 1) * items_per_page
    end_index = start_index + items_per_page
else:
    start_index = 0
    end_index = total_items

current_page_df = filtered_df.iloc[start_index:end_index]

for i in range((len(current_page_df) + 2) // 3):
    cols = st.columns(3)
    for j, col in enumerate(cols):
        index = i * 3 + j
        if index < len(current_page_df):
            row = current_page_df.iloc[index]
            front_image = row.get('Front Image', '')
            back_image = row.get('Back Image', '')
            if front_image and back_image:
                with col:
                    st.markdown(f"""
                        <div class="flip-card">
                            <div class="flip-card-inner">
                                <div class="flip-card-front">
                                    <img src="{front_image}" alt="Card Front">
                                </div>
                                <div class="flip-card-back">
                                    <img src="{back_image}" alt="Card Back">
                                </div>
                            </div>
                        </div>
                        <p>{row['Year']} {row['Set']} - <b>{row['Name']}</b> - {row['Condition']} - ${row['Approx Value']}</p>
                        <p>{row['Notes']}</p>
                    """, unsafe_allow_html=True)

# Simple HTML footer with contact and YouTube link
st.markdown("""
<p style='text-align: center; margin-top: 50px;'>
    Contact: <a href="mailto:stevew83@gmail.com">stevew83@gmail.com</a><br>
    <a href="https://www.youtube.com/@Countersparkcards" target="_blank">
        <img src="https://upload.wikimedia.org/wikipedia/commons/4/42/YouTube_icon_%282013-2017%29.png" alt="YouTube" style="width:40px;height:40px;">
    </a>
</p>
""", unsafe_allow_html=True)

import streamlit as st
# from PIL import Image


st.set_page_config(page_title="Introduction", page_icon=":bar_chart:", layout="wide")

st.title("Hackathon - Data Visualization")

# st.header("Logo Example")
# logo_image = Image.open('uni_logo.png')
# st.image(logo_image , caption="Your Logo Caption", use_column_width=True)

# Introduction Section
st.header("Introduction")
st.write("""
         In the CANIS Data Visualization and Foreign Interference challenge, we team are given a [dataset](https://kaggle.com/datasets/26d46af7be53af51e042cf9abc377731d0d53faec0a4cf713ffbf5dca3c364dc)
         and a task to visualize the dataset, and our goal, as a participant, 
         is to decode the dataset, uncover patterns, and ultimately transform raw data into meaningful 
         insights for a broader audience that might not be immediately apparent.
              
""")

st.header("Collaborators")
st.markdown("- Sina Ziaee - Computer Science, MSc - University of Calgary\n") 
st.markdown("- Sajad Dadgar - Computer Science, MSc - University of Calgary") 

# Methodology Section
st.header("Methodology")

st.write("""
         Our methodology for visualizing the "Foreign Affairs" dataset revolves around a comprehensive approach
         including preprocessing and data extraction. Our goal is not just to depict the data but to unravel
         its potential applications, demonstrating a robust understanding of the dataset. 
         The methodology comprises the following steps:    
""")

st.subheader("1. Data Preprocessing:")
st.write("""
Before visualizing the "Foreign Affairs" dataset, our initial step was to preprocess and refine the data to enhance data quality. First, We dropped the "Name (Chinese)" and "Entity owner (Chinese)" columns, as redundant information, since we have corresponding English names and Entity owners. Additionally, due to the varied nature of the "Region of Focus" column, containing cities, countries, and continents, we assigned each region to its corresponding countries in order to facilitate representing the data on the world map.
         
         \n Furthermore, to have up-to-date information about the number of followers of each name on the dataset and have more accurate data, we leveraged social media APIs to extract the most recent follower counts. As a result, the number of followers has been updated to reflect the most recent data. The data was collected on November 16, 2023.

""")

st.subheader("2. Visualization Approach:")
st.write("""
Our approach consists of two steps. First, we focused on the dataset itself, extracting valuable information by visualizing the preprocessed dataset. But we don't stop there. We dived into social media platforms for each name in the dataset to extract more data regarding their follower, following, locations, type of accounts, whether their account is verified or not, etc. As shown in the data visualization part, additional data helped us to obtain valuable information to show the scale of China's influence on social media.
""")

st.subheader("3. Technologies")
st.write("""In our data visualization, we employed the following tools and technologies:""")
st.markdown("- Python:\n Python is a versatile programming language widely used in data science and visualization. For the implementaion, we used version 3.12.0, which is the latest stable releases.") 
st.markdown("- Streamlit:\n Streamlit is a user-friendly Python library for creating interactive web applications for data visualization. Also, it contains various features, allowing us to design engaging and dynamic visualizations seamlessly. we used version 1.28.2 for this project.") 
st.markdown("- Jupyter notebook:\n Jupyter Notebook is an open-source tool that facilitates interactive computing and data analysis.") 


# Codes
st.header("Implementaion Codes")

st.write("""All the source codes can be found on GitHub. This repository consists of all codes associated with this project, such as preprocessing and data extraction codes along with the obtained datasets. For a better understanding of the repository and its content, we explain each file and folder:""")


st.subheader("Folders & Files")
sample_list = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
st.write("Sample List:")
st.write(sample_list)

st.subheader("Setup")

st.write("""
```
pip install streamlit
```

Once installed, you can run this app locally by executing the following command in your terminal:
```
streamlit run app.py
```

Replace `app.py` with the name of your Python script.
""")
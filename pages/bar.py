import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import visualizer_func
from utils import util_functions 
import json
import pandas as pd

df, twi_df = util_functions.get_processed_merged_data()

st.set_page_config(page_title="Bar Charts", page_icon=":bar_chart:", layout="wide")

with open('findings/country_corps.json', 'r') as file:
    country_info_dict = json.load(file)

st.header("List of News Account and their owners based on the selected focus country")
selected_country_name = st.selectbox('Select a Country', list(country_info_dict.keys()))
# Display country information in a table based on the selected country
visualizer_func.display_country_info(selected_country_name, country_info_dict)


st.header("Twitter Data Explorer")
selected_y_column = st.selectbox('Select among the twitter data features', ['followers_count', 'following_count', 'tweet_num', 'followers_following_ratio'])
# Allow user to choose the top n rows
top_n = st.slider('Select the top number of news channels', min_value=1, max_value=len(twi_df), value=5)
# Call the function to visualize the top n rows
visualizer_func.visualize_top_n_rows(twi_df, selected_y_column, top_n)





import streamlit as st
import plotly.express as px
import pandas as pd

st.title("Twitter Accounts with Location in China")

data = {
    'Data': [''],
    'All names with twitter accounts': [574],
    'Twitter accounts with location': [337],
    'Users from China': [174]
}

df = pd.DataFrame(data)
df.set_index('Data', inplace=True)
df = df[df.columns[::-1]]
custom_colors = {
    'All names with twitter accounts': '#088fbc',
    'Twitter accounts with location': '#04c0b1',
    'Users from China': '#e87551'
}
fig = px.bar(df, 
             barmode='stack',
             color_discrete_sequence=[custom_colors[col] for col in df.columns])

st.plotly_chart(fig, use_container_width=True)
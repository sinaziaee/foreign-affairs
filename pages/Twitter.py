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

st.title("Twitter Accounts with Locations in China")

data = {
    'Data': [''],
    'Twitter accounts without location': [63],
    'Twitter accounts outside of China': [337],
    'Users from China': [174]
}

df = pd.DataFrame(data)
df.set_index('Data', inplace=True)
df = df[df.columns[::-1]]
custom_colors = {
    'Twitter accounts without location': '#088fbc',
    'Twitter accounts outside of China': '#04c0b1',
    'Users from China': '#e87551'
}
fig = px.bar(df, 
            barmode='stack',
            color_discrete_sequence=[custom_colors[col] for col in df.columns])

st.plotly_chart(fig, use_container_width=True)

df, twi_df = util_functions.get_processed_merged_data()

bottom_left_column, bottom_mid, bottom_right_column = st.columns((20, 2, 20))

with bottom_left_column:
    st.header("Type of Twitter Accounts")
    temp_series = df['type'].value_counts(dropna=False)
    temp_df = pd.DataFrame({'Name': list(temp_series.index), 'Value': list(temp_series.values)})
    # find total and nan values
    temp_series, text = util_functions.find_account_category(temp_df, df)
    temp_df = pd.DataFrame({'Name': list(temp_series.index), 'Value': list(temp_series.values)})
    st.text(text)
    visualizer_func.create_pie_chart(temp_df, 'Value', 'Name', "")
    
with bottom_right_column:
    st.header("Twitter Verified Accounts")
    temp_series = df['is_blue_verified'].value_counts(dropna=False)
    temp_df = pd.DataFrame({'Name': ["Is Verified", "Is Not Verified", "N/A"], 'Value': list(temp_series.values)})
    visualizer_func.create_donut_chart(temp_df, 'Value', 'Name', "", text='Verified Accounts are the ones that are Blue Verified')
    
import numpy as np
import matplotlib.pyplot as plt
    

st.header("Number of Twitter Accounts Created over the")    

temp_series = df.sort_values('created_at')['created_at'].unique()
num_year_dict = {}
for time_stamp in temp_series:
    year = time_stamp.year
    if np.isnan(year):
        continue
    if year not in list(num_year_dict.keys()):
        num_year_dict[year] = 1
    else:
        num_year_dict[year] += 1

years = list(num_year_dict.keys())
values = list(num_year_dict.values())

plt.figure(figsize=(10, 6))
plt.plot(years, values, marker='o', linestyle='-', color='b')
# plt.title('Line Chart of Data Over Years')
plt.xlabel('Year')
plt.ylabel('Number of Accounts')
plt.grid(True)

# Display the chart using Streamlit
st.pyplot(plt)
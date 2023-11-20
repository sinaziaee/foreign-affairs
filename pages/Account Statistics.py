import streamlit as st
from utils import visualizer_func, util_functions
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Analysis", page_icon=":bar_chart:", layout="wide")

df, twi_df = util_functions.get_processed_merged_data()
corp_dict = util_functions.load_file('findings/corp_data.json')

# top_left_column, top_mid, top_right_column = st.columns((20, 1, 15))
top_left_column, top_right_column = st.columns((20, 15))

with top_left_column:
    st.header("Social Media Platform Focus")
    st.write("Ratio of No. accounts in each platform per total accounts")
    col_1, col_2, col_3, col_4, col_5 = st.columns(5)
    # col_1, col_2 = st.columns(2)
    with col_1:
        visualizer_func.plot_gauge(indicator_number=corp_dict['twitter']/corp_dict['total']*100, 
                                indicator_color="#274d4a", indicator_suffix="%", indicator_title=f"Twitter: {corp_dict['twitter']}", 
                                max_bound=3, value=util_functions.generate_visual_numbers(corp_dict['twitter_fol']))
    with col_2:
        visualizer_func.plot_gauge(indicator_number=corp_dict['youtube']/corp_dict['total']*100,
                                indicator_color="#04c0b1", indicator_suffix="%", indicator_title=f"Youtube: {corp_dict['youtube']}", 
                                max_bound=3, value=util_functions.generate_visual_numbers(corp_dict['youtube_fol']))
    with col_3:
        visualizer_func.plot_gauge(indicator_number=corp_dict['facebook']/corp_dict['total']*100,
                                indicator_color="#1b7868", indicator_suffix="%", indicator_title=f"Facebook: {corp_dict['facebook']}", 
                                max_bound=3, value=util_functions.generate_visual_numbers(corp_dict['facebook_fol']))        
    with col_4:
        visualizer_func.plot_gauge(indicator_number=corp_dict['instagram']/corp_dict['total']*100, 
                                indicator_color="#088fbc", indicator_suffix="%", indicator_title=f"Instagram: {corp_dict['instagram']}", 
                                max_bound=3, value=util_functions.generate_visual_numbers(corp_dict['instagram_fol']))        
    with col_5:
        visualizer_func.plot_gauge(indicator_number=corp_dict['tiktok']/corp_dict['total']*100, 
                                indicator_color="#04fdd1", indicator_suffix="%", indicator_title=f"Tiktok: {corp_dict['tiktok']}", 
                                max_bound=3, value=util_functions.generate_visual_numbers(corp_dict['tiktok_fol']))

with top_right_column:
    st.header("The ratio of Followers # per Accounts # in each platform")
    temp_dic = util_functions.load_file('findings\\follower_per_account_ratio.json')
    # temp_df = pd.DataFrame({"value": list(temp_dic.values()), "title": list(temp_dic.keys())})
    temp_df = pd.DataFrame(list(temp_dic.items()), columns=['Platform', 'Percentage'])
    fig = px.pie(temp_df, values='Percentage', names='Platform', color_discrete_sequence=px.colors.diverging.Geyser)
    st.plotly_chart(fig, use_container_width=True, align='left')


st.header('Popularity of each Platform based on Language')
visualizer_func.plot_filtered_language_follower_bar(df)

bottom_left_column, bottom_mid, bottom_right_column = st.columns((20, 2, 20))

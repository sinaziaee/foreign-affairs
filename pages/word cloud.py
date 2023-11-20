import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_excel('./dataset/state_media_on_social_media_platforms.xlsx')
text = ''
for i in df['Name (English)'].values:
  text += i + ' '

def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

st.title("Names Word Cloud")

generate_wordcloud(text)
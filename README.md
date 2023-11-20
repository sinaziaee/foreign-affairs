# Hackathon - Foreign Affairs Data Visualization

![Untitled](https://github.com/sinaziaee/foreign-affairs/assets/47991444/9d509efb-45f3-48a7-b6b6-6f326d14bcdc)
## Introduction

In the CANIS Data Visualization and Foreign Interference challenge, we team are given a  [dataset](https://kaggle.com/datasets/26d46af7be53af51e042cf9abc377731d0d53faec0a4cf713ffbf5dca3c364dc)  and a task to visualize the dataset, and our goal, as a participant, is to decode the dataset, uncover patterns, and ultimately transform raw data into meaningful insights for a broader audience that might not be immediately apparent. Youtube demo at [this](https://www.youtube.com/watch?v=a0qAAQyfE0o) link.

## Collaborators

* Sina Ziaee - Computer Science, MSc - University of Calgary
* Sajad Dadgar - Computer Science, MSc - University of Calgary

## Methodology

Our methodology for visualizing the "Foreign Affairs" dataset revolves around a comprehensive approach including preprocessing and data extraction. Our goal is not just to depict the data but to unravel its potential applications, demonstrating a robust understanding of the dataset. The methodology comprises the following steps:


###  1. Data Preprocessing:

Before visualizing the "Foreign Affairs" dataset, our initial step was to preprocess and refine the data to enhance data quality. First, We dropped the "Name (Chinese)" and "Entity owner (Chinese)" columns, as redundant information, since we have corresponding English names and Entity owners. Additionally, due to the varied nature of the "Region of Focus" column, containing cities, countries, and continents, we assigned each region to its corresponding countries in order to facilitate representing the data on the world map.

Furthermore, to have up-to-date information about the number of followers of each name on the dataset and have more accurate data, we leveraged social media APIs to extract the most recent follower counts in platforms that widely used by the names in the dataset. As a result, the number of followers has been updated to reflect the most recent data. The data was collected on November 18, 2023.

### 2. Visualization Approach:

Our approach consists of two steps. First, we focused on the dataset itself, extracting valuable information by visualizing the preprocessed dataset. But we don't stop there. We dived into social media platforms for each name in the dataset to extract more data regarding their follower, following, locations, type of accounts, whether their account is verified or not, etc. As shown in the data visualization part, additional data helped us to obtain valuable information to show the scale of China's influence on social media.

### 3. Technologies

In our data visualization, we employed the following tools and technologies:
* Python: Python is a versatile programming language widely used in data science and visualization. For the implementaion, we used version 3.12.0, which is the latest stable releases.
* Streamlit: Streamlit is a user-friendly Python library for creating interactive web applications for data visualization. Also, it contains various features, allowing us to design engaging and dynamic visualizations seamlessly. we used version 1.28.2 for this project.
* Jupyter notebook: Jupyter Notebook is an open-source tool that facilitates interactive computing and data analysis.

## Implementaion Codes

All the source codes can be found on  [GitHub](https://github.com/sinaziaee/foreign-affairs). This repository consists of all codes associated with this project, such as preprocessing and data extraction codes along with the obtained datasets. For a better understanding of the repository and its content, we explain important files and directories:

### Repository

Description of the repository content:

**assets**: It contains json files to assign each region to its equivalent countries to represent the data based on various metrics on the world map.
**dataset**: All datasets including the main dataset and new datasets are in this directory.
**findings**: Statistics (e.g., name, entity owners, accounts, etc.) obtained from the datasets.
**pages**: Implementaion of the charts and graphs in the projects.
**data_extraction.ipynb**: Codes to extract additional information about users via social media APIs.
**Home,py**: Description of the project (First page).
**preprocess.ipynb**: Codes to preprocess the raw data.

### Setup

Below are the steps to set up the Streamlit application using code from the GitHub repository:

**Clone the Repository:**

`git clone https://github.com/sinaziaee/foreign-affairs`

**Install Dependencies:**

`pip install -r requirements.txt`

**Once installed the dependencies, run the app locally by executing the following command in your terminal:**

`streamlit run introduction.py`

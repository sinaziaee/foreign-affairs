import json 
import pandas as pd

def find_country_name_list(recognized_countries, country, my_dictionary):
    if country not in recognized_countries:
        return my_dictionary[country]
    else:
        return [country]

def find_exact_focus_groups(df, recognized_countries, equivalent_countries_dict):
    all_list = []
    found_country_name_list = []
    for region in list(df['Region of Focus'].values):
        temp_country_list = find_country_name_list(recognized_countries, region, equivalent_countries_dict)
        all_list.append(temp_country_list)
        for country_name in temp_country_list:
            if country_name not in found_country_name_list:
                found_country_name_list.append(country_name)
    df['focus group'] = all_list
    return df, found_country_name_list  

def find_country_focus_count_dictionary(df, recognized_countries, equivalent_countries_dict):
    df, found_country_name_list = find_exact_focus_groups(df, recognized_countries, equivalent_countries_dict)
    temp_dic = dict.fromkeys(found_country_name_list, 0)
    for idx in range(len(df)):
        country_list = df['focus group'][idx]
        for country in country_list:
            temp_dic[country] += 1
    return temp_dic, df

def save_country_focus_count_dict_file(temp_dic, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(temp_dic, json_file)

def data_preprocessor(df):
    to_drop_columns = ['Name (Chinese)', 'Entity owner (Chinese)', 'Parent entity (Chinese)']
    df = df.drop(to_drop_columns, axis=1)
    return df 

def create_name_owner_parent_graph(df):
    column_list = ['Name (English)', 'Entity owner (English)', 'Parent entity (English)']

    unique_parents = df['Parent entity (English)'].unique()
    unique_owners = df['Entity owner (English)'].unique()
    unique_names = df.index
    df['Account Name'] = df.index

    edges = []
    nodes = []
    node_colors = dict()

    for owner in unique_owners:
        # owner = 'China Media Group (CMG)'
        if owner not in nodes:
            nodes.append(owner)
        to_node = owner
        node_colors[to_node] = 'blue'
        from_node = df[df['Entity owner (English)'] == owner]['Parent entity (English)'].unique()[0]
        node_colors[from_node] = 'red'
        if from_node not in nodes:
            nodes.append(from_node)
        # to nodes and from nodes are vise versa :)
        edges.append((from_node, to_node))

    for account in unique_names:
        # owner = 'China Media Group (CMG)'
        if account not in nodes:
            nodes.append(account)
        to_node = account
        node_colors[to_node] = 'green'
        from_node = df[df['Account Name'] == account]['Entity owner (English)'].unique()[0]
        # node_colors[from_node] = 'blue'
        if from_node not in nodes:
            nodes.append(from_node)
        # to nodes and from nodes are vise versa :)
        edges.append((from_node, to_node))
        
    graph_dict = {"nodes": nodes, "edges": edges, 'node_colors': node_colors}
    save_country_focus_count_dict_file(graph_dict, "findings/account_owner_parent.json")

def preprocess_twitter_data(twi_df):
    twi_df = twi_df.sort_values('followers_count', ascending=False)
    twi_df['X (Twitter) handle'] = list(twi_df.index)
    if 'user_id' in list(twi_df.columns):
        twi_df = twi_df.drop(columns=['user_id'], axis=1)
    if 'description' in list(twi_df.columns):
        twi_df = twi_df.drop(columns=['description'], axis=1)
    twi_df['followers_following_ratio'] = twi_df['followers_count'] / (twi_df['following_count'] + 1e-8)
    twi_df.head(2)
    twi_df = twi_df.drop_duplicates()
    twi_df['created_at'] = pd.to_datetime(twi_df['created_at'], format='%a %b %d %H:%M:%S +0000 %Y')
    # Save the new column in the desired format
    twi_df['formatted_created_at'] = twi_df['created_at'].dt.strftime('%Y-%m-%d')
    
    return twi_df

def create_country_to_name_owner_parent_data(df):
    country_to_accounts_dict = {}
    for country_list, name, owner, parent in df[['focus group', 'Name (English)', 'Entity owner (English)', 'Parent entity (English)']].values:
        for country in country_list:
            if country not in list(country_to_accounts_dict.keys()):
                country_to_accounts_dict[country] = {'name': [name], 'owner': [owner], 'parent': [parent]}
            else:
                temp_dic = country_to_accounts_dict[country]
                if name not in list(temp_dic['name']):
                    temp_dic['name'].append(name)
                if owner not in list(temp_dic['owner']):
                    temp_dic['owner'].append(owner)
                if parent not in list(temp_dic['parent']): 
                    temp_dic['parent'].append(parent)
                country_to_accounts_dict[country] = temp_dic

    with open('findings/country_corps.json', 'w') as file:
        file.write(json.dumps(country_to_accounts_dict))
        
def get_processed_merged_data():
    df_path = 'dataset/state_media_on_social_media_platforms.xlsx'
    twitter_dir_path = 'dataset/twitter_accounts_info.csv'
    twi_df = pd.read_csv(twitter_dir_path, index_col='username')
    # loading the dataset
    df = pd.read_excel(df_path, index_col='Name (English)')
    df = data_preprocessor(df)
    df['Name (English)'] = list(df.index)
    # Load JSON data from file
    with open('assets/recognized_countries.json', 'r') as file:
        data = json.load(file)
    recognized_countries = data

    with open('assets/equivalent_countries.json', 'r') as file:
        data = json.load(file)
    equivalent_countries_dict = data

    twi_df = preprocess_twitter_data(twi_df)
    country_focus_count_dict, df = find_country_focus_count_dictionary(df, recognized_countries, equivalent_countries_dict)
    country_to_accounts_dict = create_country_to_name_owner_parent_data(df)
    # create name_owner_parent_graph_data
    create_name_owner_parent_graph(df)
    df = pd.merge(df, twi_df, on='X (Twitter) handle', how='outer')
    return df, twi_df
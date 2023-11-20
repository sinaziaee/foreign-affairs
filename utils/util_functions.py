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
    df['focus countries'] = all_list
    return df, found_country_name_list  

def find_country_focus_count_dictionary(df, recognized_countries, equivalent_countries_dict):
    df, found_country_name_list = find_exact_focus_groups(df, recognized_countries, equivalent_countries_dict)
    temp_dic = dict.fromkeys(found_country_name_list, 0)
    for idx in range(len(df)):
        country_list = df['focus countries'][idx]
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
    for country_list, name, owner, parent in df[['focus countries', 'Name (English)', 'Entity owner (English)', 'Parent entity (English)']].values:
        for country in country_list:
            if country not in list(country_to_accounts_dict.keys()):
                country_to_accounts_dict[country] = {'name': [name], 'owner': [owner], 'parent': [parent]}
            else:
                temp_dic = country_to_accounts_dict[country]
                # if name not in list(temp_dic['name']):
                #     temp_dic['name'].append(name)
                # if owner not in list(temp_dic['owner']):
                #     temp_dic['owner'].append(owner)
                # if parent not in list(temp_dic['parent']): 
                #     temp_dic['parent'].append(parent)
                temp_dic['name'].append(name)
                temp_dic['owner'].append(owner)
                temp_dic['parent'].append(parent)
                
                country_to_accounts_dict[country] = temp_dic

    with open('findings/country_corps.json', 'w') as file:
        file.write(json.dumps(country_to_accounts_dict))
        
def get_processed_merged_data():
    df_path = 'dataset/state_media_on_social_media_platforms.xlsx'
    twitter_dir_path = 'dataset/twitter_accounts_info.csv'
    type_df_path = 'dataset/account types (twitter).csv'
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
    type_df = pd.read_csv(type_df_path)
    df = pd.merge(df, type_df, on='X (Twitter) handle', how='outer')
    return df, twi_df

def find_account_category(temp_df, df):
    nan_rows = temp_df[temp_df['Name'].isna()]
    null_count = nan_rows['Value'].values[0]
    total_count = len(df)
    temp_series = df['type'].value_counts()
    text = f'{100*(null_count/total_count):.2f}% of account are not Business accounts, among the business accounts these are the categories of each account'
    return temp_series, text

def save_file(path, data):
    with open(path, 'w') as file:
        json.dump(data, file)
        
def load_file(path):
    with open(path, 'r') as file:
        data = json.load(file)
    return data

def generate_corps_data(df):
    len(df['Name (English)'].unique())
    len(df['Entity owner (English)'].unique())
    len(df['Parent entity (English)'].unique())
    corp_dict = {"name": len(df['Name (English)'].unique()),
                "owner": len(df['Entity owner (English)'].unique()),
                "parent": len(df['Parent entity (English)'].unique()),
                "twitter": len(df['X (Twitter) handle'].unique()),
                "twitter_fol": int(df['followers_count'].sum()),
                "tiktok": len(df['TikTok account'].unique()),
                "tiktok_fol": int(df['TikTok Subscriber #'].sum()),
                "instagram": len(df['Instragram page'].unique()),
                "instagram_fol": int(df['Instagram Follower #'].sum()),
                "youtube": len(df['YouTube account'].unique()),
                "youtube_fol": int(df['YouTube Subscriber #'].sum()),
                "facebook": len(df['Facebook page'].unique()),
                "facebook_fol": int(df['Facebook Follower #'].sum()),
                "total": len(df)
                }
    save_file('findings/corp_data.json', corp_dict)
    
def generate_visual_numbers(num):
    if int(num /1000000000) > 0:
        bil = num /1000000000
        return f'{bil:.2f} B'
    else:
        mil = num/1000000
        return f'{mil:.2f} M'


def check_selected(selected_options, my_dict):
    opt1 = selected_options[0]
    opt2 = selected_options[1]
    
    if my_dict[opt1] == 'focus':
        return opt1, opt2
    else:
        return opt2, opt1
    
def find_priority(selected_options, my_dict):
    opt1 = selected_options[0]
    opt2 = selected_options[1]
    if my_dict[opt1] == 'name':
        return opt2, opt1
    elif my_dict[opt2] == 'name':
        return opt1, opt2
    elif my_dict[opt1] == 'owner':
        return opt2, opt1
    elif my_dict[opt2] == 'owner':
        return opt1, opt2
    else:
        return opt1, opt2
    

def generate_graph(selected_options, df):
    
    with open('findings/country_corps.json', 'r') as file:
        country_info_dict = json.load(file)
    color_code = {
        'Name (English)': '#04c0b1',
        'Entity owner (English)': '#274d4a',
        'Parent entity (English)': '#088fbc',
        'focus countries': '#e87551'
    }
    temp_my_dict = {
        'Name (English)': 'name',
        'Entity owner (English)': 'owner',
        'Parent entity (English)': 'parent',
        'focus countries': 'focus',
    }

    nodes = []
    edges = []
    node_colors = {}
    if 'focus countries' not in selected_options:
        to_node_name, from_node_name = find_priority(selected_options, temp_my_dict)
        color_1 = color_code[to_node_name]
        color_2 = color_code[from_node_name]
        temp_df = df[['Name (English)', 'Entity owner (English)', 'Parent entity (English)']]
        to_nodes_list = list(df[to_node_name].values)
        for to_node in to_nodes_list:
            from_node_list = list(temp_df[temp_df[to_node_name] == to_node][from_node_name].values)
            for from_node in from_node_list:    
                if to_node not in nodes:
                    nodes.append(to_node)
                    node_colors[to_node] = color_1
                if from_node not in nodes:
                    nodes.append(from_node)
                    node_colors[from_node] = color_2
                edge = [from_node, to_node]
                if edge not in edges:
                    edges.append(edge)

    else:
        opt1, opt2 = check_selected(selected_options, temp_my_dict)
        color_1 = color_code[opt1]
        color_2 = color_code[opt2]
        for country in list(country_info_dict.keys()):
            to_node = country
            items_list = country_info_dict[country][temp_my_dict[opt2]]
            if to_node not in nodes:
                nodes.append(to_node)
                node_colors[to_node] = color_1
            for each in items_list:
                from_node = each
                if from_node not in nodes:
                    nodes.append(from_node)
                    node_colors[from_node] = color_2
                edge = [from_node, to_node]
                if edge not in edges:
                    edges.append(edge)
                    
    return nodes, edges, node_colors

import numpy as np

def create_followers_num_for_country(df):
    temp_df = df[['X (Twitter) Follower #', 'Facebook Follower #', 'Instagram Follower #', 'YouTube Subscriber #', 'TikTok Subscriber #', 'Threads Follower #', 'focus countries']]
    def check_value(value):
        return 0 if np.isnan(value) else value
    temp_dic = {}
    for twitter_fol, facebook_fol, instagram_fol, youtube_fol, tiktok_fol, threads_fol, country_list in temp_df.values:
        for country in country_list:
            if country not in list(temp_dic.keys()):
                temp_dic[country] = {
                    'twitter': check_value(twitter_fol),
                    'facebook': check_value(facebook_fol),
                    'instagram': check_value(instagram_fol),
                    'youtube': check_value(youtube_fol),
                    'tiktok': check_value(tiktok_fol),
                    'threads': check_value(threads_fol),
                }
            else:
                temp_dic[country] = {
                    'twitter': temp_dic[country]['twitter'] + check_value(twitter_fol),
                    'facebook': temp_dic[country]['facebook'] + check_value(facebook_fol),
                    'instagram': temp_dic[country]['instagram'] + check_value(instagram_fol),
                    'youtube': temp_dic[country]['youtube'] + check_value(youtube_fol),
                    'tiktok': temp_dic[country]['tiktok'] + check_value(tiktok_fol),
                    'threads': temp_dic[country]['threads'] + check_value(threads_fol),
                }
    save_file('findings/follower_country.json', temp_dic)
    return temp_dic

def calculate_accounts_num_in_each_platform_per_country(df):
    def check_value(value):
        try:
            return 0 if np.isnan(value) else 1
        except:
            return 1

    temp_df = df[['X (Twitter) handle', 'Facebook page', 'Instragram page', 'Threads account', 'YouTube account', 'TikTok account', 'focus countries']]
    temp_dic = {}
    for twitter, facebook, instagram, threads, youtube, tiktok, country_list in temp_df.values:
        for country in country_list:
            if country not in list(temp_dic.keys()):
                temp_dic[country] = {
                        'twitter': check_value(twitter),
                        'facebook': check_value(facebook),
                        'instagram': check_value(instagram),
                        'youtube': check_value(youtube),
                        'tiktok': check_value(tiktok),
                        'threads': check_value(threads),
                        'total': check_value(twitter) + check_value(facebook) + check_value(instagram) 
                                + check_value(youtube) + check_value(tiktok) + check_value(threads)
                    }
            else:
                temp_dic[country] = {
                        'twitter': temp_dic[country]['twitter'] + check_value(twitter),
                        'facebook': temp_dic[country]['facebook'] + check_value(facebook),
                        'instagram': temp_dic[country]['instagram'] + check_value(instagram),
                        'youtube': temp_dic[country]['youtube'] + check_value(youtube),
                        'tiktok': temp_dic[country]['tiktok'] + check_value(tiktok),
                        'threads': temp_dic[country]['threads'] + check_value(threads),
                        'total': temp_dic[country]['total'] + check_value(twitter) + check_value(facebook) + check_value(instagram) 
                                + check_value(youtube) + check_value(tiktok) + check_value(threads)
                    }
    save_file('findings/platform_accounts_per_country.json', temp_dic)        
    return temp_dic           
import json 

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
    return temp_dic

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

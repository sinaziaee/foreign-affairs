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

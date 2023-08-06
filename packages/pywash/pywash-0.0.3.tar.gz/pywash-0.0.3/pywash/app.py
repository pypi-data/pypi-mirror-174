import re
import csv

def clean(data = '', data_set_name = ''):
    raw_data = ''
    with open (data,'r',encoding = 'utf-8') as data:
        raw_data = data.read()
        

    # Cleaning Raw Data
    # Removing Spaces
    raw_data = raw_data.replace(' ', '')
    # Removing Charaters
    raw_data = re.sub('[A-Za-z]', '', raw_data)
    # Spliting Data into List
    clean_data = raw_data.split(',')
    # Filtering Null Values
    clean_data = list(filter(None,clean_data))
    # Filtering Duplicate Data
    clean_data = list(set(clean_data))


    data_name = data_set_name


    data = []


    num = '00001'
    for x in clean_data:
        sample_list = [data_name+' '+num,'','','','','','','','','','','','','','','','','','','','','','','','','','','','','',x]
        data.append(sample_list)
    #  print(data_name, num)
        val = re.sub(r'[0-9]+$',lambda x: f"{str(int(x.group())+1).zfill(len(x.group()))}",
    num)
        num = val
        
    

    headers = ['Name', 'Given Name', 'Additional Name', 'Family Name', 'Yomi Name', 'Given Name Yomi', 'Additional Name Yomi', 'Family Name Yomi', 'Name Prefix', 'Name Suffix', 'Initials', 'Nickname', 'Short Name', 'Maiden Name', 'Birthday', 'Gender', 'Location', 'Billing Information', 'Directory Server', 'Mileage', 'Occupation', 'Hobby', 'Sensitivity', 'Priority', 'Subject', 'Notes', 'Language', 'Photo', 'Group Membership', 'Phone 1 - Type', 'Phone 1 - Value']


    with open('contacts.csv', 'w') as file:
        output = csv.writer(file)
        output.writerow(headers)
        output.writerows(data)
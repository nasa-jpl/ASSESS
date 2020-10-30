import pandas as pd
import dill

def savemodel(model,outfile):
    with open(outfile, 'wb') as output:
        dill.dump(model, output)
    return ''

def loadmodel(infile):
    model=''
    with open(infile, 'rb') as inp:
        model = dill.load(inp)
    return model


def getID(key):
    global counter
    global ics_map_old_new
    if key not in ics_map_old_new.keys():
        counter += 1
        ics_map_old_new[key] = counter

    return ics_map_old_new[key]

def process(a, col, lst=[]):
    a=str(a)
    if (len(lst)==0 or col in lst) and a!='':
        # because when saving to csv 43.060 becomes 43.06!!
        return '~'+str(a)
    return a

"""
# =================== 
ics categories have an ID, which can be separated into field, group, sub_group and standard.
"""


ics_path='ics.csv' # contains data about how the

df_ics=pd.read_csv(ics_path)

# create the class tree. Have a mapping to actual names of the categories (can get from querying the ics.csv directly).
df_ics_seperated=pd.DataFrame()

ics_dict={-1:[]} # create a taxonomy to input into the Hclassif algo only top two levels
ics_dict_general={-1:[]} # create a general tree (to clearly show the heirachial structure of ics)
for i, row in df_ics.iterrows():

    new_row={}
    type=''
    code=row['code']
    field,group,sub_group,standard,new_field, new_group, new_sub_group, new_standard='','','','','','','',''

    code = code.split('.ISO')
    code_ = code[0].split('.')

    if len(code_) >= 2:
        field = code_[1]
        type = 'field'
        new_field = getID(field)
        ics_dict[-1].append(new_field)
        new_row['id'] = field
        new_row['id_'] = new_field
        ics_dict_general[-1].append(new_field)


    if len(code_) >= 3:
        group = code_[1] + '.' + code_[2]
        type = 'group'
        new_group = getID(group)

        if new_field not in ics_dict.keys():
            ics_dict[new_field] = []
        ics_dict[new_field].append(new_group)

        if new_field not in ics_dict_general.keys():
            ics_dict_general[new_field] = []
        ics_dict_general[new_field].append(new_group)

        new_row['id'] = group
        new_row['id_'] = new_group


    if len(code_) >= 4:
        sub_group = code_[1] + '.' + code_[2] + '.' + code_[3]
        type = 'subgroup'
        new_sub_group = getID(sub_group)

        if new_group not in ics_dict_general.keys():
            ics_dict_general[new_group] = []
        ics_dict_general[new_group].append(new_sub_group)

        new_row['id'] = sub_group
        new_row['id_'] = new_sub_group

    if len(code) > 1:
        standard = 'ISO' + code[1]
        new_standard = getID(standard)
        if type=='field':
            if new_field not in ics_dict_general.keys():
                ics_dict_general[new_field] = []
            ics_dict_general[new_field].append(new_standard)
        if type=='group':
            if new_group not in ics_dict_general.keys():
                ics_dict_general[new_group] = []
            ics_dict_general[new_group].append(new_standard)
        if type=='subgroup':
            if new_sub_group not in ics_dict_general.keys():
                ics_dict_general[new_sub_group] = []
            ics_dict_general[new_sub_group].append(new_standard)
        type = 'standard'


        new_row['id'] = standard
        new_row['id_'] = new_standard



    new_row['field'] = field
    new_row['new_field'] = new_field
    new_row['group'] = group
    new_row['new_group'] = new_group
    new_row['subgroup'] = sub_group
    new_row['new_subgroup'] = new_sub_group
    new_row['standard'] = standard
    new_row['new_standard'] = new_standard
    new_row['code'] = row['code']
    new_row['link'] = row['link']
    new_row['title'] = row['title']
    new_row['type']=type

    to_process_list=['field','new_field','group','new_group','subgroup','new_subgroup','standard','new_standard','code','id','id_']
    new_row={k:process(v, k, to_process_list) for k, v in new_row.items()}



    df_ics_seperated=df_ics_seperated.append(new_row, ignore_index=True)
    print(i)

ics_dict_general_={}
for k,v in ics_dict_general.items():
    k=process(k,'')
    v=list(set(v))
    v=[process(item,'') for item in v]
    ics_dict_general_[k]=v
ics_dict_general=ics_dict_general_

df_ics_seperated.to_csv('ics_separated.csv') # save all things into a csv so that later on lables, ics labels and names could be correlated
savemodel(ics_dict,'ics_dict')
savemodel(ics_dict_general,'ics_dict_general')
savemodel(ics_map_old_new,'ics_map_old_new')




"""
# =================== 
merge the ics data with the iso standards
"""
df_ics_seperated=pd.read_csv('ics_separated.csv', index_col=0)
json_to_csv=pd.read_csv('json_to_csv.csv', index_col=0) # this is the csv version of 'iso_flat.json', contains the iso standards metadata

df_final_all=pd.DataFrame()
counter=0
for _, row in df_ics_seperated.iterrows():
    counter+=1
    print(counter)
    entry=json_to_csv[json_to_csv['url'] == row['link']].values
    new_row={}

    # merge
    if len(entry)!=0:
        for k, v in zip(json_to_csv.columns, entry[0]):
            new_row[k]=v

    for k, v in dict(row).items():
        new_row[k]=v



    df_final_all=df_final_all.append(new_row, ignore_index=True)

df_final_all.to_csv('iso_final_all.csv')

# todo: fix the paths for files

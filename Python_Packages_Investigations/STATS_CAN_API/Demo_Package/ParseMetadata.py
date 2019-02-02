### import stats_can
import datetime as dt
import pandas as pd
import stats_can
import json


import datetime
import qgrid 


from tqdm import tnrange, tqdm_notebook
from time import sleep

## GET CATEGORY 

with open("./subjectcode_PARSE_modified2.txt",'r') as f:
    file_cont = [item for item in f]
f.close()

# Parse entries


all_entries = [file_cont[i:i + 3] for i in range(0, len(file_cont), 3)]
size = len(all_entries)
subject_code = [all_entries[i][0] for i in range(size)]
td_eng = [all_entries[i][1] for i in range(size)]
td_fre = [all_entries[i][2] for i in range(size)]

dictionary = {"SubjectCode":subject_code,"Category(English)":td_eng,"Category(French)":td_fre}

df_subject_code = pd.DataFrame.from_dict(dictionary)
df_subject_code = df_subject_code.replace('\n',' ', regex=True)

sub_code = [item for item in df_subject_code["SubjectCode"]]
cat_en = [item for item in df_subject_code["Category(English)"]]
cat_fr = [item for item in df_subject_code["Category(French)"]]
en_category_dic = {sub_code[i] :cat_en[i]for i in range(size)}
fr_category_dic = {sub_code[i] :cat_fr[i]for i in range(size)}


## Download METADATA

changed_series = get_changed_cube_list("2018-01-31")


changed_series_df = pd.DataFrame.from_dict(changed_series)

product_ids = list(set([item for item in changed_series_df["productId"]]))

metadata = []
for i in tnrange(len(product_ids), desc='Download Cube Metadata'):# For each soup
    sleep(0.01)
    metadata.append(get_cube_metadata(str(product_ids[i])))

    
# Build DF

title_en = []
title_fr = []
start_d = []
end_d = []
nbDatapoints = []
subject_code = []
for item in metadata:
    title_en.append(item[0]["cubeTitleEn"])
    title_fr.append(item[0]["cubeTitleFr"])
    start_d.append(item[0]["cubeStartDate"])
    end_d.append(item[0]["cubeEndDate"])
    nbDatapoints.append(item[0]["nbDatapointsCube"])
    subject_code.append(item[0]["subjectCode"])
    
full = []
for item in subject_code:
    empty = []
    for i in range(len(item)):
        empty.append((en_category_dic[item[i] + " "]))
    full.append(empty)
    
all_str = []
for item in full:
    row_str = ""
    for i in range(len(item)):
        row_str = row_str + item[i] + "\n"
    all_str.append(row_str)

datasets = {'ProductID': product_ids,
         'StudyTitleEnglish': title_en,
         'StudyTitleFrench': title_fr,
           'StartDate' : start_d,
           'EndDate' : end_d,
           'NumberOfDataPoints' : nbDatapoints,
            "Category":all_str}
df = pd.DataFrame(datasets)
cols = ['ProductID', 'Category','StudyTitleEnglish','StudyTitleFrench','NumberOfDataPoints','StartDate', 'EndDate']
df = df[cols]



## Display DF
grid_features = { 'fullWidthRows': True,
                 'syncColumnCellResize': True,
                 'forceFitColumns': True,
                  'defaultColumnWidth': 150,
                  'syncColumnCellResize': True,
                  'forceFitColumns': True,
                  'rowHeight': 40,
                  'enableColumnReorder': True,
                  'enableTextSelectionOnCells': True,
                  'editable': True,
                  'filterable': True,
                  'sortable': True,
                  'highlightSelectedRow': True}


qgrid_widget = qgrid.show_grid(df, show_toolbar=False)
display(qgrid_widget)
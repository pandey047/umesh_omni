
# python /Users/cfunaki/Documents/Omni/data_source_sql_template.py

# 1) Open the Data Model config
# 2) Open the Data Source config
# 3) Open the SQL template, based on the config value 'data_source_type'
# 4) Render the SQL query

import json
from pprint import pprint
from jinja2 import Template, Environment, FileSystemLoader


# base_dir = '/Users/cfunaki/Documents/Omni/'
# config_dir = 'ConfigFiles'
# sql_dir = 'SQLTemplates'


# 1) Open the Data Model config

# data_model_config_file_str = 'data_model' + '.json'

# with open(base_dir + config_dir + '/' + data_model_config_file_str, 'r') as f:
# 	data_model_config = json.load(f)
#pprint(data_model_config)
with open(r'D:\Umesh_Proj\Omni\omniProj\uploads\datamodels\data_model.json','r') as l:
    json_data_model=json.load(l)
    # print(json_data2)

# 2) Open the Data Source config

# data_source_config_file_str = 'data_source' + '.json'

# with open(base_dir + config_dir + '/' + data_source_config_file_str, 'r') as f:
# 	data_source_config = json.load(f)
#pprint(data_source_config)
with open(r'D:\Umesh_Proj\Omni\omniProj\uploads\datasource\data_source.json','r') as l:
    json_data_source=json.load(l)
    # print(json_data_source)


# 3) Open the SQL template, based on the config value 'data_source_type'



# sql_file_str = data_source_config['simple_aggregation'] + '.sql'
# template_file = open(base_dir + sql_dir + '/' + sql_file_str, "r").read()
#print(template_file)
json_data_sql=open(r'D:\Umesh_Proj\Omni\omniProj\simple_aggregation.sql','r').read()
# print(json_data_sql)

# 4) Render the SQL query

t = Template(json_data_sql)

sql = t.render(
	data_model = json_data_model,
	data_source = json_data_source
)

print("sqldata",sql)
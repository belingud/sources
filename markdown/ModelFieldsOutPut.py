#!/usr/bin/env python
import django
import os
import sys
from django.apps import apps
from django.db import connection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SantaClara.settings")
django.setup()

args = sys.argv

models = apps.all_models


def get_app_models(arg, all_models):
    if arg == 'all':
        return all_models
    else:
        return all_models[arg]


file_path = args[2] if len(args) == 3 else 'fields_detail.md'

if not file_path.endswith('.md'):
    sys.exit('the second argument file path has to be a markdown file, now it`s {0}'.format(file_path))

try:
    arg = args[1]
    all_models = get_app_models(arg, models)
    # OrderDict
except IndexError:
    all_models = models.values()

# print('all_models: ', all_models)
markdown_lines = []

table_name = """\n\n## {0}--{1}\n\n"""
table_header = """| 字段名 | 数据类型 | 允许为空 | PK | 字段说明 |
| ---- | ---- | ---- | --- | ---- |
"""
field_desc_str = '| {0} | {1} | {2} | {3} | {4} |'
new_line_str = '\n'


def get_models_fields():
    """
    get all models and fields, format field description by field_desc_str
    append every field description into file_write_lines
    and write into file if given a specific app name, and file name
    :return:
    :rtype:
    """
    for model_odict in all_models:
        for model in model_odict.values():
            markdown_lines.append(table_name.format(model.__name__, model._meta.db_table))
            fields_list = model._meta.get_fields()
            ########
            markdown_lines.append(table_header)
            for field in fields_list:
                field_name = field.name
                field_type = field.db_type(connection)
                field_null = field.null
                try:
                    field_limit = field.primary_key
                except AttributeError:
                    field_limit = False
                try:
                    field_verbose = field.verbose_name
                except AttributeError:
                    field_verbose = ' '
                _field_str = field_desc_str.format(str(field_name), str(field_type), str(field_null),
                                                   str(field_limit), str(field_verbose))
                #############
                print('_field_str: ', _field_str, end=new_line_str)
                markdown_lines.append(_field_str + new_line_str)
            markdown_lines.append(new_line_str * 2)


def write_to_md(file_path):
    """
    write fields detail into a markdown file,
    file_path could be specific
    :param file_path:
    :type file_path:
    :return:
    :rtype:
    """
    with open(file_path, 'w') as fp:
        print('prepare to write markdown file')
        print(len(markdown_lines))
        fp.writelines(markdown_lines)


# python model_fields.py
# ---> fields_detail.md
# python model_fields.py api_home
# ---> fields_detail.md  # include all models in api_home module
# python models_fields.py all ~/docs/model_field.md
# ---> ~/docs/model_field.md  # include all models and output a specific markdown file
# python model_fields.py company company_models.md
# ---> company_models.md  # include all models in company models and output a specific markdown file


def main(file_path):
    """
    main
    :param file_path:
    :type file_path:
    :return:
    :rtype:
    """
    get_models_fields()
    write_to_md(file_path)


if __name__ == '__main__':
    main(file_path)

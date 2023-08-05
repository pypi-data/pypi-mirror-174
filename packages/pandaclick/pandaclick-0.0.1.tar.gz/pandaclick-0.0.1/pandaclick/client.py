from jinja2 import Template
from runpy import run_path
import sqlalchemy
import os

model_class_template = '''
import pandas as pd
from infi.clickhouse_orm.engines import ReplacingMergeTree, MergeTree
from infi.clickhouse_orm.fields import UInt16Field, StringField, NullableField, Int64Field,Float64Field
from infi.clickhouse_orm.models import Model
from infi.clickhouse_orm import Database
from sqlalchemy import create_engine

class ModelObj(Model):
    {% for row in fields %}{{row}}
    {% endfor %}

    engine = MergeTree(partition_key={{partition_key}}, order_by={{order_by}})

    @classmethod
    def table_name(cls):
        return '{{table_name}}'


engine = create_engine('{{connection}}')

with engine.connect() as conn:
    conn.connection.create_table(ModelObj)
'''


class PandaClick:

    def __init__(self, connection, table_name, partition_key, order_by):
        self.connection = connection
        self.table_name = table_name
        self.partition_key = partition_key
        self.order_by = order_by

    def write(self, item, replace=False):

        fields_map = {
            'int64': 'Int64Field()',
            'bool': 'UInt16Field()',
            'float64': 'Float64Field()',
            'object': "StringField()",
        }

        fields = []
        for c in item.columns:

            if (c == 'index'):
                continue

            if (c in self.partition_key or c in self.order_by):
                fields.append('{} = {}'.format(c, fields_map[str(item[c].dtype)]))
            else:
                fields.append('{} = NullableField({})'.format(c, fields_map[str(item[c].dtype)]))

        template = Template(model_class_template)

        mpdel_file = 'model_' + self.table_name + ".py"
        with open(mpdel_file, 'w') as fw:
            fw.write(
                template.render(
                    table_name=self.table_name,
                    partition_key=str(self.partition_key),
                    order_by=str(self.order_by),
                    fields=fields,
                    connection=self.connection
                )
            )

        self.model_lib = run_path(mpdel_file)
        os.remove(mpdel_file)

        if (replace):
            with self.model_lib['engine'].connect() as conn:
                conn.connection.drop_table(self.model_lib['ModelObj'])
                conn.connection.create_table(self.model_lib['ModelObj'])

        item = self.format_to_write(item)
        item.to_sql(self.table_name, self.model_lib['engine'], if_exists='append', index=False)

    def format_to_write(self, item):
        item = item.drop('index', axis=1, errors='ignore')
        for c in item.columns:
            if (str(item[c].dtype) == 'bool'):
                item[c] = item[c].astype(int)
        return item



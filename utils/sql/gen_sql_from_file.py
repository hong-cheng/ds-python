""" generate create table and insert sql statements from input files.
Input files can be csv or text (tab or space delimited)

exampe:
    python3 gen_sql_from_file.py -i refund.txt -t demand2

"""
import sys
import os
import re
import csv
from argparse import ArgumentParser

### check for the input file
def check_input_file(input_file):
    if not os.path.exists(input_file):
        print(f"ERROR: input file does not exist: {input_file}")

### read the input file, generate sql statements
###
def gen_sql(input_file, table_name=None):
    delimiter = ','
    with open(input_file) as f:
        if input_file.endswith('.csv'):
            reader = csv.reader(f)
        else:
            reader = csv.reader(f, delimiter='\t')
            delimiter = '\t'

        reader = csv.reader(f)
        first_row = next(reader)
        #print(f"first row: {first_row}")
        header_line = first_row[0]     ### the reader returns a list of strings, first item is the headers
        headers = header_line.split(delimiter)

        ### sample the first line of data to figure out what the data type is for each column
        col_types = []
        first_data_line = next(reader)[0]
        #print(f"first data: {first_data_line}")
        data_fields = first_data_line.split(delimiter)
        #print(f"data fields: {data_fields}")
        for i, col in enumerate(data_fields):
            if col.isdigit():
                col_types.append('int')
            elif col.replace('.', '', 1).isdigit():
                    col_types.append('float')
            else:
                col_types.append('varchar')
        #print(f"-- col types: {col_types}")

        ### if the table name is note specified, use the file name as the table name
        ### ie:  if the filename is: refund.txt, table name will be: refund
        if table_name is None:
            table_name = input_file.split('.')[0]

        ### use the input file name as the table name
        CREATE_TABLE_STMT = f"CREATE TABLE IF NOT EXISTS {table_name} ("
        for i, col in enumerate(headers):
            CREATE_TABLE_STMT += f"\n  {col} {col_types[i]},"

        ### get rid of the last comma and replace with closing: );
        CREATE_TABLE_STMT = CREATE_TABLE_STMT[:-1]
        CREATE_TABLE_STMT += "\n);\n"
        print("\n" + CREATE_TABLE_STMT)

        INSERT_STMT = f"INSERT INTO {table_name} VALUES "
        for i, col_data in enumerate(first_data_line.split(delimiter)):
            #print(f"{i}: {col_data}")
            if i==0:
                INSERT_STMT += f"\n  ("

            if col_types[i] in ('int', 'float'):
                INSERT_STMT += f" {col_data},"
            else:
                INSERT_STMT += f" '{col_data}',"
        INSERT_STMT = INSERT_STMT[:-1]  ### get rid of the last comma
        INSERT_STMT += "),"

        while (True):
            try:
                line = next(reader)[0]
                for i, col_data in enumerate(line.split(delimiter)):
                    #print(f"{i}: {col_data}")
                    if i==0:
                        INSERT_STMT += f"\n  ("

                    if col_types[i] == 'int':
                        INSERT_STMT += f" {col_data},"
                    else:
                        INSERT_STMT += f" '{col_data}',"
                INSERT_STMT = INSERT_STMT[:-1]  ### get rid of the last comma
                INSERT_STMT += "),"

            except StopIteration:
                break

            #print(f"-- line: {line}")

        INSERT_STMT = INSERT_STMT[:-1]  ### get rid of the last comma
        INSERT_STMT += ";\n"
        print(INSERT_STMT)

        print(f"select * from {table_name} limit 5;\n")

if __name__ == '__main__':
    parser = ArgumentParser(description='generate create table and insert sql statements from input files')
    parser.add_argument('-i', '--input_file', help='input file name', required=True)
    parser.add_argument('-t', '--table_name',
        help='Optional: table name, else will use the filenanme as the table name', required=False)
    args = parser.parse_args()

    check_input_file(args.input_file)
    gen_sql(args.input_file, args.table_name)
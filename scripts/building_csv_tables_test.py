import json
import csv
# 3 following lines are specific to the file structure for importing the lib client
import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
# import the lib client
from lib.client import Api
# instantiate the lib client
client = Api()


result1 = client.toflit.get_classification_sliced_search("product_orthographic") # tester avec seulement 200 produits


names_orthographic = []
for s in result1: # s est un dictionnaire python         
    names_orthographic.append(s["name"])  
# print ("\n toflit products (orthographic):", names_orthographic)

# initialisation du tableau avec noms tels que dans la clasification 
with open('dumps/transfo_names_ortho_products.csv', 'w', newline='') as csvfile:
        fieldnames = ['name_orthographic']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in names_orthographic:
                    writer.writerow({'name_orthographic': i})

#2 transfo lowercase
orthographic_low = []
for i in names_orthographic:
    orthographic_low.append(i.lower())
# print(" -------------------- list orthographic lower: \n",orthographic_low)

from csv import DictReader
from csv import DictWriter

def add_column_in_csv_2(input_file, output_file, iterable, transform_row, tansform_column_names):
    """ Append a column in existing csv using csv.reader / csv.writer classes"""
    # Open the input_file in read mode and output_file in write mode
    with open(input_file, 'r') as read_obj, \
            open(output_file, 'w', newline='') as write_obj:
        # Create a DictReader object from the input file object
        dict_reader = DictReader(read_obj)
        # Get a list of column names from the csv
        field_names = dict_reader.fieldnames
        # Call the callback function to modify column name list
        tansform_column_names(field_names)
        # Create a DictWriter object from the output file object by passing column / field names
        dict_writer = DictWriter(write_obj, field_names)
        # Write the column names in output csv file
        dict_writer.writeheader()
        # Read each row of the input csv file as dictionary
        for row, item in zip(dict_reader, iterable): 
            # Modify the dictionary / row by passing it to the transform function (the callback)
            transform_row(row, dict_reader.line_num, item)
            # Write the updated dictionary or row to the output file
            dict_writer.writerow(row)

# complétion du tableau avec noms transformés en lowercase
header_of_new_col = 'lowercase_name'
# Add a Dictionary as a column in the existing csv file using DictWriter class
add_column_in_csv_2('dumps/transfo_names_ortho_products.csv', 'dumps/transfo_names_ortho_products_1.csv', orthographic_low,
                    lambda row, line_num, item: 
                            row.update({header_of_new_col: item}), 
                    lambda field_names: field_names.append(header_of_new_col))



import pandas as pd
from pyperseo.functions import milisec as milisec
from Hefesto.template import Template
import sys
import yaml


class Hefesto:

    def transform_shape(path_datainput,configuration):

        if type(configuration) is not dict:
            sys.exit("configuration file must be a dictionary from a Python, YAML or JSON file")

        
        # Import static template for all CDE terms:
        temp = Template.template_model

        # Import data input:
        df_data = pd.read_csv(path_datainput)
        
        # Empty objects:
        resulting_df = pd.DataFrame()
        row_df = {}

        # Iterate each row from data input
        # check each YAML object from configuration file to set the parameters
        for row in df_data.iterrows():

            for config in configuration.items():

                # Create a unique stamp per new row to about them to colapse:
                milisec_point = milisec()

                row_df.update({milisec_point: {'model':config[0]}})
                
                # Add YAML template static information
                for cde in temp.items():
                    if cde[0] == row_df[milisec_point]["model"]:
                        row_df[milisec_point].update(cde[1])

                # Relate each YAML parameter with original data input
                for element in config[1]["columns"].items():
                    for r in row[1].index:
                        if r == element[1]:
                            dict_element = {element[0]:row[1][r]}
                            row_df[milisec_point].update(dict_element)

                # Delete all "empty" row that doesnt contain valueOutput
                if row_df[milisec_point]["valueOutput"] == None:
                    del row_df[milisec_point]
                else:
                    # Add new dict with extracted information into a Data frame
                    final_row_df = pd.DataFrame(row_df[milisec_point], index=[1])
                resulting_df = pd.concat([resulting_df, final_row_df])

        # uniqid (re)generation:
        resulting_df = resulting_df.reset_index(drop=True)

        resulting_df['uniqid'] = ""
        for i in resulting_df.index:
            resulting_df.at[i, "uniqid"] = milisec()

        return resulting_df

# # Test
with open("../data/config.yaml") as file:
    configuration = yaml.load(file, Loader=yaml.FullLoader)

test = Hefesto.transform_shape(path_datainput ="../data/exemplarCDEdata2.csv", configuration=configuration)
test.to_csv ("../data/result.csv", index = False, header=True)
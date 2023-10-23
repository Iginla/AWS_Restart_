import json
import os

def readJsonFile(fileName):
    data = ""
    try:
        with open(fileName) as json_file:
            data = json.load(json_file)
    except IOError:
        print("Could not read file")
    return data

# Check if the file exists before attempting to read it
file_path = 'files/insulin.json'
if os.path.exists(file_path):
    data = readJsonFile(file_path)

    if data:
        bInsulin = data['molecules']['bInsulin']
        aInsulin = data['molecules']['aInsulin']
        insulin = bInsulin + aInsulin
        molecularWeightInsulinActual = data['molecularWeightInsulinActual']
        print('bInsulin: ' + bInsulin)
        print('aInsulin: ' + aInsulin)
        print('molecularWeightInsulinActual: ' + str(molecularWeightInsulinActual))
    else:
        print("Error reading JSON data.")
else:
    print(f"The file '{file_path}' does not exist.")

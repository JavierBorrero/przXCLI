import os
import json

"""Cargar el archivo JSON si no existe lo crea"""
def load_file(filename):
    if(os.path.exists(filename)):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        return {"tasks": []}

"""Guardar la informacion en el JSON"""
def save_data(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
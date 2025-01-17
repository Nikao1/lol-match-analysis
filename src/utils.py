import os
import json

def save_to_json(filename, data):
    # Extrai o diretório do caminho do arquivo
    directory = os.path.dirname(filename)
    # Cria o diretório se ele não existir
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    # Salva o arquivo JSON
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

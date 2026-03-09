#!/usr/bin/env python3
import json

for company in ['company_n', 'company_a', 'company_u']:
    nb_path = f'{company}/{company}_visualization.ipynb'
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    # Find the visualization cell
    for idx, cell in enumerate(nb['cells']):
        source = ''.join(cell['source'])
        if 'fig = plt.figure(figsize=(16, 12))' in source:
            lines = source.split('\n')
            
            plt_import_line = None
            plt_figure_line = None
            
            for i, line in enumerate(lines, 1):
                if 'import matplotlib.pyplot as plt' in line:
                    plt_import_line = i
                if 'fig = plt.figure(figsize=(16, 12))' in line:
                    plt_figure_line = i
            
            if plt_import_line and plt_figure_line:
                status = "OK" if plt_import_line < plt_figure_line else "ERROR"
            else:
                status = "MISSING"
            
            print(f"{company}: import at {plt_import_line}, used at {plt_figure_line} - {status}")

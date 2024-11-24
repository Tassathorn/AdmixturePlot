import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import sys
import os
import time

import warnings
warnings.filterwarnings("ignore")

input_path = sys.argv[1]
fam_file = sys.argv[2]

start = time.process_time()

files = os.listdir(input_path)
q_files = [f for f in files if f.endswith(".Q")]
q_files.sort()

fam_data = pd.read_csv(fam_file, sep='\s+', header=None)
sample_ids = fam_data[1].to_list()

output_pdf = PdfPages('admixture_plots.pdf')

K_values = []
CV_errors = []

if os.path.exists(input_path + 'cv_error.txt'):
    with open('cv_error.txt', 'r') as file: 
        for line in file:
            if "CV error" in line:
                parts = line.split(':')
                K = int(parts[0].split('=')[1].replace(')', '').strip()) 
                CV_error = float(parts[1].strip())
                K_values.append(K)
                CV_errors.append(CV_error)

    fig, ax = plt.subplots(figsize=(10, 5.625))
    plt.plot(K_values, CV_errors, marker='o', linestyle='-', color='b', label='CV Error')

    plt.xlabel('K (Number of Ancestral Populations)')
    plt.ylabel('CV Error')
    plt.title('Cross-Validation Error for Different K values in ADMIXTURE')
    plt.grid(True)
    plt.legend()
    output_pdf.savefig(fig)

for i in range(len(q_files)):
    admixture_data = pd.read_csv(input_path+q_files[i], sep='\s+', header=None)
    column_list = []
    for j in range(len(admixture_data.columns)):
        column_list.append(f"{j+1}")
    admixture_data.columns = column_list
    admixture_data['Sample'] = sample_ids
    
    fig, ax = plt.subplots(figsize=(10, 5.625))

    bottom = pd.Series([0] * len(admixture_data))
    colors = ["#FF0000", "#FFBF00", "#80FF00", "#00FF40", "#00FFFF", "#0040FF", "#8000FF", "#FF00BF"]

    for i, cluster in enumerate(column_list):
        ax.bar(admixture_data['Sample'], 
               admixture_data[cluster], 
               bottom=bottom, 
               color=colors[i], 
               label=cluster,
               edgecolor='black', 
               linewidth=0.75,
               )
        bottom += admixture_data[cluster]

    ax.set_ylim(bottom=0)
    ax.set_xticklabels(admixture_data['Sample'], rotation=90)
    ax.set_ylabel('Ancestry')
    ax.set_xlabel(f'Individual (total={len(admixture_data)})')
    ax.legend(loc='center right', 
              bbox_to_anchor=(1.10, 0.5),
              title="k"
              )
    plt.title(f'ADMIXTURE Analysis (K={i+1})')
    plt.tight_layout()
    # plt.savefig(f'admixture_K={i+1}.png', dpi=300, bbox_inches='tight')
    output_pdf.savefig(fig)
    plt.close(fig)
    
output_pdf.close()

print("Time process:", time.process_time() - start, "second")

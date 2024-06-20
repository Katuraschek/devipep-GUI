import tkinter as tk
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

from peptide_analysis_toolbox.main import experiment

def submit():
    global ex, output_directory_path, results_ratio
    # Get values from the entry fields
    folder_path = folder_path_var.get()
    pep_filename = pep_filename_var.get()
    pro_filename = pro_filename_var.get()
    meta_filename = meta_filename_var.get()
    protein_info_path = protein_info_path_var.get()
    output_directory_path = output_directory_path_var.get()

    disease_state = disease_state_var.get()
    healthy_state = healthy_state_var.get()
    disease_states = [state.strip() for state in disease_states_var.get().split(',')]
    meta_ID_column = meta_ID_column_var.get()
    pre_hook, post_hook = [hook.strip() for hook in hook_var.get().split(',')]
    experiment_name = experiment_name_var.get()
    
    # Get the selected options from the Listbox
    selected_options = listbox.curselection()
    selected_values = [listbox.get(idx) for idx in selected_options]
    
    # create experiment object from peptide_analysis_toolbox
    ex = experiment(
      peptide_file = pep_filename,
      protein_file = pro_filename,
      metadata_file = meta_filename,
      input_folder = folder_path,
      protein_info_file= protein_info_path,
      experiment_name= experiment_name,

      disease_state_var = disease_state,
      healthy_state_label = healthy_state,
      disease_states = disease_states,
      meta_id_column = meta_ID_column,
      pep_patient_id_pre_hook = pre_hook,
      pep_patient_id_post_hook = post_hook,
      pro_patient_id_pre_hook = pre_hook,
      pro_patient_id_post_hook = post_hook,
)
    # run analysis from peptide_analysis_toolbox
    if "Distance analysis" in selected_values:
        results_dist = ex.distance_analysis(output_directory=output_directory_path)
        results_dist[results_dist.pval_w_AD_BH <= 0.05].head()

    if "Ratio analysis" in selected_values:
        results_ratio = ex.ratio_wilcox_analysis(output_directory=output_directory_path)
        results_ratio[results_ratio.pval_AD_BH <= 0.05].head()

    if "Fisher's exact test" in selected_values:
        results_detection = ex.detection_fisher_analysis(output_directory=output_directory_path)
        results_detection[results_detection.pval_AD_BH <= 0.05].head()

    # Perform analysis or pass parameters to analysis function
    print("Starting analysis...")
    print("Given folder path:", folder_path)
    print("Given peptide file name:", pep_filename)
    print("Given protein file name:", pro_filename)
    print("Given metadata filename:", meta_filename)
    print("Given protein info file path:", protein_info_path)
    print("Output directory:", output_directory_path)
    print("Name of disease state:", disease_state)
    print("Name of healthy state:", healthy_state)
    print("Disease states of interest:", disease_states)
    print("Column name with ID:", meta_ID_column)
    print("Pre-hook:", pre_hook)
    print("Post-hook:", post_hook)
    print("Your experiment name:", experiment_name)
    print("Selected options:", selected_values)

    # ------------------------------------- CODE FOR GUI SUBPLOT ------------------------------
    # Open new window after analysis
    analysis_finished_window = tk.Toplevel(root)
    analysis_finished_window.title("Sonja's Plot - Plot")

    # frame, label, entry und button für die linke Seite
    left_frame = tk.Frame(analysis_finished_window, bd=2, relief=tk.GROOVE)
    left_frame.grid(row=0, column=0, padx=5, pady=5)
    left_heading = tk.Label(left_frame, text="Plot specific peptide", font=("Arial", 12, "bold"))
    left_heading.grid(row=0, column=0, padx=5, pady=5)

    specific_peptide_label = tk.Label(left_frame, text="Enter the name of the specific peptide:", font=("Arial", 10), anchor="w")
    specific_peptide_label.grid(row=1, column=0, padx=5, pady=(5, 0))
    specific_peptide_entry = tk.Entry(left_frame, width=50)
    specific_peptide_entry.grid(row=2, column=0, padx=5, pady=(0, 5))
    specific_peptide_explanation = tk.Label(left_frame, text="e.g.: P01042_KNG1_644_487-GGHVLDHGHK2-496_ST", font=("Arial", 8), anchor="w")
    specific_peptide_explanation.grid(row=3, column=0, padx=5, pady=(0, 5))

    def plot_specific(plot_type):
        specific_peptide = specific_peptide_entry.get()
        print("Specific peptide:", specific_peptide)
        print("Plot type:", plot_type)
        plt.close('all') 
        ex.create_plot_for_peptide(specific_peptide, plot_type=plot_type)
        plt.show()

    jointplot_button = tk.Button(left_frame, text="Jointplot", command=lambda: plot_specific("jointplot"))
    jointplot_button.grid(row=4, column=0, padx=5, pady=(0, 5))
    masterplot_button = tk.Button(left_frame, text="Masterplot", command=lambda: plot_specific("masterplot"))
    masterplot_button.grid(row=4, column=1, padx=5, pady=(0, 5))
    boxplot_button = tk.Button(left_frame, text="Boxplot", command=lambda: plot_specific("boxplot"))
    boxplot_button.grid(row=4, column=2, padx=5, pady=(0, 5))

    # frame, label, entry und button für die rechte Seite
    right_frame = tk.Frame(analysis_finished_window, bd=2, relief=tk.GROOVE)
    right_frame.grid(row=0, column=1, padx=5, pady=5)
    right_heading = tk.Label(right_frame, text="Plot top X plots", font=("Arial", 12, "bold"))
    right_heading.grid(row=0, column=0, padx=5, pady=5)

    plot_count_label = tk.Label(right_frame, text="Enter the number of plots to generate:", font=("Arial", 10), anchor="w")
    plot_count_label.grid(row=1, column=0, padx=5, pady=(5, 0))
    plot_count_entry = tk.Entry(right_frame, width=10)
    plot_count_entry.grid(row=2, column=0, padx=5, pady=(0, 5))

    def plot_top():
        plot_count = plot_count_entry.get()
        print("Plot count:", plot_count)
        ex.plot_top_x_most_significant_peptides(output_directory=output_directory_path, results_table=results_ratio, top_x=int(plot_count))

    plot_top_button = tk.Button(right_frame, text="Plot top X plots", command=plot_top)
    plot_top_button.grid(row=3, column=0, padx=5, pady=(0, 5))
# ----------------------------------------------- CODE FOR GUI ------------------------------------------

# Create main window
root = tk.Tk()
root.title("Sonja's Plot")

# Create a container frame to hold all widgets
container = tk.Frame(root)
container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Frame for file name and paths
frame = tk.Frame(container, bd=2, relief=tk.GROOVE)
frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

title_label = tk.Label(frame, text="FILENAME AND PATHS", font=("Arial", 10, "bold"))
title_label.grid(row=0, columnspan=2, pady=(0, 10))

folder_path_var = tk.StringVar()
pep_filename_var = tk.StringVar()
pro_filename_var = tk.StringVar()
meta_filename_var = tk.StringVar()
protein_info_path_var = tk.StringVar()
output_directory_path_var = tk.StringVar()

entries = [
    ("Folder path:", folder_path_var),
    ("Peptide filename:", pep_filename_var),
    ("Protein filename:", pro_filename_var),
    ("Metadata filename:", meta_filename_var),
    ("Protein info filepath:", protein_info_path_var),
    ("Output directory path:", output_directory_path_var)
]

for i, (label_text, var) in enumerate(entries, start=1):
    label = tk.Label(frame, text=label_text)
    label.grid(row=i, column=0, padx=2, pady=2, sticky="w")
    entry = tk.Entry(frame, textvariable=var, width=60)
    entry.grid(row=i, column=1, padx=2, pady=2, sticky="w")

# Additional information text
additional_info_text = """
INFORMATION:
- Provide the path to the folder containing the data (protein, peptide, metadata) and finish the path with a / (e.g., peptide_analysis_toolbox/data/)
- Provide the extension of the file (protein, peptide, metadata) as .tsv, .csv, or other (e.g., example_pr_matrix.tsv or example_meta.csv)
- If you want to include information about the protein sequence in the analysis (protein info filepath), you need an additional input file that
  can be downloaded from UniProt, for example, for all human proteins: https://www.uniprot.org/uniprotkb?query=%28organism_id%3A9606%29
  Afterwards, you need to provide the whole path (e.g., peptide_analysis_toolbox/data/uniprotkb_protein_info_human.tsv)
- The output directory should end with a / (e.g., peptide_analysis_toolbox/data/example_results/)
"""
additional_info_display = tk.Label(frame, text=additional_info_text, justify="left", font=("Arial", 7))
additional_info_display.grid(row=len(entries)+1, columnspan=2, padx=2, pady=2, sticky="w")

# Frame for additional input fields
meta_frame = tk.Frame(container, bd=2, relief=tk.GROOVE)
meta_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

meta_title_label = tk.Label(meta_frame, text="METADATA", font=("Arial", 10, "bold"))
meta_title_label.grid(row=0, columnspan=2, pady=(0, 10))

disease_state_var = tk.StringVar()
healthy_state_var = tk.StringVar()
disease_states_var = tk.StringVar()
meta_ID_column_var = tk.StringVar()
hook_var = tk.StringVar()
experiment_name_var = tk.StringVar()

meta_entries = [
    ("Disease state column name:", disease_state_var),
    ("Healthy state label:", healthy_state_var),
    ("All needed disease states:", disease_states_var),
    ("Meta ID column name:", meta_ID_column_var),
    ("Patients ID pre and post hook:", hook_var),
    ("Your experiment name:", experiment_name_var)
]

for i, (label_text, var) in enumerate(meta_entries, start=1):
    label = tk.Label(meta_frame, text=label_text)
    label.grid(row=i, column=0, padx=2, pady=2, sticky="w")
    entry = tk.Entry(meta_frame, textvariable=var, width=60)
    entry.grid(row=i, column=1, padx=2, pady=2, sticky="w")

# Additional information text for the additional frame
meta_info_text = r"""
ADDITIONAL INFORMATION:
- The disease state column name is the header of the metadata column containing the grouping into disease states, e.g., CognitiveStatus
- The healthy state label must be one column within the disease state column used as healthy reference, e.g., normal
- All needed disease states are all disease states of interest within the disease state column, comma-separated (e.g., AD, MCI)
- Meta ID column name is the name of the column containing the IDs, e.g., SampleID
- The pre and post hook are the areas immediately before and after the patients ID.
  Example: If your identifier is JHU_CSF_SP3_DIA\JHU_AD_CSF_SP3_PRO_DIA_3_S5-D1_1_15770.d 
  and the patient's ID is 3, then enter: DIA_, _)
"""
meta_info_label = tk.Label(meta_frame, text=meta_info_text, justify="left", font=("Arial", 7))
meta_info_label.grid(row=len(meta_entries)+1, columnspan=2, padx=2, pady=2, sticky="w")

# Create the Listbox with analysis options
listbox_frame = tk.Frame(container, bd=2, relief=tk.GROOVE)
listbox_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

listbox_label = tk.Label(listbox_frame, text="Select analysis options:", font=("Arial", 10, "bold"))
listbox_label.pack(side=tk.TOP, pady=(0, 5))

options = ["Ratio analysis", "Fisher's exact test", "Distance analysis"]
listbox = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE, height=len(options))
for option in options:
    listbox.insert(tk.END, option)
listbox.pack(side=tk.LEFT, padx=(0, 10))
listbox.selection_set(0)  # Set default selection

# Create the button for "Run analysis"
submit_button = tk.Button(container, text="Run analysis", command=submit)
submit_button.grid(row=2, columnspan=2, padx=10, pady=10)

# Configure grid weights to make sure the frames and button expand properly
container.grid_columnconfigure(0, weight=1)
container.grid_columnconfigure(1, weight=1)
container.grid_rowconfigure(0, weight=1)
container.grid_rowconfigure(1, weight=1)


# Run the Tkinter event loop
root.mainloop()
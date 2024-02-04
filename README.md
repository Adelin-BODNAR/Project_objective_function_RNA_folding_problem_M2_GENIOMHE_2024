# Project_objective_function_RNA_folding_problem_M2_GENIOMHE_2024

### /!\ The python environment necessary for the good functioning is not included
### Please execute the following commandes to install the virtual environment or install the python packages listed in requirements.txt

## Virtual environment

### Creating a vitual environment
python -m venv .venv

### Activating the virtual environment
source .venv/bin/activate

### Deactivating the virtual environment
deactivate

### Saving the libraries installed while the environment is activated
pip freeze > requirements.txt

### Installing the libraries on the environment from the "requirements.txt" file while the environment is activated
pip install -r requirements.txt

## Usage of the scripts

### Usage of Training.py

python [Path_to_Training.py] [-h, --help] [--plot] [Path_to_data_directory]
        [Path_to_Training.py] : Path to this training script
        [-h, --help] : Prints this help text
        [--plot] : Use if plots of the intermediary and scores distributions wanted
        [Path_to_data_directory] : Path to the data directory
                Must contain a directory containing pdb files

### Usage Plotting.py

python [Path_to_Plotting.py] [-h, --help] [Path_to_data_directory]
        [Path_to_Plotting.py] : Path to this plotting script
        [-h, --help] : Prints this help text
        [Path_to_data_directory] : Path to the data directory
                Must contain a directory containing the score csv files

### Usage Scoring.py

python [Path_to_Scoring.py] [-h, --help] [Path_to_data_directory]
        [Path_to_Scoring.py] : Path to this scoring script
        [-h, --help] : Prints this help text
        [Path_to_data_directory] : Path to the data directory
                Must contain a directory containing the score csv files and another containing only the input pdb file

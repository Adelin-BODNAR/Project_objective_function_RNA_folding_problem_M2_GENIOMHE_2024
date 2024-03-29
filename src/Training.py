from importlib.resources import path
from math import sqrt, log
from Utility_script import save_to_csv
import glob
import os
import sys

from Plotting import plot_distrib, plot_distrib_by_pairs

def get_interatomic_distances_distribution_by_pairs(filename, distances_distribution_by_pairs = dict(),round_down = True):

	""" Function parsing a pdb file to get the distribution of interatomic distances between each possible pair of nucleosides

	Parameters
	----------
	filename
		String containing the path to the pdb file that must be parsed
	distances_distribution_by_pairs
		Dictionary in which the distribution of distances by pairs is stored
		Pass the same dictionary for multiple files to get the distribution across all of them
	round_down
		Boolean used to know if the distances should be rounded down or not
		True should be used for the training and False for the scoring

	Returns
	-------
	distances_distribution_by_pairs
		Dictionary containing the distribution of distances for each pair of nucleosides
	
	"""

	lines = []

	#Gets the lines from the "filename" file and strips them of the Carriage Return at the end of the line
	with open(filename) as f:
		lines = [line.rstrip() for line in f]

	#Keeps only the lines containing atoms (Line starts with "ATOM")
	atom_lines = [line for line in lines if line[0:6].replace(" ", "") == "ATOM"]
	
	#Keeps only the lines with C3' atoms
	C3_lines = [line for line in atom_lines if line[12:16].replace(" ", "") == "C3'"]
	
	#Get the set of chain IDs in the file
	chain_ids = set([line[21] for line in C3_lines])

	#Dictionnary for parsed lines for each chain in the file
	chain_lines = dict()
	for id in chain_ids :
		chain_lines[id] = []

	#Parses the lines from "C3_lines" 
	for line in C3_lines :
		chain_lines[line[21]].append([line[17:20].replace(" ", ""), int(line[22:26].replace(" ", "")), float(line[30:38].replace(" ", "")), float(line[38:46].replace(" ", "")), float(line[46:54].replace(" ", ""))])
		
	#Dictionnary of interatomic distances for each chain in the file
	distances_by_chain = dict()
	for key, value in chain_lines.items() :
		distances_by_chain[key] = []
		for i in range(0,len(value)-1) :
			for j in range(1,len(value)) :
				#Residues of the two atoms ("A", "C", "T", "G")
				r1 = chain_lines[key][i][0][-1]
				r2 = chain_lines[key][j][0][-1]

				#Positions of the two atoms in the chain
				pos1 = chain_lines[key][i][1]
				pos2 = chain_lines[key][j][1]

				#Positions of the two atoms on the X axis
				x1 = chain_lines[key][i][2]
				x2 = chain_lines[key][j][2]

				#Positions of the two atoms on the Y axis
				y1 = chain_lines[key][i][3]
				y2 = chain_lines[key][j][3]

				#Positions of the two atoms on the Z axis
				z1 = chain_lines[key][i][4]
				z2 = chain_lines[key][j][4]
				
				#Calculates the interatomic distance using the X, Y and Z positions of the two atoms
				if ( (pos2 - pos1) >= 3) :
					distance = sqrt( ((x1-x2)**2) + ((y1-y2)**2) + ((z1-z2)**2) )
					distances_by_chain[key].append( [r1,r2,pos1,pos2,distance] )
				

	distances_by_pairs = dict()
	for key, value in distances_by_chain.items() :
		for l in value :
			pair = ""
			for r in sorted(l[:2]) :
				pair += r
				
			if not ("N" in [r for r in pair]):
				if not (pair in distances_by_pairs.keys()) :
					distances_by_pairs[pair] = []
			
			
				distances_by_pairs[pair].append(l[2:])
	
	for key, value in distances_by_pairs.items() :
		if not (key in distances_distribution_by_pairs.keys() ):
			distances_distribution_by_pairs[key] = dict()
		for l in value :
			if (round_down) :
				d = int(l[-1])
			else :
				d = l[-1]
			if (d >=0 and d <=20) :
				if not (d in distances_distribution_by_pairs[key].keys()) :
					distances_distribution_by_pairs[key][d] = 0
				distances_distribution_by_pairs[key][d] += 1
		
	#print(distances_distribution_by_pairs,"\n")
			
	return distances_distribution_by_pairs

def get_reference_distances_distribution(distances_distribution_by_pairs):

	"""Function calculating the distances distribution across all pairs of nucleosides from a dictionary by pairs

	Parameters
	----------
	distances_distribution_by_pairs
		Dictionary containing the dictionaries of the distribution of distances for each pair of nucleosides

	Returns
	-------
	reference_distances_distribution
		 Dictionary containing the distances distribution across all pairs of nucleosides
	"""

	reference_distances_distribution = dict()
	for distrib in distances_distribution_by_pairs.values():
		for d in distrib.keys():
			reference_distances_distribution[d] = 0
	for distribution in distances_distribution_by_pairs.values():
		for distance, count in distribution.items():
			reference_distances_distribution[distance] += count
	return reference_distances_distribution

def get_frequencies(distances_distribution : dict):

	"""Function calculating the distances frequencies for each pair of nucleosides from a dictionary of distance distribution by pairs

	Parameters
	----------
	distances_distribution_by_pairs
		Dictionary containing the dictionaries of the distribution of distances for each pair of nucleosides

	Returns
	-------
	reference_distances_distribution
		 Dictionary containing the distances frequencies for each pair of nucleosides
	"""

	N = sum(distances_distribution)
	distance_frequencies = dict()
	for key, value in distances_distribution.items() :
		distance_frequencies[key] = value / N
	return distance_frequencies

def get_scores(distance_frequencies_by_pairs : dict, reference_distance_frequencies : dict) :

	"""Function calculating the distance scores for each pair of nucleosides using a dictionary of distance frequencies by pairs and the reference one

	Parameters
	----------
	distance_frequencies_by_pairs
		Dictionary containing the dictionaries of the distribution of distances for each pair of nucleosides
	reference_distance_frequencies
		Dictionary containing the dictionaries of the frequencies of distances across all pairs of nucleosides

	Returns
	-------
	distance_scores_by_pairs
		 Dictionary containing the distance scores for each pair of nucleosides
	"""

	distance_scores_by_pairs = dict()
	for pair, distances in distance_frequencies_by_pairs.items():
		distance_scores_by_pairs[pair] = dict()
		for d in distances.keys():
			distance_scores_by_pairs[pair][d] = min(-(log(distance_frequencies_by_pairs[pair][d] / reference_distance_frequencies[d] )),10)

	return distance_scores_by_pairs


def save_distribs(path_distrib_dir : str,distribs_by_pairs : dict):

	"""Function saving the data produced in this script usin the save_to_csv function from Utility_script.py

	Parameters
	----------
	path_distrib_dir
		String containing the path to the directory where the files for each pairs of nucleotides that contain the data of the dictionary passed as a parameter must be saved
	distribs_by_pairs
		Dictionary containing the distributions, frequencies or scores that must be saved

	Returns
	-------
	None
	"""

	if ( not (os.path.isdir(path_distrib_dir))) :
		os.mkdir(path_distrib_dir)
	for key, value in distribs_by_pairs.items() :
		#print(os.path.join(path_distrib_dir,f"{path_distrib_dir.split('/')[-1]}_{key}.csv"))
		save_to_csv(os.path.join(path_distrib_dir,f"{path_distrib_dir.split('/')[-1]}_{key}.csv"),value)
	return


def main():

	""" Function called when this script is executed as a script and not imported as a library

    Parameters
    ----------
    None

    Returns
    -------
    None
    """

	plot_option = False
	path_data_dir = str(os.path.join(__file__, "data"))
	usage = "Usage :\npython [Path_to_Training.py] [-h, --help] [--plot] [Path_to_data_directory]\n\t[Path_to_Training.py] : Path to this training script \n\t[-h, --help] : Prints this help text \n\t[--plot] : Use if plots of the intermediary and scores distributions wanted \n\t[Path_to_data_directory] : Path to the data directory\n\t\tMust contain a directory containing pdb files"

	if (len(sys.argv) > 1):
		for i in range(len(sys.argv)):
			if (sys.argv[i] in ["-h","--help"]) :
				print(usage)
				return
			elif (sys.argv[i] == "--plot") :
				plot_option = True
			elif (os.path.exists(sys.argv[i])):
				if (os.path.isabs(sys.argv[i])) :
					path_data_dir = str(sys.argv[i])
				else:
					path_data_dir = str(os.path.join(os.getcwd(), sys.argv[i]))
			else:
				print(usage)
				return

	
	print(path_data_dir)

	if( not (os.path.exists(path_data_dir and os.path.isdir(path_data_dir)))):
		print("Data directory not found.")
		print(usage)
		return

	pdb_file_names = glob.glob(os.path.join(path_data_dir,"pdb*/*.pdb"))

	d = dict()
	for file in pdb_file_names :
		d = get_interatomic_distances_distribution_by_pairs(file,d)

	reference_distances_distribution = get_reference_distances_distribution(d)

	reference_distance_frequencies = get_frequencies(reference_distances_distribution)

	distance_frequencies_by_pairs = dict()

	for pair, distrib in d.items():
		distance_frequencies_by_pairs[pair] = get_frequencies(distrib)

	distance_scores_by_pairs = get_scores(distance_frequencies_by_pairs,reference_distance_frequencies)

	save_distribs(os.path.join(path_data_dir,"distribs"),d)
	save_distribs(os.path.join(path_data_dir,"frequencies"),{**distance_frequencies_by_pairs,**{"XX" : reference_distance_frequencies}})
	save_distribs(os.path.join(path_data_dir,"scores"),distance_scores_by_pairs)

	if (plot_option):

		plot_distrib_by_pairs(d, plot_name = "Distribution of distances by pairs")

		plot_distrib_by_pairs(distance_frequencies_by_pairs, plot_name = "Frequencies of distances by pairs")

		plot_distrib_by_pairs({"XX" : reference_distance_frequencies}, plot_name = "Reference distance frequencies")

		plot_distrib_by_pairs(distance_scores_by_pairs, plot_name = "Distribution of distance scores by pairs")

	return

#Call the main function when this script is executed as a script and not imported as a library
if __name__ == "__main__" :
	main()
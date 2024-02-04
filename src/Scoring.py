import os, sys, glob
from Utility_script import import_from_csv
from Training import get_interatomic_distances_distribution_by_pairs
from math import ceil, floor

def linear_interpolation(x,x0,y0,x1,y1):
    return ( (y0 * (x1 - x)) + (y1 * (x - x0)) ) / (x1 - x0)

def get_estimated_energy(input_scores_distrib,distance_scores_by_pairs):
    scores = []
    for pair, distrib in input_scores_distrib.items():
        for distance, nb in distrib.items() :
            x0 = floor(distance)
            while (not(x0 in distance_scores_by_pairs[pair].keys()) and x0 > 0):
                x0 -= 1
            x1 = ceil(distance)
            while (not(x1 in distance_scores_by_pairs[pair].keys()) and x1 < 20):
                x1 += 1

            scores.append( linear_interpolation(distance, x0, distance_scores_by_pairs[pair][x0], x1, distance_scores_by_pairs[pair][x1]) * nb )
    return sum( scores )

def main():

    path_data_dir = str(os.path.join(__file__, "data"))
    usage = "Usage :\npython [Path_to_Scoring.py] [-h, --help] [Path_to_data_directory]\n\t[Path_to_Scoring.py] : Path to this scoring script \n\t[-h, --help] : Prints this help text \n\t[Path_to_data_directory] : Path to the data directory\n\t\tMust contain a directory containing the score csv files and another containing only the input pdb file"

    if (len(sys.argv) > 1):
        for i in range(len(sys.argv)):
            if (sys.argv[i] in ["-h","--help"]) :
                print(usage)
                return
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

    scores_file_names = glob.glob(os.path.join(path_data_dir,"*/scores*.csv"))

    distance_scores_by_pairs = dict()
    for file_path in scores_file_names :

        #print(file_path)
        dict_scores = dict()
        distance_scores_by_pairs[os.path.splitext(os.path.basename(file_path))[0].split("_")[-1]] = import_from_csv(file_path,dict_scores)

        #print(distance_scores_by_pairs)

    input_path = glob.glob(os.path.join(path_data_dir,"input/*.pdb"))[0]

    input_scores_distrib = get_interatomic_distances_distribution_by_pairs(input_path,round_down= False)

    estimated_gibbs_free_energy = get_estimated_energy(input_scores_distrib,distance_scores_by_pairs)
	
    print(f"Estimated Gibbs free energy for {os.path.splitext(os.path.basename(input_path))[0]} : {estimated_gibbs_free_energy}")

    return


if __name__ == "__main__" :
	main()
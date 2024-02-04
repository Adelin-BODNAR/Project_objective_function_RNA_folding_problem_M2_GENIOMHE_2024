import os, sys, glob
from Utility_script import import_from_csv
from Training import get_interatomic_distances_distribution_by_pairs
from math import ceil, floor

def linear_interpolation(x,x0,y0,x1,y1):
    
    """ Function performing a linear interpolation

    Parameters
    ----------
    x
        The x value for which the y value must be calculated by linear interpolation
    x0 , y0
        Coordinates of the lower point used in the linear interpolation
    x1 , y1
        Coordinates of the higher point used in the linear interpolation

    Returns
    -------
    y
        Result of the linear interpolation formula performed with the data passed in arguments
    """

    return ( (y0 * (x1 - x)) + (y1 * (x - x0)) ) / (x1 - x0)

def get_estimated_energy(input_distances_distrib,distance_scores_by_pairs):

    """ Function calculating the estimated Gibbs free energy using the data passed as arguments

    Parameters
    ----------
    input_distances_distrib
        Dictionary containing the distribution of distances between 1 and 20 included and not rounded down
    distance_scores_by_pairs
        Dictionary of the distribution of scores for distances between 1 and 20 included and rounded down for each pair of nucleosides
        This dictionary is used as reference scores for the linear interpolation of the scores for the input distances

    Returns
    -------
    sum(scores)
        The estimated Gibbs free energy which is the sum of the scores calculated by linear interpolation for the input distances
    """

    scores = []
    for pair, distrib in input_distances_distrib.items():
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

    """ Function called when this script is executed as a script and not imported as a library

    Parameters
    ----------
    None

    Returns
    -------
    None
    """

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

    input_distances_distrib = get_interatomic_distances_distribution_by_pairs(input_path,round_down= False)

    estimated_gibbs_free_energy = get_estimated_energy(input_distances_distrib,distance_scores_by_pairs)
	
    print(f"Estimated Gibbs free energy for {os.path.splitext(os.path.basename(input_path))[0]} : {estimated_gibbs_free_energy}")

    return

#Call the main function when this script is executed as a script and not imported as a library
if __name__ == "__main__" :
	main()
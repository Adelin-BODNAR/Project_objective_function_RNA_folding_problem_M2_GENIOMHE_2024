import matplotlib.pyplot as plt
from math import ceil
from Utility_script import import_from_csv
import os, sys, glob

def plot_distrib(fig,distances_distribution, pair = "XX",nb_ax = 0):
	
    ax =fig.axes[nb_ax]
    ax.bar(distances_distribution.keys(),distances_distribution.values())
    ax.axis([0 , 20 + 1, min(distances_distribution.values()), max(distances_distribution.values()) * 1.1])
    ax.set_title(pair)
    
    return

def plot_distrib_by_pairs(distances_distribution_by_pairs, plot_name = "Distribution") :
	
    #print(distances_distribution_by_pairs,"\n")

    nb_rows = min(2,len(distances_distribution_by_pairs.keys()))
    nb_cols = ceil(len(distances_distribution_by_pairs.keys())/nb_rows)

    fig, axs = plt.subplots(nrows= nb_rows, ncols= nb_cols, figsize=(16, 8))

    plt.subplots_adjust(hspace=0.5,wspace=0.7)
    fig.suptitle(plot_name)

    for i,(key, value) in enumerate(distances_distribution_by_pairs.items()) :
        plot_distrib(fig,value,key,nb_ax =i)
    
    plt.show()

    return

def plot_score_function(fig,scores, pair = "XX",nb_ax = 0):
	
    ax =fig.axes[nb_ax]
    ax.plot([ int(d) for d in scores.keys()], [float(v) for v in scores.values()])
    ax.set_title(pair)
	
    return

def plot_score_functions_by_pairs(scores_by_pairs):
	
    #print(scores_by_pairs,"\n")

    nb_rows = min(2,len(scores_by_pairs.keys()))
    nb_cols = ceil(len(scores_by_pairs.keys())/nb_rows)

    fig, axs = plt.subplots(nrows= nb_rows, ncols= nb_cols, figsize=(16, 8))

    plt.subplots_adjust(hspace=0.5,wspace=0.3)
    fig.suptitle("Scores functions")

    for i,(key, value) in enumerate(scores_by_pairs.items()) :
        plot_score_function(fig,value,key,nb_ax =i)
    
    plt.show()

    return

def main():

    path_data_dir = str(os.path.join(__file__, "data"))
    usage = "Usage :\npython [Path_to_Plotting.py] [-h, --help] [Path_to_data_directory]\n\t[Path_to_Plotting.py] : Path to this plotting script \n\t[-h, --help] : Prints this help text \n\t[Path_to_data_directory] : Path to the data directory\n\t\tMust contain a directory containing the score csv files"

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

    plot_score_functions_by_pairs(distance_scores_by_pairs)
	

    return


if __name__ == "__main__" :
	main()
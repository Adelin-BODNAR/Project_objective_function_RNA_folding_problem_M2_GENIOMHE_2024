def save_to_csv(path : str, data : dict):

	"""Saves a directory distribution produced in the Training.py file to a csv file
	
	Parameters
	----------
	path : str
		String containing path to the file where the data must be saved
	data : dict
		Dictionary containing the data that must be saved
		This functionned is specifically designed for a dictionary with keys ranging from 1 to 20 included

	Returns
	-------
		None
	"""

	with open(path,"w") as file:
		for d in range(1,21):
			if d in data: 
				#Writes the data for the keys existing in the dictionary
				file.write(f"{d},{data[d]}\n")
			else :
				#Writes the data for the keys between 1 and 20 included to get 20 lines in the file
				file.write(f"{d},0\n")
	return

def import_from_csv(file_path : str,imported_data : dict):
	
	""" Imports the data from a csv file with the same format as the ones created by the function save_to_csv
	
	Parameters
	----------
	file_path : str
		String containing the path to the file containing the data that must be imported

	imported_data : dict
		Dictionary where the data must be imported to

	Returns
	-------
	imported_data : dict
		Dictionary where the function imported the data to
	"""

	with open(file_path,"r") as file :
			for line in file.readlines() :
				distance, score = line.split(",")
				imported_data[int(distance)] = float(score)

	##Prints used for debugging
	#print(file_path)
	#print(imported_data)

	return imported_data
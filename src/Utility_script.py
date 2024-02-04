def save_to_csv(path : str, data : dict):
	with open(path,"w") as file:
		for d in range(1,21):
			if d in data: 
				file.write(f"{d},{data[d]}\n")
			else :
				file.write(f"{d},0\n")
	return

def import_from_csv(file_path,imported_data = dict()):
	
	with open(file_path,"r") as file :
			for line in file.readlines() :
				distance, score = line.split(",")
				imported_data[int(distance)] = float(score)

	#print(file_path)
	#print(imported_data)

	return imported_data
import os
import requests
files_list = [os.path.join(root, fname) for root, sub, files in os.walk(r"/home/anastasia/Загрузки/example/") for fname in files]

for f in files_list:
		data = open(f, 'r')
		s = ""
		for d in data:
			s+=d
		SN = f.split(".")[0].split('/')[-1]
		filename = f.split("/")[-1]
		response = requests.post('http://localhost:5000/'+ SN + '/'+filename, data=s)
		print(response)

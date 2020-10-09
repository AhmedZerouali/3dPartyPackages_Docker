import os
import subprocess
import multiprocessing as mp
import pandas as pd


commands = [
"docker stop $(docker ps -a -q)", 
"docker rm $(docker ps -a -q)",
"docker volume rm $(docker volume ls -qf dangling=true)",
"docker rmi -f $(docker images  | grep '/' | awk '{print $3}')"
#"docker rmi -f $(docker images  | grep -v ^'debian ' | awk '{print $3}')"
]

def clean_docker():
	for cmd in commands:
		print(cmd)
		try:
			subprocess.check_call(cmd, stdout=subprocess.DEVNULL, shell=True)
		except:
			continue
		#p.wait()
		print('Finished process')

def download(tab):
	"""Pulls and runs the Docker images-f
	"""
	image = tab[0]+':latest'
	base = tab[1]
	
	os.system('docker pull '+image)
	get_os(image)
	get_packages(image, base)

def get_os(image):

	os.system("docker run --entrypoint '/bin/bash' " + image + " -c 'cat /etc/issue' > /home/ahmed/libraries_docker/pulled/os/"+ image.replace('/',':')+"_r1")
	os.system("docker run --entrypoint '/bin/bash' " + image + " -c 'cat /etc/os-release' > /home/ahmed/libraries_docker/pulled/os/"+ image.replace('/',':')+"_r2")

def get_packages(image, base):

	if base == 'node':
		os.system("docker run --entrypoint '/bin/bash' " + image + " -c 'npm list -g' > /home/ahmed/libraries_docker/pulled/packages/node/"+ image.replace('/',':'))

	elif base == 'python':
		os.system("docker run --entrypoint '/bin/bash' " + image + " -c 'pip2 freeze' > /home/ahmed/libraries_docker/pulled/packages/python/"+ image.replace('/',':')+"_2")
		os.system("docker run --entrypoint '/bin/bash' " + image + " -c 'pip3 freeze' > /home/ahmed/libraries_docker/pulled/packages/python/"+ image.replace('/',':')+"_3")

	else:
		os.system("docker run --entrypoint '/bin/bash' " + image + " -c 'gem list' > /home/ahmed/libraries_docker/pulled/packages/ruby/"+ image.replace('/',':'))


def main():
	images = pd.read_csv('../../libraries_docker/csv/to_pull.csv', dtype=object)
	candidates = []
	for row in images.iterrows():
		image = row[1]['image']
		base = row[1]['base']
		candidates.append([image, base])

	for i in range(0,33): #3077
		print('Moving to the iteration number '+str(i))	
		try:
			print(i)
			pool= mp.Pool(processes=14)
			#results=pool.imap_unordered(download,images[i*100:(i+1)*100], 6)
			results=pool.imap_unordered(download,candidates[0:2], 1)
			pool.close()
			pool.join()

			#clean_docker()

		except:
			break

		break

if __name__ == "__main__":
	#clean_docker()
	main()

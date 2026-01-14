import numpy as np
import os
import urllib.request
import sys
import shutil
import time
import argparse

#working directory path
#workdir=os.getcwd()+"/"
def cavity (n,workdir,s):
	lista = ["%05d" % (x+s) for x in range(n-s+1)]
	for i in range(len(lista)):
		dat="FRAME_"+lista[i]
		with open(workdir+"/"+dat+"_out/"+dat+"_out.pdb","r") as f:
			Fe=[]
			NA=[]
			NB=[]
			big_lista=[] #big list with x,y,z coordinates of each sphere+number of sphere
			for line in f:
				linespl=line.split()
				small_lista=[] #small list where each sphere is separated, to be put in big one
				if ((linespl[3]=="HEMOA" or linespl[3]=="HEMO") and (linespl[11]=="Fe" or linespl[11]=="FE" or linespl[2]=="FE")):
					Fe.append(linespl[5])
					Fe.append(linespl[6])
					Fe.append(linespl[7])
			#conditions so it can read file from database but also normal ones from PDB
				if ((linespl[3]=="HEMOA" or linespl[3]=="HEMO") and (linespl[2]=="NA" or linespl[2]=="N1")):
					NA.append(linespl[5])
					NA.append(linespl[6])
					NA.append(linespl[7])
				if ((linespl[3]=="HEMOA" or linespl[3]=="HEMO") and (linespl[2]=="NB" or linespl[2]=="N2")):
					NB.append(linespl[5])
					NB.append(linespl[6])
					NB.append(linespl[7])
				if (len(linespl)==11):
					if (linespl[10]=="Ve"):
						small_lista.append(linespl[5])
						small_lista.append(linespl[6])
						small_lista.append(linespl[7])
						small_lista.append(linespl[4])
						big_lista.append(small_lista)
				if (len(linespl)==12):
					if (linespl[11]=="Ve"):
						small_lista.append(linespl[6])
						small_lista.append(linespl[7])
						small_lista.append(linespl[8])
						small_lista.append(linespl[5])
						big_lista.append(small_lista)
			FeNA=[(float(NA[0])-float(Fe[0])),(float(NA[1])-float(Fe[1])),(float(NA[2])-float(Fe[2]))]
			FeNB=[(float(NB[0])-float(Fe[0])),(float(NB[1])-float(Fe[1])),(float(NB[2])-float(Fe[2]))]
			n=np.cross(FeNA,FeNB)
			smallest_num=100000
			FeS=[]
			for sfera in big_lista:
				#dot product to see from which side of heme the sphere is
				FeS=[(float(sfera[0])-float(Fe[0])),(float(sfera[1])-float(Fe[1])),(float(sfera[2])-float(Fe[2]))]
				sk=np.dot(n,FeS)
				#if it is above, then calculate the distance, if it is the smallest one so far remember the number of sphere
				if (sk>0):
						d=np.sqrt(np.square(float(sfera[0])-float(Fe[0]))+np.square(float(sfera[1])-float(Fe[1]))+np.square(float(sfera[2])-float(Fe[2])))
						if (d<smallest_num):
							smallest_num=d
							sf=sfera[3]
			print (dat, sf)
		#taking volume and proportion of apolar alpha spheres from the selected pocket
		#print (str(workdir)+str(dat)+"_out/pockets/pocket"+str(sf)+"_vert.pqr")
		with open(workdir+"/"+dat+"_out/"+dat+"_info.txt","r") as f:
			pocket=False
			alpha=0.
			vol=0.
			sasa=0.
			apolar_sasa=0.
			
			for line in f:
				line = line.strip()
				linespl=line.split()
				if (linespl!=[]):
					if (linespl[0]=="Pocket" and linespl[1]==str(sf)):
						pocket=True
				#properties go by the order how they are listen in the txt file, otherwise break breaks it and we get 0 values for some
				if (pocket==True):
					if (linespl!=[]):
						if (linespl[0]=="Total" and linespl[1]=="SASA"):
							sasa=float(linespl[3])
						if (linespl[0]=="Apolar" and linespl[1]=="SASA"):
							apolar_sasa=float(linespl[3])
						if (linespl[0]=="Volume"):
							vol=float(linespl[2])
						if (linespl[0]=="Apolar" and linespl[1]=="alpha"):
							alpha=float(linespl[5])
							break
		#append name, volume and alpha sphere proportion and sasa in fpocket.txt to have them in one place
		with open(workdir+"/"+"fpocket_sasa.txt","a") as f:
			f.write("\n"+str(dat)+" "+str(vol)+" "+str(alpha)+" "+str(sasa)+" "+str(apolar_sasa)+" "+str(sf))

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="script")
	parser.add_argument('-n','--number', type=int, required=True, help="Range in ")   
	parser.add_argument('-wd','--working_dir', type=str, required=True,help="WORKDIR from bash script")    
	parser.add_argument('-s','--start', type=int, required=False, help="Start snapshot number")

	args=parser.parse_args()
	if args.start is None:
		cavity(args.number,args.working_dir,s=1)
	else:
		cavity(args.number,args.working_dir,args.start)

	

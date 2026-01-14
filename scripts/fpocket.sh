#!/bin/bash

#SBATCH --time=4-00:00:00 
#SBATCH --partition COM 
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=4096 
#SBATCH --export=ALL 

'''
The script finds the folder where the wanted snapshots are. They should be .pdb files, and named FRAME_00001,...,FRAME_$range.
The script runs fpocket with the parameters -m 2.9 -M 16.0 -i 30 on each of these snapshots. It writes out the volume, apolar alpha sphere ratio and sasa
for each snapshot in fpocket.txt file, using the fpocket_ana.py python script. In the end, all the fpocket output folders are put into fpocket.zip and copied to the original directory where the 
pdb files were taken from. The fpocket.txt file is copied as well. It is much faster as writing time on scratch is much shorter than the writing time 
on pool.
Called in such a way: sbatch /pool/teakuvek/CYPs/zenodo_data/scripts/fpocket.sh /folder_with_snapshots number_of_snapshots
'''

  
SIMULDIR="$1"
range="$2"
echo "Checking if fpocket_sasa.txt already exists."
if [ -e "${SIMULDIR}/fpocket_sasa.txt" ]; then
    echo "fpocket_sasa.txt already exists in ${SIMULDIR}. Script will now exit."
    exit 1
fi

WORKDIR=/scratch/${SLURM_JOBID}
mkdir -p ${WORKDIR}
echo "Running fpocket for $range snapshots."
echo "Running fpocket for: $SIMULDIR, working directory: $WORKDIR"
for (( num=1; num<=${range}; num++ )); do
	cd "$SIMULDIR"
	printf -v padded_num "%05d" "$num"
	echo  "FRAME_$padded_num inspection..."
	directory=FRAME_${padded_num}_out

	#check if the fpocket output for a certain frame already exists, if yes skip it, if no run it

#	if [ -d "$directory" ]; then
#    		echo "Directory '$directory' exists."
#    	else
	cd "$WORKDIR"
	cp ${SIMULDIR}/FRAME_${padded_num}.pdb .
    	fpocket -f FRAME_${padded_num}.pdb -m 2.9 -M 16.0 -i 30
#	fi
done

#zip up all the files that fpocket fpocket folders that were made and copy them to the simuldir

cd "$WORKDIR"
python3 /pool/teakuvek/CYPs/zenodo_data/scripts/fpocket_ana.py -n ${range} -w $WORKDIR
zip -r fpocket.zip *_out*
cp fpocket.zip ${SIMULDIR}/.
cp fpocket_sasa.txt ${SIMULDIR}/.
#remove the working directory

rm -r ${WORKDIR}
    	

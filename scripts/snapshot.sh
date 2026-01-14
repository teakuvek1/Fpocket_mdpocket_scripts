#!/bin/bash

#First gmx trjconv needs to be with a generated local md.tpr
#All needs to be fitted to the same structure (FRAME_00001.pdb)
#Provide the name of .tpr file in input

#gmx grompp -c eq_cyp_5.gro -f md.mdp -p ../../../topo/gmx/"$2"_gmx.top -o md_local.tpr -n index.ndx -maxwarn 2

#mkdir frames
#cd frames
echo '22' | gmx trjconv -s ../../../../coord/FRAME_00001.pdb -f ../reduced_fit.xtc -o FRAME_.pdb -sep -n ../index.ndx
bash /pool/teakuvek/CYPs/zenodo_data/scripts/renaming.sh





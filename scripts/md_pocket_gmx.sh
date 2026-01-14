#!/bin/bash
#First make a gmx fpolder inside of mdpocket_all_together folder, which is in md folder
cp ../../repl1/gmx/reduced_fit.xtc 1.xtc
cp ../../repl2/gmx/reduced_fit.xtc 2.xtc
cp ../../repl3/gmx/reduced_fit.xtc 3.xtc
cp ../../repl4/gmx/reduced_fit.xtc 4.xtc
cp ../../repl5/gmx/reduced_fit.xtc 5.xtc
#Cat needs to be there so they can join together, as they have same starting and ending time they overwrite each other otherwise
echo '22' | gmx trjcat -f 1.xtc 2.xtc 3.xtc 4.xtc 5.xtc -o md_cili.xtc -n ../../repl1/gmx/index.ndx -cat
#Here mind the tpr file name
echo -e '22\n22' | gmx trjconv -s ../../../coord/FRAME_00001.pdb -f md_cili.xtc -n ../../repl1/gmx/index.ndx -fit rot+trans -o md_cili_aligned.xtc
rm 1.xtc 2.xtc 3.xtc 4.xtc 5.xtc md_cili.xtc
cp ../../../coord/FRAME_00001.pdb 1_bez_iona.pdb
mdpocket -f 1_bez_iona.pdb --trajectory_file md_cili_aligned.xtc --trajectory_format xtc -m 2.9 -M 16.0



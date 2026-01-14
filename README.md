# Fpocket_mdpocket_scripts

*MD simulation files*

Directories human_cyps and plant_cyps contain all the files needed to reproduce the Md ismulation trajectories. Each CYP has 7 directories, starting from topology and ending with md. They have a prefix number which says in which order they are to be used. Ion topologies, mtb, ifp and library files can be found in folder files.
Useful info:
- for each system, you can find three gromos topologies:
	- cyp.top corresponds to topology where heme is not bound to the protein
	- cyp_heme.top corresponds to the topology where heme is bound to the CYS
	- CYP90D1.top (for example) corresponds to the protein with bound heme and with Na and Cl ions
- equilibration is done with gromos
- md is done with gromacs

*Pocket analysis scripts*

- mdpocket:
	- md_pocket_gmx.sh concatanates the created replicates for a certain CYP, aligns them on a reference structure and runs mdpocket
- fpocket:
	- snapshot.sh extacts the snapshot from the simulation (renaming.sh names them from 1 to 12500, so it fits the rest of analysis)
	- fpocket.sh runs fpocket on each snapshot (fpocket_ana.py checks for the cavity above the heme and extracts wanted properties from the output)
- binding properties generation:
	- Properties.ipynb plots and calculates the Volume, Volume range, shape and hydrophobicity of the binding pocket for each snapshot for the chosen pocket description between mdpocket and fpocket

## Authors and acknowledgment
Made by Tea Kuvek


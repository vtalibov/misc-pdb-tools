#!/bin/bash

# Directory containing the files
directory="test"

for pdb_file in "$directory"/*.pdb; do
    ligand_file="${pdb_file%.*}_ligand.pdb"
    if [ -f "$ligand_file" ]; then
        # think how to do it with mktemp
        obabel -ipdb "$ligand_file" -osdf - | obabel -i sdf -opdb -O "$ligand_file".temp
        python pdb_bulkrplresname.py -INH "$ligand_file".temp > "$ligand_file".temp2
        protein_file_name="${ligand_file%_ligand.pdb}"
        python pdb_merge.py "$protein_file_name".pdb "$ligand_file".temp2 > "$protein_file_name"_merged.pdb 
        rm "$ligand_file".temp*
    fi
done
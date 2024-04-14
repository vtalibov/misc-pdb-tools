#!/bin/bash

# Directory containing the files
directory="$1"

for protein_file in "$directory"/*.pdb; do
    ligand_file="${protein_file%.*}_ligand.pdb"
    if [ -f "$ligand_file" ]; then # checks if file_ligand.pdb exists
        if [ ! -d "$directory/merged" ]; then
            mkdir -p "$directory/merged"
            echo "Directory $directory/merged created."
        fi
        # think how to do it with mktemp; python does not work without temp files
        obabel -ipdb "$ligand_file" -osdf - | obabel -i sdf -opdb -O "$ligand_file".temp
        python pdb_bulkrplresname.py -INH "$ligand_file".temp > "$ligand_file".temp2
        python pdb_merge.py "$protein_file" "$ligand_file".temp2 > "${protein_file%.*}_merged.pdb" 
        protein_file_name=$(basename "$protein_file")
        echo "Models for ${protein_file_name%.*} were merged." 
        # comment lines below before rm command to keep merged file as
        # _merged.pdb in the folder with structures
        mv "${protein_file%.*}_merged.pdb" "$directory/merged/$protein_file_name"
        rm "$ligand_file".temp*
    fi
done
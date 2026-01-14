#!/bin/bash


# Loop through files and rename them
for i in {1..10000}; do
    old_name="FRAME_$i.pdb"
    new_name="FRAME_$(printf "%05d" $i).pdb"
    mv "$old_name" "$new_name"
done


#!/bin/sh

# Assumptions:
# This file is in a top level folder where you python model is
# You have a subfolder with the 9 scenario input files
# The 9 scenario input files are called modelName_treeComposition
# In the 9 scenario input files you specify that the output should go into
# model_output/modelName_treeComposition

for i in {1..2}; do
    echo "Running repetition $i"
    # Step 1: run models -> Emma, replace everything until step 2 this with your python commands
    # for the 9 input files, here I just create a dummy folder in model_output
    # that gets renamed in step 2 according to the current repetition
    echo "FS, 1A"
    py ./MANGA.py -i model_final_Emma/ctrl_files/FS_1_A.xml
    echo "FS, 1R"
    py ./MANGA.py -i model_final_Emma/ctrl_files/FS_1_R.xml
    echo "FS, 1AR"
    py ./MANGA.py -i model_final_Emma/ctrl_files/FS_1_AR.xml
    echo "FS, 2A"
    py ./MANGA.py -i model_final_Emma/ctrl_files/FS_2_A.xml
    echo "FS, 2R"
    py ./MANGA.py -i model_final_Emma/ctrl_files/FS_2_R.xml
    echo "FS, 2AR"
    py ./MANGA.py -i model_final_Emma/ctrl_files/FS_2_AR.xml
    echo "FS, 3A"
    py ./MANGA.py -i model_final_Emma/ctrl_files/FS_3_A.xml
    echo "FS, 3R"
    py ./MANGA.py -i model_final_Emma/ctrl_files/FS_3_R.xml
    echo "FS, 3AR"
    py ./MANGA.py -i model_final_Emma/ctrl_files/FS_3_AR.xml
    echo "ZOI, A"
    py ./MANGA.py -i model_final_Emma/ctrl_files/SZOI_A.xml
    echo "ZOI, R"
    py ./MANGA.py -i model_final_Emma/ctrl_files/SZOI_R.xml
    echo "ZOI, AR"
    py ./MANGA.py -i model_final_Emma/ctrl_files/SZOI_AR.xml
#    py ./MANGA.py -i model_final_Emma/ctrl_files/SZOIFS_1_A.xml
#    py ./MANGA.py -i model_final_Emma/ctrl_files/SZOIFS_1_R.xml
#    py ./MANGA.py -i model_final_Emma/ctrl_files/SZOIFS_1_AR.xml
#    py ./MANGA.py -i model_final_Emma/ctrl_files/SZOIFS_2_A.xml
#    py ./MANGA.py -i model_final_Emma/ctrl_files/SZOIFS_2_R.xml
#    py ./MANGA.py -i model_final_Emma/ctrl_files/SZOIFS_2_AR.xml
#    py ./MANGA.py -i model_final_Emma/ctrl_files/SZOIFS_3_A.xml
#    py ./MANGA.py -i model_final_Emma/ctrl_files/SZOIFS_3_R.xml
#    py ./MANGA.py -i model_final_Emma/ctrl_files/SZOIFS_3_AR.xml
    echo "FON, A"
    py ./MANGA.py -i model_final_Emma/ctrl_files/FON_A.xml
    echo "FON, R"
    py ./MANGA.py -i model_final_Emma/ctrl_files/FON_R.xml
    echo "FON, AR"
    py ./MANGA.py -i model_final_Emma/ctrl_files/FON_AR.xml
#    py ./MANGA.py -i model_final_Emma/ctrl_files/FONFS_1_A.xml
#    py ./MANGA.py -i model_final_Emma/ctrl_files/FONFS_1_R.xml
#    py ./MANGA.py -i model_final_Emma/ctrl_files/FONFS_1_AR.xml
#    py ./MANGA.py -i model_final_Emma/ctrl_files/FONFS_2_A.xml
#    py ./MANGA.py -i model_final_Emma/ctrl_files/FONFS_2_R.xml
#    py ./MANGA.py -i model_final_Emma/ctrl_files/FONFS_2_AR.xml
#    py ./MANGA.py -i model_final_Emma/ctrl_files/FONFS_3_A.xml
#    py ./MANGA.py -i model_final_Emma/ctrl_files/FONFS_3_R.xml
#    py ./MANGA.py -i model_final_Emma/ctrl_files/FONFS_3_AR.xml


    # Step 2: Add the number of the repetition to the folder name
    mv previous_setups/model_output/FS_1_A "previous_setups/model_output/FS-1_A_$i"
    echo "previous_setups/model_output/FS-1_A_$i"
    mv previous_setups/model_output/FS_1_R "previous_setups/model_output/FS-1_R_$i"
    mv previous_setups/model_output/FS_1_AR "previous_setups/model_output/FS-1_AR_$i"
    mv previous_setups/model_output/FS_2_A "previous_setups/model_output/FS-2_A_$i"
    mv previous_setups/model_output/FS_2_R "previous_setups/model_output/FS-2_R_$i"
    mv previous_setups/model_output/FS_2_AR "previous_setups/model_output/FS-2_AR_$i"
    mv previous_setups/model_output/FS_3_A "previous_setups/model_output/FS-3_A_$i"
    mv previous_setups/model_output/FS_3_R "previous_setups/model_output/FS-3_R_$i"
    mv previous_setups/model_output/FS_3_AR "previous_setups/model_output/FS-3_AR_$i"
    mv previous_setups/model_output/SZOI_A "previous_setups/model_output/SZOI_A_$i"
    mv previous_setups/model_output/SZOI_R "previous_setups/model_output/SZOI_R_$i"
    mv previous_setups/model_output/SZOI_AR "previous_setups/model_output/SZOI_AR_$i"
#    mv previous_setups/model_output/SZOIFS_1_A "previous_setups/model_output/SZOIFS_1_A_$i"
#    mv previous_setups/model_output/SZOIFS_1_R "previous_setups/model_output/SZOIFS_1_R_$i"
#    mv previous_setups/model_output/SZOIFS_1_AR "previous_setups/model_output/SZOIFS_1_AR_$i"
#    mv previous_setups/model_output/SZOIFS_2_A "previous_setups/model_output/SZOIFS_2_A_$i"
#    mv previous_setups/model_output/SZOIFS_2_R "previous_setups/model_output/SZOIFS_2_R_$i"
#    mv previous_setups/model_output/SZOIFS_2_AR "previous_setups/model_output/SZOIFS_2_AR_$i"
#    mv previous_setups/model_output/SZOIFS_3_A "previous_setups/model_output/SZOIFS_3_A_$i"
#    mv previous_setups/model_output/SZOIFS_3_R "previous_setups/model_output/SZOIFS_3_R_$i"
#    mv previous_setups/model_output/SZOIFS_3_AR "previous_setups/model_output/SZOIFS_3_AR_$i"
    mv previous_setups/model_output/FON_A "previous_setups/model_output/FON_A_$i"
    mv previous_setups/model_output/FON_R "previous_setups/model_output/FON_R_$i"
    mv previous_setups/model_output/FON_AR "previous_setups/model_output/FON_AR_$i"
#    mv previous_setups/model_output/FONFS_1_A "previous_setups/model_output/FONFS_1_A_$i"
#    mv previous_setups/model_output/FONFS_1_R "previous_setups/model_output/FONFS_1_R_$i"
#    mv previous_setups/model_output/FONFS_1_AR "previous_setups/model_output/FONFS_1_AR_$i"
#    mv previous_setups/model_output/FONFS_2_A "previous_setups/model_output/FONFS_2_A_$i"
#    mv previous_setups/model_output/FONFS_2_R "previous_setups/model_output/FONFS_2_R_$i"
#    mv previous_setups/model_output/FONFS_2_AR "previous_setups/model_output/FONFS_2_AR_$i"
#    mv previous_setups/model_output/FONFS_3_A "previous_setups/model_output/FONFS_3_A_$i"
#    mv previous_setups/model_output/FONFS_3_R "previous_setups/model_output/FONFS_3_R_$i"
#    mv previous_setups/model_output/FONFS_3_AR "previous_setups/model_output/FONFS_3_AR_$i"
done

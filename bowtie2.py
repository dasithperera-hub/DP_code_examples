#this script is used to run bowtie2 on multiple paired-end FASTQ files in the same directory
#It assumes that the paired files are named in the format "ConditionX_y_R1.fastq" and "ConditionX_y_R2.fastq"
#it assumes that the index is named "hpara" 
#It will run bowtie2 for each pair of files and output a SAM file with the same name as the condition


import glob
import os

# Get all FASTQ files in directory
fastq_files = sorted(glob.glob("*.fastq"))

# create a dictionary to store file pairs based on their sample name (eg. DP1, DP2, DP3)
paired_reads = {}

# Categorize files into pairs based on sample name
for file in fastq_files:
    condition = file.split("_R")[0]  
    if condition not in paired_reads:
        paired_reads[condition] = {"R1": None, "R2": None}

    if "_R1.fastq" in file:
        paired_reads[condition]["R1"] = file
    elif "_R2.fastq" in file:
        paired_reads[condition]["R2"] = file

# Run bowtie2 for each matched pair, hpara is the index name. checking for presence of both R1 and R2 files
for condition, files in paired_reads.items():
    r1, r2 = files["R1"], files["R2"]
    if r1 and r2:  
        output_sam = f"{condition}_SAMPLES.sam"
        command = f"bowtie2 -x hpara -1 {r1} -2 {r2} -S {output_sam}"
        print(f"Running: {command}")
        os.system(command)  
    else:
        print(f"Warning: Missing R1 or R2 for {condition}")
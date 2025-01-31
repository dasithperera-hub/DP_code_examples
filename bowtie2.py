#this script was used to run bowtie2 on multiple paired-end FASTQ files in the same directory
#It assumes that the paired files are named in the format "ConditionX_y_R1.fastq" and "ConditionX_y_R2.fastq"
#it assumes that the index is named "hpara". see line 33
#It will run bowtie2 for each pair of files and output a SAM file with the same name based on information upstream of _R


import glob
import os

# Get all FASTQ files in directory
fastq_files = sorted(glob.glob("*.fastq"))

# create a dictionary to store file pairs based on their sample info
paired_reads = {}

# Categorize files into pairs based on information upstream of _R i.e. the condition
for file in fastq_files:
    condition = file.split("_R")[0]  
    #check if already present and assigning empty R1 and R2 keys 
    if condition not in paired_reads:
        paired_reads[condition] = {"R1": None, "R2": None}
#Look for R1 and R2 for each paired file
    if "_R1.fastq" in file:
        paired_reads[condition]["R1"] = file
    elif "_R2.fastq" in file:
        paired_reads[condition]["R2"] = file

# Run bowtie2 for each matched pair, hpara is the index name. Output error if file pair is missing
for condition, files in paired_reads.items():
    r1, r2 = files["R1"], files["R2"]
    if r1 and r2:  
        output_sam = f"{condition}_SAMPLES.sam"
        command = f"bowtie2 -x hpara -1 {r1} -2 {r2} -S {output_sam}"
        print(f"Running: {command}")
        os.system(command)  
    else:
        print(f"Warning: Missing R1 or R2 for {condition}")

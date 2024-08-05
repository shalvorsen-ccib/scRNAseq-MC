############### Prerequisites, Installation, and Output #######################
This read processing pipeline depends on both python and common shell commands included with most operating systems. It should be compatible with most *nix systems, but has been tested only on RHEL and MacOS operating systems. It should be compatible with most versions of python3, but has been tested only with python version 3.5.1 and 3.9.2. These scripts might not work on windows systems due to the differences in shell commands and directory nomenclature. While the resulting read format should be compatible with all versions of StarSOLO, the read files have only been tested to be compatible with StarSOLO version 2.7.3a.

Software installation is not needed if running these scripts directly. In order to call these scripts from a different directory without specifying the absolute script path, you will need to add the script locations to your path variable. For the sample dataset, the expected runtime is only a few seconds. An intermediate output will be a set of 24 temporary files in the inDrops_2read folder. The final output will be in the inDrops_merged folder. There will be 12 files, corresponding to 6 libraries (R1 and R2 for each library).


############### Quick-start Command List #######################

#convert reads:
python3 Start_Read_Conversion.py --base samp_data --subdirs subdirs_to_process.txt --out inDrops_2read
#merge reads:
python3 Merge_Library_Files.py --base_dir inDrops_2read --map_file Seq_Metadata.txt --out inDrops_merged
#output files are contained in inDrops_merged directory

#generate barcode whitelist for StarSOLO (only have to do this once):
python3 Generate_Barcodes.py indrops_barcodes.txt



############### Lane and Library Index Metadata #######################
Create a file listing your lane number and the library indices expected in each lane. There should be one of these files in each data directory. An example file is provided in the sample data directory (Lane_Lib_Mapping.txt)


############### Specify the Directories to Process #######################
Specify the names of the subdirectories you wish to process in this file. We frequently received data in multiple tranches, and kept all raw data in one master directory. We used this file to specify which of the subdirectories to process, allowing us to process only the new data. An example file is provided (subdirs_to_process.txt). Note there is only one subdirectory listed here -- additional subdirectories would go on additional lines.


############### Convert the Reads #######################
Start the read conversion from the inDrops 4-read format to a 2-read format compatible with StarSOLO. This script will search through the main directory listed with --base for all the subdirectories listed in the --subdirs file. Within each of these subdirectories, it expects to see a lane and library index metadata file (you can change the default file name it searches for with --ind_map_file). The new 2-read format files are output into the directory specified with --out. Note that a separate set of read files will be output for each lane and library index. Also note that this script will call the Parse_ReadFiles_WithIndex.py script. Make sure it's located in the same directory, or specify the filename/location with --script.

Example command with the example dataset:
python3 Start_Read_Conversion.py --base samp_data --subdirs subdirs_to_process.txt --out inDrops_2read


############### Create a Sequence Metadata File #######################
Make a metadata file with each row listing a sequencing run and index combination. First column should be the run ID (e.g. the subdirectory the data initially came from), the second column should have the library index, and the third column should be the label to use for the output files. Note that the third column can be used to merge libraries across multiple different sequencing runs by using duplicate labels. The downstream merging script will simply come up with a unique list of IDs from this third column, and merge all read files associated with each of these unique IDs into one output file.

An example file (Seq_Metadata.txt) is provided. Note that you can have one master file for all the runs in your analysis, regardless of whether they will be processed in the current batch of data. The downstream script will match up the filenames in the data processing directory with the metadata from this file, and will only operate on the files within the data processing directory. Thus, extra rows in this file that are not used are completely fine.


############### Merge the Reads #######################
This step will merge all the reads associated with each library into one set of read files. The input reads are in the directory specified by --base_dir, and the reads are output in the directory specified by --out

Example command:
python3 Merge_Library_Files.py --base_dir inDrops_2read --map_file Seq_Metadata.txt --out inDrops_merged


############### Barcode Whitelist File #######################
StarSOLO utilizes a barcode whitelist file to filter out impossible cell barcodes. To generate this for inDrops, use the Generate_Barcodes.py script. Much of this script and methodology was adapted from Adrian Veres and indrops.py: https://github.com/indrops/indrops
First download the gel_barcode2_list provided by inDrops and place it in the same directory as the script (or supply the path to this file with --bc_file option). A copy of this file is included here. Now run the script:
python3 Generate_Barcodes.py indrops_barcodes.txt


############### StarSOLO parameters #######################
These parameters were used for StarSOLO mapping in our manuscript:
--soloType CB_UMI_Simple --soloCBwhitelist {whitelist_file} --soloCBstart 1 --soloCBlen 16 --soloUMIstart 17 --soloUMIlen 6 --soloBarcodeReadLength 0 --soloUMIfiltering MultiGeneUMI --soloCBmatchWLtype 1MM_multi_pseudocounts --soloFeatures Gene --soloStrand Forward --soloUMIdedup 1MM_All --readFilesCommand zcat --soloCellFilter CellRanger2.2 2000 0.99 10

The parameters related to this specific read processing pipeline are the cell barcode and UMI length and start positions, as well as "soloType".



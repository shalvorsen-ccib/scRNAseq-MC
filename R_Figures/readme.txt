############### Introduction #######################
This repository contains the R code for generating the figures in our publication on characterizing Microscopic Colitis using single-cell RNA sequencing technologies.


############### Software #######################
The primary analysis is done using the R package Seurat. Many ancillary packages are called during the generation of various figures. The necessary packages are loaded at the beginning of each file, so you can make sure they are all installed. 


############### Files #######################
The file "MC_Misc_Functions.rmd" contains many helper functions utilized for generating and/or customizing various plots. These functions will need to be sourced before running the figure generation code.

The "MC_scRNAseq_Figures.rmd" file contains the code used to generate most of the figures, with the exception of the CellPhoneDB plots. The code for generating the CellPhoneDB plots is contained in the file "MC_CellPhoneDB_Vis.rmd".


############### Data #######################
The IRB protocol these patients were consented under does not allow for public sharing of their raw sequence data, so we cannot deposit the raw data into GEO. However, we can share the processed data. Due to file size limitations, we cannot upload it to GitHub. However, we have shared it at the link below:

https://www.dropbox.com/scl/fo/nw1nad9n7aar78k48xzog/AC7KG0qszR5Qv_omwvEQ7yM?rlkey=94yym7ylhdq0gidjme9a522c1&dl=0
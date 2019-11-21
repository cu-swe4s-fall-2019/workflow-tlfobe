# workflow-tlfobe

This repository is a testcase for using SnakeMake to run a pipeline of files. In this repo one can generate a series of boxplots of the gene counts for any number of genes and tissues found in the GTEx dataset.

# Installation

To install this program, make sure you have `matplotlib` installed. `matplotlib` can be installed using conda:

```
conda install matplotlib --yes
```

Otherwise, all other modules are python modules. This was developed and tested on Python 3.6.

# Usage

To use this pipeline, one only has to type:
```
snakemake
```
This output will run the entire pipeline, which:
1. Pulls down both `GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt` and `GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz`. These are both datafiles that contain the relevant data present in the output boxplots.
2. Extracts tissue datafiles, which contains sample ID numbers pertaining to specific tissue types. (`Brain.txt`, `Blood.txt`)
3. Extracts gene datafiles, which contains sample IDs and their gene counts for specific genes. (`BRCA2.txt`, `MEN1`)
4. Uses those files to generate a plot with boxplots of the gene counts for each tissue and gene type.

The full workflow results in figure like such: 
![Alt text]()
<img src="images/Brain-Heart-Blood-Skin_SDHB-MEN1-KCNH2-MSH2-MYL2-BRCA2.png">


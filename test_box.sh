#!/bin/bash
test -e ssshtest ||  wget -q http://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

# grab files for testing
wget https://storage.googleapis.com/gtex_analysis_v8/annotations/GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt
wget https://github.com/swe4s/lectures/raw/master/data_integration/gtex/GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz

# generate some data files to build plots with

for gene in MYL2 MSH2 MEN1 KCNH2 BRCA2 SDHB
do
    python get_gene_counts.py --file_name GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz --gene_name $gene --output_file $gene.txt
done

for tissue in Brain Heart Blood Skin
do
    python get_tissue_samples.py --file_name GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt --tissue_name $tissue --output_file $tissue.txt
done


run test_box_normal python box.py --tissues Brain Heart Blood Skin --genes SDHB MEN1 KCNH2 MSH2 MYL2 BRCA2
assert_exit_code 0
assert_no_stdout
assert_no_stderr

rm Brain-Heart-Blood-Skin_SDHB-MEN1-KCNH2-MSH2-MYL2-BRCA2.png

run test_box_no_enough_inputs python box.py
assert_exit_code 2
assert_stderr

run test_box_no_genefile python box.py --tissues NOTTISSUE Heart Blood Skin --genes SDHB MEN1 KCNH2 MSH2 MYL2 BRCA2
assert_exit_code 1
assert_in_stderr NOTTISSUE

run test_box_no_genefile python box.py --tissues Brain Heart Blood Skin --genes SDHB MEN1 KCNH2 MSH2 MYL2 NOTGENE
assert_exit_code 1
assert_in_stderr NOTGENE





# cleanup

rm GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz
rm GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt

for gene in MYL2 MSH2 MEN1 KCNH2 BRCA2 SDHB
do
    rm $gene.txt
done

for tissue in Brain Heart Blood Skin
do
    rm $tissue.txt
done
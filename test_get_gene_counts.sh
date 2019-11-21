#!/bin/bash
test -e ssshtest ||  wget -q http://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

# grab file for testing
wget https://github.com/swe4s/lectures/raw/master/data_integration/gtex/GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz

run test_get_gene_counts python get_gene_counts.py --file_name GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz --gene_name SDHB --output_file out.txt
assert_exit_code 0
assert_no_stdout

rm out.txt

run test_get_gene_counts_not_enough_inputs python get_gene_counts.py
assert_exit_code 2
assert_stderr

run test_get_gene_counts_invalid_file python get_gene_counts.py --file_name not_a_file --gene_name SDHB --output_file out.txt
assert_exit_code 1
assert_in_stderr not_a_file

run test_get_gene_counts_invalid_file python get_gene_counts.py --file_name GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz --gene_name HAHA --output_file out.txt
assert_exit_code 1
assert_in_stderr HAHA

rm GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz
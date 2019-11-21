#!/bin/bash
test -e ssshtest ||  wget -q http://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

# grab file for testing
wget https://storage.googleapis.com/gtex_analysis_v8/annotations/GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt

run test_get_tissue_counts python get_tissue_samples.py --file_name GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt --tissue_name Brain --output_file out.txt
assert_exit_code 0
assert_no_stdout

rm out.txt

run test_get_tissue_samples_not_enough_inputs python get_tissue_samples.py
assert_exit_code 2
assert_stderr

run test_get_tissue_samples_invalid_file python get_tissue_samples.py --file_name not_a_file --tissue_name Brain --output_file out.txt
assert_exit_code 1
assert_in_stderr not_a_file

run test_get_tissue_samples_invalid_file python get_tissue_samples.py --file_name GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt --tissue_name HAHA --output_file out.txt
assert_exit_code 1
assert_in_stderr HAHA

run test_get_tissue_samples_invalid_attribute python get_tissue_samples.py --file_name GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt --tissue_name HAHA --output_file out.txt --attribute NOTATTRIBUTE
assert_exit_code 1
assert_in_stderr NOTATTRIBUTE

rm GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt
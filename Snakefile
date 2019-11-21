TISSUES = ["Brain", "Heart", "Blood", "Skin" ]
GENES = ["SDHB", "MEN1", "KCNH2", "MSH2", "MYL2", "BRCA2"]


rule all:
    input:
        "-".join(TISSUES)+"_"+"-".join(GENES) + ".png"

rule plot:
    input:
        expand("{gene}.txt", gene=GENES),
        expand("{tissue}.txt", tissue=TISSUES),
    output:
        "-".join(TISSUES)+"_"+"-".join(GENES) + ".png"
    shell:
        "python box.py " \
        + " --tissues "+" ".join(TISSUES) \
        + " --genes "+" ".join(GENES)
        + " --out_file {output}"


rule tissue_samples:
    input:
        "GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt"
    output:
        expand("{tissue}.txt", tissue=TISSUES)
    shell:
        "for tissue in {TISSUES}; do " \
        +  "python get_tissue_samples.py --file_name {input} --tissue_name $tissue --output_file $tissue\.txt;"\
        + "done"

rule sample_tissue_data:
    output:
        "GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt"
    shell:
        "wget https://storage.googleapis.com/gtex_analysis_v8/annotations/GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt"

rule gene_sample_counts:
    input:
        "GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz"
    output:
        expand("{gene}.txt", gene=GENES)
    shell:
        "for gene in {GENES}; do " \
        +   "python get_gene_counts.py --file_name {input} --gene_name $gene --output_file $gene\.txt;" \
        + "done"
        
rule gene_data:
    output:
        "GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz"
    shell:
        "wget https://github.com/swe4s/lectures/raw/master/data_integration/gtex/GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz"

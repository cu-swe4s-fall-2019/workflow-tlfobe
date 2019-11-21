import matplotlib.pyplot as plt
import matplotlib
import argparse
import sys
matplotlib.use('Agg')

# plt.style.use('fivethirtyeight')


def get_tissue_data(tissue, gene_list):
    if not isinstance(tissue, str):
        raise TypeError("box.get_tissue_data(): tissue needs to be type str")
    if not isinstance(gene_list, list):
        raise TypeError(
            "box.get_tissue_data(): gene_list needs to be type list")
    if not all([type(a) == str for a in gene_list]):
        raise TypeError(
            "box.get_tissue_data(): gene_list must be a list of type str")
    genes_counts = []
    tissue_samp_ids = []
    try:
        with open(tissue+".txt", 'r') as tissue_file:
            for line in tissue_file:
                tissue_samp_ids.append(line.rstrip())
    except FileNotFoundError:
        print("box.py: No tissue datafile named",
              tissue+".txt!", file=sys.stderr)
        sys.exit(1)

    for gene in gene_list:
        sample_to_counts = {}
        try:
            with open(gene+".txt", 'r') as gene_file:
                for line in gene_file:
                    A = line.rstrip().split()
                    sample_to_counts[A[0]] = A[1]
        except FileNotFoundError:
            print("box.py: No gene datafile named",
                  gene+".txt!", file=sys.stderr)
            sys.exit(1)

        gene_counts = []
        for tissue_id in tissue_samp_ids:
            if tissue_id in sample_to_counts.keys():
                gene_counts.append(int(sample_to_counts[tissue_id]))
        genes_counts.append(gene_counts)
    return(genes_counts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tissues",
                        required=True,
                        help="tissue name to pull sample ids from",
                        nargs="+",
                        type=str
                        )
    parser.add_argument("--genes",
                        required=True,
                        help="Name of genes to pull counts from",
                        nargs="+",
                        type=str
                        )
    parser.add_argument("--out_file",
                        required=False,
                        help="name of output figure",
                        type=str,
                        )
    args = parser.parse_args()

    fig, ax = plt.subplots(ncols=1, nrows=len(args.tissues), figsize=[10, 10])

    for i, tissue in enumerate(args.tissues):
        gene_counts_list = get_tissue_data(tissue, args.genes)
        ax[i].boxplot(gene_counts_list)
        ax[i].set_title(tissue)
        ax[i].set_xticklabels(args.genes)
        ax[i].spines['right'].set_visible(False)
        ax[i].spines['top'].set_visible(False)
        ax[i].set_ylabel("Count")

    if args.out_file is None:
        args.out_file = "-".join(args.tissues)+"_"+"-".join(args.genes)+".png"
    fig.savefig(args.out_file, dpi=300)


if __name__ == "__main__":
    main()

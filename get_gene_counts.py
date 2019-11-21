import sys
import gzip
import os
import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--file_name",
                        required=True,
                        help="path to gene count file",
                        type=str
                        )
    parser.add_argument("--gene_name",
                        required=True,
                        help="valid gene name/abbreivation",
                        type=str,
                        )
    parser.add_argument("--output_file",
                        required=True,
                        help="name of output file",
                        type=str)

    args = parser.parse_args()
    file_name = args.file_name
    gene_name = args.gene_name
    out_file_name = args.output_file

    try:
        o = open(out_file_name, 'w')
    except IsADirectoryError:
        print("get_gene_counts.py:", out_file_name,
              "is a directory, please choose a new outfile!", file=sys.stderr)
    except PermissionError:
        print("get_gene_counts.py", out_file_name,
              "doesn't allow writing!", file=sys.stderr)
    version = None
    dim = None
    header = None

    try:
        f = gzip.open(file_name, 'rt')
    except FileNotFoundError:
        print("get_gene_counts.py:", file_name,
              "isn't a valid file!", file=sys.stderr)
        sys.exit(1)
    except IsADirectoryError:
        print("get_gene_counts.py:", file_name,
              "is a directory, please choose a new datafile!", file=sys.stderr)
    except PermissionError:
        print("get_gene_counts.py", file_name,
              "doesn't allow writing!", file=sys.stderr)

    gene_names = []

    for l in f:
        A = l.rstrip().split('\t')
        if version is None:
            version = A
            continue
        if dim is None:
            dim = A
            continue
        if header is None:
            header = A
            continue
        if A[1] == gene_name:
            for i in range(2, len(header)):
                o.write(header[i] + ' ' + A[i] + '\n')
        if A[1] not in gene_names:
            gene_names.append(A[1])

    if gene_name not in gene_names:
        print("get_gene_counts.py:", gene_name,
              "isn't present in", file_name+"!", file=sys.stderr)
        os.remove(out_file_name)
        sys.exit(1)
    f.close()
    o.close()


if __name__ == "__main__":
    main()

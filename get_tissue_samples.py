import sys
import argparse
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_name",
                        required=True,
                        help="path to gene count file",
                        type=str
                        )
    parser.add_argument("--tissue_name",
                        required=True,
                        help="available tissue type",
                        type=str,
                        )
    parser.add_argument("--output_file",
                        required=True,
                        help="name of output file",
                        type=str)

    args = parser.parse_args()

    file_name = args.file_name
    tissue_name = args.tissue_name
    out_file_name = args.output_file

    try:
        o = open(out_file_name, 'w')
    except IsADirectoryError:
        print("get_tissue_name.py:", out_file_name,
              "is a directory, please choose a new outfile!", file=sys.stderr)
    except PermissionError:
        print("get_tissue_name.py", out_file_name,
              "doesn't allow writing!", file=sys.stderr)

    header = None
    sampid_col = -1
    smts_col = -1

    try:
        f = open(file_name, 'rt')
    except FileNotFoundError:
        print("get_tissue_name.py:", file_name,
              "isn't a valid file!", file=sys.stderr)
        sys.exit(1)
    except IsADirectoryError:
        print("get_tissue_name.py:", file_name,
              "is a directory, please choose a new datafile!", file=sys.stderr)
    except PermissionError:
        print("get_tissue_name.py", file_name,
              "doesn't allow writing!", file=sys.stderr)

    tissue_names = []

    for l in f:
        A = l.rstrip().split('\t')
        if header is None:
            header = A
            sampid_col = A.index('SAMPID')
            smts_col = A.index('SMTS')
            continue

        if A[smts_col] == tissue_name:
            o.write(A[sampid_col] + '\n')

        if A[smts_col] not in tissue_names:
            tissue_names.append(A[smts_col])

    if tissue_name not in tissue_names:
        print("get_tissue_samples.py:", tissue_name,
              "isn't present in", file_name+"!", file=sys.stderr)
        os.remove(out_file_name)
        sys.exit(1)

    f.close()
    o.close()


if __name__ == "__main__":
    main()

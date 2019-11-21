import unittest
import box
import os
import random

gene_num = random.randint(0, 30)
tissue_num = random.randint(0, 30)


class TestGetTissueData(unittest.TestCase):
    def setUp(self):
        # tissues
        for i in range(tissue_num):
            with open("DUMMY_TISSUE_"+str(i)+".txt", 'w') as f:
                for j in range(random.randint(0, 500)):
                    f.write(str(j)+"\n")
        for i in range(gene_num):
            with open("DUMMY_GENE_"+str(i)+".txt", 'w') as f:
                for j in range(random.randint(0, 500)):
                    f.write(str(j)+" "+str(random.randint(1, 10000))+"\n")

    def test_get_tissue_data_normal(self):
        genes = ["DUMMY_GENE_"+str(j) for j in range(gene_num)]
        for i in range(tissue_num):
            genes_counts = box.get_tissue_data("DUMMY_TISSUE_"+str(i), genes)
            assert len(genes_counts) == len(genes)

    def test_get_tissue_data_tissue_type(self):
        genes = ["DUMMY_GENE_"+str(j) for j in range(gene_num)]
        self.assertRaises(TypeError, box.get_tissue_data, 123456, genes)

    def test_get_tissue_data_genes_type(self):
        self.assertRaises(TypeError, box.get_tissue_data, "tissue", "string!")

    def test_get_tissue_data_genes_list_types(self):
        self.assertRaises(TypeError, box.get_tissue_data,
                          "tissue", ["string", 1, []])

    def tearDown(self):
        os.system("rm DUMMY*")

import pytest
from rdkit import Chem

import opm.bo_rdkit as bo_rdkit

class TestBoRdkit:

    smi = "CC(C)Cc1ccc(C(C)C(=O)O)cc1"
    mol = Chem.MolFromSmiles(smi)
    bo = bo_rdkit.RDKitOperation()

    def test_calculate_iupac_name(self):
        assert self.bo._calculate_iupac_name(self.mol) == "2-methylbutane-1,4-diol"

    def test_calculate_mol_formula(self):
        assert self.bo._calculate_mol_formula(self.mol) == "C13H18O2"

    def test_calculate_mol_weight(self):
        assert self.bo._calculate_mol_weight(self.mol) == 206.28499999999997

    def test_calculate_smiles(self):
        assert self.bo._calculate_smiles(self.mol) == self.smi

    def test_calculate_clogp(self):
        assert self.bo._calculate_clogp(self.mol) == 3.073200000000001

    def test_calculate_clogd(self):
        assert self.bo._calculate_clogd(self.mol) == 3.073200000000001

    def test_calculate_tpsa(self):
        assert self.bo._calculate_tpsa(self.mol) == 37.3

    def test_calculate_pka(self):
        assert self.bo._calculate_pka(self.mol) == None

    def test_calcualte_heavy_atom_count(self):
        assert self.bo._calculate_heavy_atom_count(self.mol) == 15

    def test_calculate_num_rotatable_bonds(self):
        assert self.bo._calculate_num_rotatable_bonds(self.mol) == 4

    def test_calculate_num_h_donor(self):
        assert self.bo._calculate_num_h_donor(self.mol) == 1

    def test_calculate_num_h_acceptor(self):
        assert self.bo._calculate_num_h_acceptor(self.mol) == 1








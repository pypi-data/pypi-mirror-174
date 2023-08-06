#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/10/6 20:54
# @Author  : zhangbc0315@outlook.com
# @File    : rxn_template_apply.py
# @Software: PyCharm

from collections import namedtuple

from rdkit.Chem import AllChem


Rxn = namedtuple('Rxn', ['reactants', 'products'])


class RXNTemplateApply:

    @classmethod
    def _react_from_smi(cls, smi: str, rxn_template_smarts: str, remove_stereo: bool) -> [[str]]:
        """
        :param smi:
        :param rxn_template_smarts:
        :param remove_stereo:
        :return:
        """
        rxn_template = AllChem.ReactionFromSmarts(rxn_template_smarts)
        reactant = AllChem.MolFromSmiles(smi)
        products_set = rxn_template.RunReactants((reactant, ))
        p_smis_set = []
        for products in products_set:
            p_smis = []
            for product in products:
                if remove_stereo:
                    AllChem.RemoveStereochemistry(product)
                p_smis.append(AllChem.MolToSmiles(product, canonical=True))
            p_smis_set.append(p_smis)
        return p_smis_set

    @classmethod
    def _remove_unreact_r(cls, r_smi: str, p_smi: str) -> (str, bool):
        """

        :param r_smi:
        :param p_smi:
        :return:
        """
        start = p_smi.find(r_smi)
        if start == -1:
            return p_smi, False
        end = start + len(r_smi)
        if start == 0 and end == len(p_smi) - 1:
            return '', True
        if start == 0 and p_smi[end] != '.':
            return p_smi, False
        if end == len(p_smi) - 1 and p_smi[start-1] != '.':
            return p_smi, False
        if p_smi[start-1] != '.' or p_smi[end] != '.':
            return p_smi, False
        return p_smi[:start] + p_smi[end:], True

    @classmethod
    def _clean_rxn(cls, r_smis: [str], p_smis: [str]) -> ([str], [str]):
        """

        :param r_smis:
        :param p_smis:
        :return:
        """
        cleaned_r_smis = set()
        cleaned_p_smis = []
        for p_smi in p_smis:
            for r_smi in r_smis:
                p_smi, unreact = cls._remove_unreact_r(r_smi, p_smi)
                if not unreact:
                    cleaned_r_smis.add(r_smi)
                cleaned_p_smis.append(p_smi)
        return list(cleaned_r_smis), cleaned_p_smis

    @classmethod
    def _contain_p_smi(cls, rxns: [Rxn], p_smis: [str]):
        for rxn in rxns:
            if len(p_smis) == len(rxn.products) and all([p_smi in rxn.products for p_smi in p_smis]):
                return True
        return False

    @classmethod
    def react_from_smis(cls, smis: [str], rxn_template_smarts: str,
                        remove_stereo: bool = True, remove_unreact_reactants: bool = True) -> [Rxn]:
        """
        
        :param smis:
        :param rxn_template_smarts:
        :param remove_stereo:
        :param remove_unreact_reactants:
        :return:
        """
        p_smis_set = cls._react_from_smi('.'.join(smis), rxn_template_smarts, remove_stereo)
        cleaned_rxns_set = []
        for p_smis in p_smis_set:
            if remove_unreact_reactants:
                cleaned_r_smis, cleaned_p_smis = cls._clean_rxn(smis, p_smis)
            else:
                cleaned_r_smis = smis
                cleaned_p_smis = p_smis
            cleaned_p_smis = list(set(cleaned_p_smis))
            if not cls._contain_p_smi(cleaned_rxns_set, cleaned_p_smis):
                cleaned_rxns_set.append(Rxn(reactants=cleaned_r_smis, products=cleaned_p_smis))
        return cleaned_rxns_set


if __name__ == "__main__":
    pass

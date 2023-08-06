#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Read .lpp file.
"""
import re

from lpp_parser.data import ELEM_Z_MAP

# [settings], primary beam, and frag beam
_AZQ_REG = r'A,Z,Q = (\d+)(\D+)(\d+)\+.*'  # 1:A, 2:name, 3:Q
_EK_REG = r'Energy = (\d+(?:\.\d+)?).*'  # 1: Energy in MeV/u
_PWR_REG = r'Intensity = (\d+(?:\.\d+)?).*'  # 1: Power in kW
_RF_FREQ_REG = r'RF.* = (\d+(?:\.\d+)?).*'  # 1: RF frequency in MHz
_TAU_REG = r'Bunch.* = (\d+(?:\.\d+)?).*'  # 1: Bunch length in ns
_ISO_REG = r'Settings.* = (\d+)([a-zA-Z]+).*'  # Settings on A,Z, 1: A, 2: name


def get_lpp_info(filepath: str):
    """Return a list of interested info from the given .lpp file.
    """
    info_dict = {
        'settings': {},
    }
    processed_nline = 0
    with open(filepath, "r") as fp:
        line = fp.readline()
        while line:
            processed_nline += 1
            if line.strip().startswith('[settings]'):
                print(f"{processed_nline}: hit [settings] section")
                _line1 = fp.readline()  # A,Z,Q
                _line1_r = re.match(_AZQ_REG, _line1.strip())
                _line2 = fp.readline()  # Energy, MeV/u
                _line2_r = re.match(_EK_REG, _line2.strip())
                _line3 = fp.readline()  # Intensity (Power), kW
                _line3_r = re.match(_PWR_REG, _line3.strip())
                _line4 = fp.readline()  # RF frequency, MHz
                _line4_r = re.match(_RF_FREQ_REG, _line4.strip())
                _line5 = fp.readline()  # Bunch length, ns
                _line5_r = re.match(_TAU_REG, _line5.strip())
                _line6 = fp.readline()  # Settings on A, Z (isotope)
                _line6_r = re.match(_ISO_REG, _line6.strip())
                info_dict['settings']['primary_beam'] = {
                    'A': _line1_r.group(1),
                    'name': _line1_r.group(2),
                    'Q': _line1_r.group(3),
                    'Z': ELEM_Z_MAP[_line1_r.group(2)],
                    'Ek': _line2_r.group(1),
                    'power': _line3_r.group(1),
                    'rf_freq': _line4_r.group(1),
                    'tau': _line5_r.group(1),
                }
                info_dict['settings']['frag_beam'] = {
                    'A': _line6_r.group(1),
                    'name': _line6_r.group(2),
                    'Z': ELEM_Z_MAP[_line6_r.group(2)],
                }

            line = fp.readline()
    print(info_dict)
    return info_dict


if __name__ == '__main__':
    lpp_filepath = "tests/44S_target8mm.lpp"
    get_lpp_info(lpp_filepath)

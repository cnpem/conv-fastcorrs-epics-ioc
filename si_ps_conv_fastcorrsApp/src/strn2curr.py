from __future__ import print_function
from siriuspy.magnet.factory import NormalizerFactory
from siriuspy.search import MASearch
from devsup.db import getRecord


class Converter(object):
    raw = True

    def __init__(self, rec, args):
        tokens = args.split()
        if len(tokens) == 4:
            test = ''
            sec, dip, ori, base = tokens
        elif len(tokens) == 5:
            test, sec, dip, ori, base = tokens
        else:
            raise ValueError(f"Expected 4 or 5 values, got {len(tokens)}")

        psname = f"SI-{sec}{dip}:PS-{ori}"
        maname = MASearch.conv_psname_2_psmaname(psname)
        self.norm = NormalizerFactory.create(maname)

        self.dipole_strength = getRecord(
            f"{test}copy-SI-{sec}:Fam:PS-B1B2-1:EnergyRef-Mon")
        self.base_record = getRecord(f"{test}out-{psname}:{base}")

    def process(self, rec, reason):
        self.base_record.VAL = self.norm.conv_strength_2_current(
            rec.VAL, strengths_dipole=self.dipole_strength.VAL)

    def detach(self, rec):
        pass


def build(rec, args):
    return Converter(rec, args)

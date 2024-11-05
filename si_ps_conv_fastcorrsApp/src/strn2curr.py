from __future__ import print_function
from siriuspy.magnet.factory import NormalizerFactory
from siriuspy.search import MASearch
from devsup.db import getRecord

class Converter(object):
    raw = True
    def __init__(self, rec, args):
        parsed_args = args.split()
        psname = parsed_args[0][:-1]
        maname = MASearch.conv_psname_2_psmaname(psname)
        self.norm = NormalizerFactory.create(maname)

        self.dipole_strength = getRecord("copy-SI-Fam:PS-B1B2-1:EnergyRef-Mon")
        self.base_record = getRecord("copy-" + parsed_args[0]+parsed_args[1])

    def process(self, rec, reason):
        self.base_record.VAL = self.norm.conv_strength_2_current(rec.VAL, strengths_dipole=self.dipole_strength.VAL)
        self.base_record.scan(sync=True)

    def detach(self, rec):
        pass

def build(rec, args):
    return Converter(rec, args)

#!/usr/bin/env python3
# -----------------------------------------------------------------------------
#   Copyright (C): OpenGATE Collaboration
#   This software is distributed under the terms
#   of the GNU Lesser General  Public Licence (LGPL)
#   See LICENSE.md for further details
# -----------------------------------------------------------------------------

import gatetools as gt
import gatetools.phsp as phsp
import itk
import click
import os
import uproot
from pathlib import Path
import numpy as np
import logging
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('output_folders',
                nargs=-1,
                required=True,
                type=click.Path(exists=True, file_okay=True, dir_okay=True))
@gt.add_options(gt.common_options)
def analyse_command_line(output_folders, **kwargs):
    # logger
    gt.logging_conf(**kwargs)
    # Run the analysis with the command line (click)
    # the return code is 0 (fail) or 1 (success)
    r = analyse_all_folders(output_folders)
    print(f'Last test return is: {r}')


def analyse_all_folders(output_folders):
    r_spectrum = analyze_137Cs("spectrum", "output-9.0/Energy_spectrum_10M.root", "output/Energy_spectrum.root")
    r_source = analyze_137Cs("source", "output-9.0/Energy_source_10M.root", "output/Energy_source.root")
    return(r_spectrum and r_source)

def analyze_137Cs(type, file10M, file):
    # Read test root file
    root_filename1 = Path(file)
    f1 = uproot.open(root_filename1)
    k1 = f1.keys()
    h1 = f1['edepHisto']
    print('Read object', h1)

    # Read reference root file
    root_filename2 = Path(file10M)
    f2 = uproot.open(root_filename2)
    k2 = f2.keys()
    h2 = f2['edepHisto']
    print('Read object', h2)

    # Compute efficiency parameters
    nEntries = 1000000 #number of primary particles in GATE
    h1_full = np.sum(h1.values())
    h1_peak = np.sum(h1.values()[661:663])
    efficiency_full = 100.*h1_full/nEntries
    error_efficiency_full = 100.*np.sqrt(h1_full)/nEntries
    print("Full efficiency : %.2f \u00B1 %.2f %%" % (efficiency_full,error_efficiency_full))
    efficiency_peak = 100.*h1_peak/nEntries
    error_efficiency_peak = 100.*np.sqrt(h1_peak)/nEntries
    print("Peak efficiency : %.2f \u00B1 %.2f %%" % (efficiency_peak,error_efficiency_peak))

    # Compare to reference values (Gate 8.2, Geant4 10.5.1, N = 1e7)
    if type == "spectrum":
        reference_efficiency_full = 14.83
    else:
        reference_efficiency_full = 14.64
    reference_efficiency_peak = 7.02

    ratio_full = efficiency_full/reference_efficiency_full
    ratio_full_error = ratio_full*(error_efficiency_full/efficiency_full)
    print("Benchmark full efficiency : %.2f \u00B1 %.2f" % (ratio_full,ratio_full_error))
    ratio_peak = efficiency_peak/reference_efficiency_peak
    ratio_peak_error = ratio_peak*(error_efficiency_peak/efficiency_peak)
    print("Benchmark peak efficiency : %.2f \u00B1 %.2f" % (ratio_peak,ratio_peak_error))

    efficiecyTest = False
    peakTest = False
    if(np.abs(efficiency_full-reference_efficiency_full) <= 2*error_efficiency_full):
        print("Test of full efficiency is OK for " + type)
        efficiecyTest = True
    else:
        print("Problem with test of full efficiency for " + type)

    if(np.abs(efficiency_peak-reference_efficiency_peak) <= 2*error_efficiency_peak):
        print("Test of spectrum efficiency is OK for " + type)
        peakTest = True
    else:
        print("Problem with test of peak efficiency for " + type)

    # Plot 1D histogram
    plt.title("137Cs energy " + type)
    plt.plot(h1.values(), "r-", label = "Test")
    plt.plot(h2.values()/10., "b-", label = "Reference")
    plt.xlabel("Energy [MeV]")
    plt.ylabel("N")	
    plt.yscale('log')
    plt.legend()
    plt.savefig('output_' + type + '.pdf')
    plt.show()

    return(efficiecyTest and efficiecyTest)


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    analyse_command_line()

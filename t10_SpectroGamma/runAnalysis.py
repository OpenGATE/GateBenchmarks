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
import matplotlib.cm as cm

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

# -----------------------------------------------------------------------------
def analyse_all_folders(output_folders):
    fig, axs = plt.subplots(2, 2)
    axs[0, 0].title.set_text("137Cs energy spectrum emstandard_opt4")
    axs[0, 1].title.set_text("137Cs energy source emstandard_opt4")
    axs[1, 0].title.set_text("137Cs energy spectrum QGSP_BERT_EMZ")
    axs[1, 1].title.set_text("137Cs energy source QGSP_BERT_EMZ")

    iFolder = 0
    for output_folder in output_folders:
        r = analyze_137Cs(output_folder, axs, iFolder)
        iFolder += 1

    for i in range(2):
        for j in range(2):
            axs[i, j].set_xlabel("Energy [MeV]")
            axs[i, j].set_ylabel("N")
            axs[i, j].set_yscale('log')
            axs[i, j].legend()
    fig.tight_layout()
    plt.show()
    plt.savefig('output.pdf')
    return(r)

# -----------------------------------------------------------------------------
def analyze_137Cs(output_folder, axs, iFolder):
    value_spectrum_emstandard_opt4, r_spectrum_emstandard_opt4 = analyze_one_file(os.path.join(output_folder, "Energy_spectrum_emstandard_opt4.root"))
    value_source_emstandard_opt4, r_source_emstandard_opt4 = analyze_one_file(os.path.join(output_folder, "Energy_source_emstandard_opt4.root"))
    value_spectrum_QGSP_BERT_EMZ, r_spectrum_QGSP_BERT_EMZ = analyze_one_file(os.path.join(output_folder, "Energy_spectrum_QGSP_BERT_EMZ.root"))
    value_source_QGSP_BERT_EMZ, r_source_QGSP_BERT_EMZ = analyze_one_file(os.path.join(output_folder, "Energy_source_QGSP_BERT_EMZ.root"))

    scale = 1.
    colors = cm.rainbow(np.linspace(0, 1, 10))
    if output_folder != "output":
        scale = 10.
    axs[0, 0].plot(value_spectrum_emstandard_opt4/scale, c=colors[iFolder], ls='-', label = output_folder)
    axs[0, 1].plot(value_source_emstandard_opt4/scale, c=colors[iFolder], ls='-', label = output_folder)
    axs[1, 0].plot(value_spectrum_QGSP_BERT_EMZ/scale, c=colors[iFolder], ls='-', label = output_folder)
    axs[1, 1].plot(value_source_QGSP_BERT_EMZ/scale, c=colors[iFolder], ls='-', label = output_folder)

    return(r_spectrum_emstandard_opt4 and r_source_emstandard_opt4 and r_spectrum_QGSP_BERT_EMZ and r_source_QGSP_BERT_EMZ)

# -----------------------------------------------------------------------------
def analyze_one_file(file):
    # Read test root file
    print(file)
    root_filename1 = Path(file)
    f1 = uproot.open(root_filename1)
    k1 = f1.keys()
    h1 = f1['edepHisto']
    print('Read object', h1)

    # Compute efficiency parameters
    nEntries = 1000000 #number of primary particles in GATE
    if "output-" in file:
        nEntries *= 10
    h1_full = np.sum(h1.values())
    h1_peak = np.sum(h1.values()[661:663])
    efficiency_full = 100.*h1_full/nEntries
    error_efficiency_full = 100.*np.sqrt(h1_full)/nEntries
    print("Full efficiency : %.2f \u00B1 %.2f %%" % (efficiency_full,error_efficiency_full))
    efficiency_peak = 100.*h1_peak/nEntries
    error_efficiency_peak = 100.*np.sqrt(h1_peak)/nEntries
    print("Peak efficiency : %.2f \u00B1 %.2f %%" % (efficiency_peak,error_efficiency_peak))

    # Compare to reference values (Gate 9, Geant4 10.7, N = 1e7, opt4)
    if "spectrum" in file:
        reference_efficiency_full = 14.75
    else:
        reference_efficiency_full = 14.93
    reference_efficiency_peak = 7.00

    ratio_full = efficiency_full/reference_efficiency_full
    ratio_full_error = ratio_full*(error_efficiency_full/efficiency_full)
    print("Benchmark full efficiency : %.2f \u00B1 %.2f" % (ratio_full,ratio_full_error))
    ratio_peak = efficiency_peak/reference_efficiency_peak
    ratio_peak_error = ratio_peak*(error_efficiency_peak/efficiency_peak)
    print("Benchmark peak efficiency : %.2f \u00B1 %.2f" % (ratio_peak,ratio_peak_error))

    efficiencyTest = False
    peakTest = False
    print(str(efficiency_full) + " " + str(reference_efficiency_full) + " " + str(error_efficiency_full))
    if(np.abs(efficiency_full-reference_efficiency_full) <= 3*error_efficiency_full):
        print("Test of full efficiency is OK for " + file)
        efficiencyTest = True
    else:
        print("Problem with test of full efficiency for " + file)

    if(np.abs(efficiency_peak-reference_efficiency_peak) <= 3*error_efficiency_peak):
        print("Test of peak efficiency is OK for " + file)
        peakTest = True
    else:
        print("Problem with test of peak efficiency for " + file)

    return (h1.values(), efficiencyTest and peakTest) 


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    analyse_command_line()

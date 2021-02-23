#!/usr/bin/env python3

import matplotlib

matplotlib.use('TkAgg')  # (required on osx)
import matplotlib.pyplot as plt

import numpy as np
import gatetools as gt
import uproot4 as uproot
import click
import os

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('output_folders',
                nargs=-1,
                required=True,
                type=click.Path(exists=True, file_okay=True, dir_okay=True))
@gt.add_options(gt.common_options)
def analyse_click(output_folders, **kwargs):
    analyse_all_folders(output_folders)


def analyse_all_folders(output_folders):
    for folder in output_folders:
        f = os.path.join(folder, 'range.root')
        try:
            f = uproot.open(f)
        except Exception:
            print(f'Not a root file ? {f}')
            exit(-1)
        analyse(f)


def analyse(f):
    # get the track length data
    x = f['Annihilation']['X'].array(library="np")
    y = f['Annihilation']['Y'].array(library="np")
    z = f['Annihilation']['Z'].array(library="np")
    pos = np.array((x, y, z))

    # compute distance (assume source is at 0,0,0)
    distance = np.linalg.norm(pos, axis=0)

    # some info about range
    '''
    In "Radiation Oncology Physics: A Handbook for Teachers and Students"
    from Podgorsak page 277
    "The maximum range Rmax (cm or g/cm2) is defined as the depth at which
     extrapolation of the tail of the central axis depth dose curve meets 
     the bremsstrahlung background, as shown in Fig. 8.2. It is the largest
     penetration depth of electrons in the absorbing medium. The maximum range
     has the drawback of not giving a well defined measurement point."

    Here: maximum of range.
   
    '''

    # model for Rmean and Rmax
    '''
    [Lehnert2011]
    "Emax is the positron end point energy or maximum energy for the particular 
    positron emitter in MeV, E is the kinetic energy of the positron in MeV, 
    p is the momentum of the positron and F(Z,E) is the Fermi function, 
    with Z being the atomic number of the daughter nucleus following beta decay."
    
    Rmean_model [cm] = 0.18 * Emax[MeV]^1.14 / rho [g.cm-3]
    
    0.01 < Emax < 2.5 MeV
    Rmax_model [mg/cm2] = 412 * Emax [MeV]^(1.265−0.0954 ln Emax [MeV]) / rho [g.cm-3].
    
    2.5 < Emax < 20 MeV
    Rmax_model [mg/cm2] = ( 530 * Emax [MeV] - 106)  / rho [g.cm-3].
    
    [Lehnert2011] Table 1. Mean and end point energies for four major PET isotopes
    in keV
    | rad | Emean | Emax |
    |-----|-------|------|
    | 18F |   251 |  635 |
    | 11C |   390 |  970 |
    | 13N |   488 | 1190 |
    | 15O |   730 | 1720 |  
    
    https://ejnmmiphys.springeropen.com/articles/10.1186/s40658-016-0144-5/tables/1

    Table 1 Properties of pure positron emission radioisotopes. Data from the National Institute of Standards and Technology [14], Laboratoire National Henri Becquerel [15], and Brookhaven National Laboratory [16]. Range of positrons is in water [14]
    From: Physics of pure and non-pure positron emitters for PET: a review and a discussion
    Isotope	Half-life	β+%	    E max 	E mean 	Rmax    Rmean
    11C	    20.4 min	99.8	0.960	0.386	4.2	    1.2
    13N	    10.0 min	99.8	1.199	0.492	5.5	    1.8
    15O	    2 min	    99.9	1.732	0.735	8.4	    3.0
    18F	    110 min	    96.9	0.634	0.250	2.4	    0.6
    64Cu	12.7 h	    17.5	0.653	0.278	2.5	    0.7
    89Zr	78.4 h	    22.7	0.902	0.396	3.8	    1.3     
  
    '''

    # Ref for 18F
    Rmean_nist = 0.6
    Rmax_nist = 2.4

    # Rmean model
    Emax = 0.634  # MeV for 18F
    rho = 1  # water
    Rmean_model = 0.108 * Emax ** (1.14) / rho * 10  # in mm

    # historical values
    Rmean_histo = 0.42
    Rmax_histo = 2.7

    # Rmax model
    if Emax < 2.5:
        Rmax_model = (412 * np.power(Emax, (1.265 - 0.0954 * np.log(Emax)))) / rho / 100
    else:
        Rmax_model = (530 * Emax - 106) / rho / 100

    # Rmean
    Rmean = distance.mean()
    diff_Rmean_model = (Rmean - Rmean_model) / Rmean_model * 100
    diff_Rmean_nist = (Rmean - Rmean_nist) / Rmean_nist * 100
    diff_Rmean_histo = (Rmean - Rmean_histo) / Rmean_histo * 100

    # Rmax (Practical range Rp = max of all distances)
    Rmax = distance.max()
    diff_Rmax_model = (Rmax - Rmax_model) / Rmax_model * 100
    diff_Rmax_nist = (Rmax - Rmax_nist) / Rmax_nist * 100
    diff_Rmax_histo = (Rmax - Rmax_histo) / Rmax_histo * 100

    # print
    print(f'Number of events = {len(x)}')
    print(f'Rmean (nist)     = {Rmean_nist:.2f} mm')
    print(f'Rmean (model)    = {Rmean_model:.2f} mm')
    print(f'Rmean (historic) = {Rmean_histo:.2f} mm')
    print(f'Rmean (gate)     = {Rmean:.2f} mm     nist {diff_Rmean_nist:.2f} %   '
          f'model {diff_Rmean_model:.2f} %    '
          f'historic {diff_Rmean_histo:.2f} %')
    print(f'Rmax (nist)      = {Rmax_nist:.2f} mm')
    print(f'Rmax (model)     = {Rmax_model:.2f} mm')
    print(f'Rmax (gate)      = {Rmax:.2f} mm     nist {diff_Rmax_nist:.2f} %    '
          f'model {diff_Rmax_model:.2f} %    '
          f'historic {diff_Rmax_histo:.2f} %')

    # fig, ax = plt.subplots()
    plt.hist(distance, 200, density=True, histtype=u'step', facecolor='g', alpha=0.75)
    plt.title('Positron range')
    plt.savefig('range.pdf')
    # plt.show()

    # return value (only compare with historical version)
    tolerance = 5  # %
    return diff_Rmax_histo < tolerance and diff_Rmean_histo < tolerance


# --------------------------------------------------------------------------
if __name__ == '__main__':
    analyse_click()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uproot
import click
import gatetools as gt
import os
import numpy as np

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('output_folders', nargs=-1, required=True,
                type=click.Path(exists=True, file_okay=True, dir_okay=True))
@gt.add_options(gt.common_options)
def analysis_all_click(output_folders, **kwargs):
    analyse_all_folders(output_folders)


def analyse_all_folders(output_folders, **kwargs):
    # logger
    gt.logging_conf(**kwargs)
    # loop over folders
    for output_folder in output_folders:
        fn = os.path.join(output_folder, 'output.root')
        f = uproot.open(fn)
        r = analysis(f)
    # return only last analysis
    return r


def analysis(root_file):
    # Compute the types of events
    data = gt.get_pet_counts(root_file)

    # Compute the rate -> divide the counts per seconds (if available)
    d = gt.get_pet_data(root_file)
    if not d:
        print('Need the acquisition time to compute the NECR')
        exit(0)
    duration = d.stop_time_sec - d.start_time_sec

    print(f'Prompt events    {data.prompts_count} \t(all coincidences)')
    print(f'Delayed events   {data.delays_count}  \t(approximation of the number of random events)')
    print(f'Random events    {data.randoms_count} \t(including noise event)')
    print(f'Scattered events {data.scatter_count}')
    print(f'Trues events     {data.trues_count}')

    print(f'Prompt rate    {data.prompts_count / duration} counts.s-1')
    print(f'Delayed rate   {data.delays_count / duration}  counts.s-1')
    print(f'Random rate    {data.randoms_count / duration} counts.s-1')
    print(f'Scattered rate {data.scatter_count / duration} counts.s-1')
    print(f'Trues rate     {data.trues_count / duration} counts.s-1')

    # reference NECR (Salvadori2020)
    # obtained for 1787914158 Bq -> ~78 kBq.mL-1
    # (see below for volume computation)
    ref_necr = 170000

    # Cylindrical volume (in mm)
    cyl_radius = 102
    cyl_h = 700
    cyl_V = np.pi * cyl_radius ** 2 * cyl_h  # in mm3
    cyl_V = cyl_V * 0.001  # in mL
    print(f'Cylindrical phantom radius = {cyl_radius} mm')
    print(f'Cylindrical phantom height = {cyl_h} mm')
    print(f'Cylindrical phantom volume = {cyl_V:.2f} mL')

    # Total activity (see excel file)
    a = 1787914158  # in Bq
    ac = a / cyl_V
    print(f'Total activity             = {a / 1e6:.2f} MBq')
    print(f'Activity concentration     = {ac / 1e3:.3f} kBq.mL-1')

    # Compute NECR (Noise Equivalent Count Rate)
    Rt = data.trues_count / duration
    Rtot = data.prompts_count / duration
    Rsc = data.scatter_count / duration
    necr = Rt ** 2 / Rtot
    sf = Rsc / (Rt + Rsc)
    print(f'Simulation duration        = {duration} sec')
    print(f'ScatterFraction            = {sf * 100.0} %')
    print(f'NECR                       = {necr:.2f} <-> {ref_necr} counts.s-1')

    # difference with reference
    diff = (necr - ref_necr) / ref_necr * 100.0
    print()
    print(f'NECR Difference is         = {diff:.2f} %')

    return abs(diff) < 10.0


# --------------------------------------------------------------------------
if __name__ == '__main__':
    analysis_all_click()

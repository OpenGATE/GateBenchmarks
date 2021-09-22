#!/usr/bin/env python3
# -----------------------------------------------------------------------------
#   Copyright (C): OpenGATE Collaboration
#   This software is distributed under the terms
#   of the GNU Lesser General  Public Licence (LGPL)
#   See LICENSE.md for further details
# -----------------------------------------------------------------------------

import gatetools as gt
import click
import os
import numpy as np
import logging
import sys
from box import Box
import pandas as pd

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
    # sort folders: the current simple 'output' must be at the end
    output_folders = list(output_folders)
    if 'output' in output_folders:
        output_folders.pop(output_folders.index('output'))
    output_folders.append('output')
    for folder in output_folders:
        if not os.path.isdir(folder):
            continue
        r = analyse_one_folder(folder)
    return r


def read_stat_file(filename):
    p = os.path.abspath(filename)
    f = open(p, 'r')
    stat = Box()
    read_track = False
    for line in f:
        if 'NumberOfRun' in line:
            stat.run = float(line[len('# NumberOfRun    ='):])
        if 'NumberOfEvents' in line:
            stat.event = float(line[len('# NumberOfEvents = '):])
        if 'NumberOfTracks' in line:
            stat.track = float(line[len('# NumberOfTracks ='):])
        if 'NumberOfSteps' in line:
            stat.step = float(line[len('# NumberOfSteps  ='):])
        if 'ElapsedTimeWoInit' in line:
            stat.duration = float(line[len('# ElapsedTimeWoInit     ='):])
        if read_track:
            w = line.split()
            name = w[1]
            value = w[3]
            stat[name] = float(value)
        if 'Track types:' in line:
            read_track = True
    return stat


def add_diff(df, tag, vdiff):
    v = []
    for s in df:
        v.append(df[s][tag])
    ref = float(v[0])
    # print('ref', tag, ref, v)
    max_diff = 0.0
    max_val = ''
    for x in v:
        # print('x', x)
        diff = (ref - float(x)) / ref
        # print(diff)
        if np.fabs(diff) > max_diff:
            max_diff = diff
            max_val = Box({'tag': tag, 'v': v, 'ref': ref, 'x': x, 'diff': diff})
    if max_val != '':
        # print(f'Max diff {max_val.tag} : {max_val.diff * 100.0:.2f}% ')
        vdiff.append(max_val.diff * 100)
    else:
        vdiff.append(0)


def analyse_one_folder(folder):
    print(folder)

    # compare stat files
    l = {}
    l['opt4_e+'] = read_stat_file(f'{folder}/stat1.txt')
    l['QGSP_e+'] = read_stat_file(f'{folder}/stat2.txt')
    l['opt4_ion'] = read_stat_file(f'{folder}/stat3.txt')
    l['QGSP_ion'] = read_stat_file(f'{folder}/stat4.txt')

    df = pd.DataFrame(l)
    df = df.fillna(0)

    # pd.set_option("display.max_rows", None)
    # pd.set_option('display.max_columns', 700)
    # pd.set_option('display.expand_frame_repr', False)
    df = df.transpose()
    #pd.options.display.float_format = '{:.0f}'.format
    df['duration'] = df['duration'].map('{:,.2f}'.format)
    df = df.transpose()
    # print(df)

    diff = []
    for tag in l['opt4_e+']:
        add_diff(df, tag, diff)
    for tag in l['QGSP_ion']:
        if tag not in l['opt4_e+']:
            diff.append(0)
    df['max_diff'] = diff

    drun = np.abs(float(df['max_diff']['run']))
    devent = np.abs(float(df['max_diff']['event']))
    dep = np.abs(float(df['max_diff']['e+']))
    dgamma = np.abs(float(df['max_diff']['gamma']))
    maxd = max(drun, devent, dep, dgamma)

    df['max_diff'] = df['max_diff'].map('{:,.1f}%'.format)
    print(df)
    print(f'Max difference (run/event/e+/gamma) is {maxd:.2f}%')

    if maxd < 8.0:
        return True
    return False


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    analyse_command_line()

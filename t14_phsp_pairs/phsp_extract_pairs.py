#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import click
import gatetools.phsp as phsp
import numpy as np
import uproot

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('root_filename', nargs=1)
@click.option('--output', '-o', default='auto', help='output filename (npy)')
def go(root_filename, output):
    # read the root file
    try:
        f = uproot.open(root_filename)
    except Exception:
        print(f'Cannot open the file {root_filename}. Is this a root file ?')
        exit(-1)

    if output == 'auto':
        output = os.path.splitext(root_filename)[0] + '_pairs.npy'
    print(f'Input root file {root_filename}')
    print(f'Output npy file {output}')

    phspf = f['PhaseSpace']
    phspf.show()

    # names of the branches
    sekine = 'Ekine'
    if sekine not in phspf:
        sekine = 'KineticEnergy'
    sx = 'X'
    sy = 'Y'
    sz = 'Z'
    if sx not in phspf:
        sx = 'PostPosition_X'
        sy = 'PostPosition_Y'
        sz = 'PostPosition_Z'
    sdx = 'dX'
    sdy = 'dY'
    sdz = 'dZ'
    if sdx not in phspf:
        sdx = 'PostDirection_X'
        sdy = 'PostDirection_Y'
        sdz = 'PostDirection_Z'

    st = 'Time'

    print('Reading number of events: ', phspf['EventID'].num_entries)
    event_id = phspf['EventID'].array(library='numpy')
    ekine = phspf[sekine].array(library='numpy')
    posx = phspf[sx].array(library='numpy')
    posy = phspf[sy].array(library='numpy')
    posz = phspf[sz].array(library='numpy')
    dx = phspf[sdx].array(library='numpy')
    dy = phspf[sdy].array(library='numpy')
    dz = phspf[sdz].array(library='numpy')
    print('Warning: time is considered as GlobalTime')
    time = phspf[st].array(library='numpy')
    weight_enabled = False
    if 'Weight' in phspf:
        weights = phspf['Weight'].array(library='numpy')
        weight_enabled = True
        print('weights', len(weights))

    print('count nb of pairs ...')
    unique, counts = np.unique(event_id, return_counts=True)
    print(unique, counts)
    n = len(event_id)  # .num_entries

    u, c = np.unique(counts, return_counts=True)
    max_u = u[len(u) - 1]

    x = []
    i = 0
    for eid in event_id:
        # look for same event ID in the XX (max_u) next values
        r = event_id[i:i + max_u]
        # print('r', eid, r)
        idx = np.where(r == eid)[0]
        # if we dont have 2 events, we ignore ftm
        # however it can be 3 or more ! FIXME !!!!
        if i % 1e5 == 0:
            print(f' {i}/{n} {i / n * 100:1f}%: event id {eid} ; idx={idx}')
        if len(idx) != 2:
            i = i + 1
            continue
        # Get the energies of the two events
        idx1 = i + idx[0]
        idx2 = i + idx[1]
        # print('idx ', idx1, idx2)
        e1 = ekine[idx1]
        e2 = ekine[idx2]
        # print(f' {eid} {i} --> {event_id[i + idx[0]]} {event_id[i + idx[1]]} => {e1} {e2}')
        if weight_enabled:
            x.append([e1, e2,
                      posx[idx1], posy[idx1], posz[idx1],
                      posx[idx2], posy[idx2], posz[idx2],
                      dx[idx1], dy[idx1], dz[idx1],
                      dx[idx2], dy[idx2], dz[idx2],
                      time[idx1], time[idx2],
                      weights[idx1], weights[idx2]])
        else:
            x.append([e1, e2,
                      posx[idx1], posy[idx1], posz[idx1],
                      posx[idx2], posy[idx2], posz[idx2],
                      dx[idx1], dy[idx1], dz[idx1],
                      dx[idx2], dy[idx2], dz[idx2],
                      time[idx1], time[idx2]])
        i = i + 1

    print('Pairs: ', len(x))
    keys = ['E1', 'E2',
            'X1', 'Y1', 'Z1', 'X2', 'Y2', 'Z2',
            'dX1', 'dY1', 'dZ1', 'dX2', 'dY2', 'dZ2',
            't1', 't2']
    if weight_enabled:
        keys.append('w1')
        keys.append('w2')
    print('Keys', keys)
    x = np.reshape(x, newshape=(len(x), len(keys)))
    print(x.shape)
    phsp.save_npy(output, x, keys)


# --------------------------------------------------------------------------
if __name__ == '__main__':
    go()

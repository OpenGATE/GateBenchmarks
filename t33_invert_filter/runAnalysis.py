#!/usr/bin/env python3
# -----------------------------------------------------------------------------
#   Copyright (C): OpenGATE Collaboration
#   This software is distributed under the terms
#   of the GNU Lesser General  Public Licence (LGPL)
#   See LICENSE.md for further details
# -----------------------------------------------------------------------------

import click
import os
import numpy as np
import gatetools as gt
import matplotlib.pyplot as plt

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('output_folders',
                nargs=-1,
                required=True,
                type=click.Path(exists=True, file_okay=True, dir_okay=True))
                
def analyse_command_line(output_folders, **kwargs):
    # logger
    gt.logging_conf(**kwargs) 
    # Run the analysis with the command line (click)
    # the return code is 0 (fail) or 1 (success)
    r = analyse_all_folders(output_folders)
    print(f'Last test return is: {r}')


def analyse_all_folders(output_folders):
    r = True
    for folder in output_folders:
        folder_basename = os.path.basename(folder)
        if folder_basename.split("-")[-1] != "output":
            if float(folder_basename.split("-")[-1]) < 9.4:
                continue # feature add in 9.3
        r = r and analyse_folder(folder)
    return r

def analyse_folder(folder):
    r = True
    for filter_id in range(12):
        filepath = os.path.join(folder, f"filter_id_{filter_id}.hits.npy")
        if os.path.exists(filepath):
            data = get_primary(np.load(filepath))
        elif filter_id != 8 and filter_id != 9:
            raise(f"File {filepath} does not exist")
        
        if filter_id == 0 or filter_id == 1:
            r = r and analyse_angle(data, filter_id == 1)

        if filter_id == 2 or filter_id == 3:
            r = r and analyse_energy(data, filter_id == 3)
        
        if filter_id == 4 or filter_id == 5:
            r = r and analyse_material(data, filter_id == 5)

        if filter_id == 6 or filter_id == 7:
           r = r and  analyse_volume(data, filter_id == 7)

        if filter_id == 8 or filter_id == 9:
            r = r and analyse_ID(data, filter_id == 9)

        if filter_id == 10 or filter_id == 11:
            r = r and analyse_particle(data, filter_id == 11)
    return r

def get_primary(data):
    is_primary = data["nCrystalRayleigh"]==0 
    is_primary = np.logical_and(is_primary, data["nCrystalCompton"]==0)
    is_primary = np.logical_and(is_primary, data["nPhantomRayleigh"]==0)
    is_primary = np.logical_and(is_primary, data["nPhantomCompton"]==0)
    
    return np.compress(is_primary,data)



def analyse_angle(data, invert:bool):
    distance2 = data["posX"]**2 + data["posY"]**2
    radius2 = 150**2*np.tan(np.pi/6)**2
    if invert:
        return (distance2.max() - radius2 < 1)
    else:
        return (distance2.min() - radius2 > -1)

    
def analyse_energy(data, invert:bool):
    if invert:
        return data["edep"].min() > 0.195
    else:
        return data["edep"].max() < 0.195

def plot_scatter(data, invert:bool, name):
    plt.figure()
    plt.scatter(data["posX"], data["posY"])
    plt.axis('equal')
    plt.savefig(f"{name}_{invert}.svg")

def analyse_material(data, invert:bool):
    if invert:
        return data["posX"].min() > 0
    else:
        return data["posX"].max() < 0
        

def analyse_volume(data, invert:bool):
    if invert:
        return data["posX"].min() > 0
    else:
        return data["posX"].max() < 0
    
def analyse_ID(data, invert:bool):
    return True

def analyse_particle(data, invert:bool):

    # first remove secondary by bremsstrahlung effect
    event_id = data["eventID"]
    dupulicate = np.insert((event_id[1:]-event_id[:-1] == 0), 0, False)
    data = np.compress(np.logical_not(dupulicate),data)
    
    if invert:
        return data["PDGEncoding"].min()==11 and data["PDGEncoding"].max()==11
    else:
        return data["PDGEncoding"].min()==22 and data["PDGEncoding"].max()==22


    


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    analyse_command_line(["output"])

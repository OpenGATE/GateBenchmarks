import numpy as np
from scipy import interpolate
import click
import gatetools as gt

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
    print(f'Final test return is: {r}')

# -----------------------------------------------------------------------------
def analyse_all_folders(output_folders):
    # sort folders: the current simple 'output' must be at the end
    events = np.loadtxt('output/genericMoveTest_Coincidences.dat', usecols=(0, 1, 2, 3, 4, 5, 6))

    detector_sim = events[:, (3, 4, 5, 6)]
    source_sim = events[:, (3, 0, 1, 2)]
    source_real = np.loadtxt('data/moveSource.placements', skiprows=8, usecols=(0, 5, 6, 7))
    detector_real = np.loadtxt('data/moveDetector.placements', skiprows=8, usecols=(0, 5, 6, 7))
    source_bools = np.zeros(len(source_sim[:, 0]))
    detector_bools = np.zeros(len(detector_sim[:, 0]))
    for i in range(len(source_sim[:, 0])):
        source_index = np.where(source_real[:, 0] <= source_sim[i, 0])
        if source_sim[i, 3]-source_real[source_index[0][-1], 3] > 1*10**-10:
            source_bools[i] = False
        else:
            source_bools[i] = True

        detector_index = np.where(detector_real[:, 0] <= detector_sim[i, 0])
        if np.abs(detector_sim[i, 1])-np.abs(detector_real[detector_index[0][-1], 1]+87) >= 16:
            detector_bools[i] = False
        else:
            detector_bools[i] = True

    print('Source Movement Test Pass: '+str(np.all(source_bools==True)))
    print('Detector Movement Test Pass: '+str(np.all(detector_bools==True)))
    return(np.all(source_bools==True) and np.all(detector_bools==True))


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    analyse_command_line()

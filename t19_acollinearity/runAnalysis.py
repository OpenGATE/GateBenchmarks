"""
Last modified on Wed Nov 24 18:36:10 2021

@author: mlenz

Update path to output files (main_dir).
"""

import os
import numpy as np
import matplotlib.pylab as plt
from scipy.optimize import curve_fit
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
    output_folders = list(output_folders)
    if 'output' in output_folders:
        output_folders.pop(output_folders.index('output'))
    output_folders.append('output')
    for folder in output_folders:
        if not os.path.isdir(folder):
            continue
        r = analyse_one_folder(folder)
    return r

# -----------------------------------------------------------------------------
def analyse_one_folder(output_folder):
    pathAcoF18 = os.path.join(output_folder, "dataAcoF18.bin")
    pathAcoBTB = os.path.join(output_folder, "dataAcoBTB.bin")

    # Read the simulation data
    F18_aco_angle = process_binary(pathAcoF18)
    BTB_aco_angle = process_binary(pathAcoBTB)

    # single output figure
    f = plt.figure(figsize=(10, 9))
    ax1 = f.add_subplot(221)
    f.tight_layout(pad = 5.0)
    ax1.set_title('BackToBack acollinearity')
    a, b, c = plot_fit_histogram(180-BTB_aco_angle, ax1, with_text = True)
    plt.savefig("acoDistComparison.png")
    plt.close()
    print("folder: " + output_folder)
    print('    amplitude: ' + str(round(a, 2)) + ' < 4.00 ')
    print('    abs(mean): ' + str(abs(round(b, 2))) + ' < 0.02 ')
    print('    sigma: ' + str(round(c, 2)) + ' < 0.25 ')
    returnBool = True
    if (abs(a) >= 4.00):
       returnBool = False
    if (abs(b) >= 0.02):
       returnBool = False
    if (abs(c) >= 0.25):
       returnBool = False
    print('    ' + str(returnBool))
    return(returnBool)

def process_binary(filename):
    data = np.fromfile(filename, dtype = float)

    # Angle between the vectors as obtained from the angle() function
    aco_angle = data*180/np.pi

    return(aco_angle)

# plot histogram and fit Gaussian
def gaus(x,a,m,sigma):
    return a*np.exp(-(x-m)**2/(2*sigma**2))

def plot_fit_histogram(data,ax, with_text=True):
    counts, _, axes = ax.hist(data,density=True, bins=100)
    x = np.linspace(min(data), max(data), 100)
    p0 = [3, 0, 0.5]
    popt,pcov = curve_fit(gaus,x,counts,p0=p0)
    ax.plot(x, gaus(x,popt[0],popt[1],popt[2]))
    ax.set_xlabel('acollinearity [°]')
    ax.set_ylabel('frequency [AU]')
    textstr = '\n'.join((r'$a=%.2f$' % (popt[0], ), r'$\mu=%.2f$' % (popt[1], ), r'$\sigma=%.2f$' % (popt[2], )))

    if with_text:
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax.text(0.7, 0.95, textstr, transform=ax.transAxes, fontsize=14,
                verticalalignment='top', bbox=props)

    return popt[0], popt[1], popt[2]

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    analyse_command_line()


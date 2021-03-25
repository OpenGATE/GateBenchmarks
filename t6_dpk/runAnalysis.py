#!/usr/bin/env python3

import gatetools as gt
import click
import logging
import numpy as np
import matplotlib.pyplot as plt
import gzip

logger = logging.getLogger(__name__)


def analyse_one_folder(folder, ax1, is_first):
    print(folder)
    E = 1
    histories = 5000
    rE = 4.367
    bins = 24
    path = f'{folder}/10000_1MeV_opt4_1um_nostepmax_test.hits.npy.gz'

    f = gzip.GzipFile(path, "r")
    data = np.load(f)
    posX = data['posX']
    posY = data['posY']
    posZ = data['posZ']
    edep = data['edep']
    print(f'size : {posX.size}')

    r_egs1MeV, dpk_egs1MeV = np.loadtxt("EGSnrc/1MeV-EGSnrc.ascii", delimiter=',', unpack=True)
    # print(r_egs1MeV)
    # print(dpk_egs1MeV)

    # 24 shells
    radius_sphere = []
    bin_size = rE * (1.2 / bins)
    for i in range(1, bins + 1):
        radius_sphere.append(i * bin_size)
    # print(radius_sphere)
    ##########################################################
    radius_middle = []
    for i in range(0, bins):
        radius_middle.append((radius_sphere[0] / 2) + (i * bin_size))
    # print(radius_middle)

    volume_sphere = [(4 / 3) * np.pi * (j) ** 3 for j in radius_sphere]
    # print(volume_sphere)
    ##########################################################
    density = 1
    masse_sphere = [density * k for k in volume_sphere]
    # print(masse_sphere)
    masse_sphere_min = masse_sphere[0]
    # print(masse_sphere_min)

    masse_shell = []
    for i in range(len(masse_sphere) - 1):
        masse_shell.append(masse_sphere[i + 1] - masse_sphere[i])
    # print(masse_shell)

    masse_shell_final = [masse_sphere_min] + masse_shell
    # print(masse_shell_final)
    ###########################################################
    spherepos = [np.sqrt((i) ** 2 + (j) ** 2 + (k) ** 2) for i, j, k in zip(posX, posY, posZ)]

    # print('spherepos:', len(spherepos))
    # print('edep:', len(edep))
    # print('posX:', len(posX))
    # print('posY:', len(posY))
    # print('posZ:', len(posZ))
    ##########################################################################
    edep_sphere = []
    i = 0
    for i in range(len(radius_sphere)):
        num = 0
        somme = 0
        mean = 0
        for num in range(len(spherepos)):
            if (spherepos[num] <= (radius_sphere[i])):
                somme += edep[num]
        print(f'radius_sphere = {radius_sphere[i]:.3f}    Edep_sum = {somme:.3f}')
        edep_sphere.append(somme)
    # print(edep_sphere)
    edep_sphere_min = edep_sphere[0]
    # print(edep_sphere_min)

    edep_shell = []
    # print(len(edep_sphere))
    for i in range(len(edep_sphere) - 1):
        edep_shell.append(edep_sphere[i + 1] - edep_sphere[i])
    # print(edep_shell)
    edep_shell_final = [edep_sphere_min] + edep_shell
    # print(edep_shell_final)
    ############################################################################################""
    dose_history_shell = [i / histories / j for i, j in zip(edep_shell_final, masse_shell_final)]
    # print(dose_history_shell)

    J_history_shell = [(4 * np.pi) * (rE / E) * (i ** 2) * (j) for i, j in zip(radius_middle, dose_history_shell)]
    # print(J_history_shell)

    x = []
    x = [i / rE for i in radius_middle]
    diff_rel = [abs(((i - j) / j) * 100) for i, j in zip(J_history_shell, dpk_egs1MeV)]
    # print(x)

    ax1.set_xlabel('r/r0')
    ax1.set_ylabel('J(r,r/r0)')
    ax1.plot(x, J_history_shell, label=f'GATE {folder}')
    if is_first:
        ax1.plot(r_egs1MeV, dpk_egs1MeV, label='EGSnrc', linewidth=2)
    ax1.legend(loc="upper right")
    plt.title('DPK 1 MeV')
    ax1.tick_params(axis='y')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:red'
    ax2.set_ylabel('Relative difference(%)', color=color)  # we already handled the x-label with ax1
    ax2.plot(x, diff_rel, color=color)
    ax2.set_ylim([0, 100])
    ax2.tick_params(axis='y', labelcolor=color)

    # tolerance
    # print(x)
    # print(diff_rel)
    d = diff_rel[1:17]
    # print(d)
    d95 = np.percentile(d, 95)
    print(f'95percentile difference {d95:.3f}% ; tolerance is 10.0%')
    return d95 < 10.0


# -----------------------------------------------------------------------------
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('output_folders',
                nargs=-1,
                required=True,
                type=click.Path(exists=True, file_okay=True, dir_okay=True))
@gt.add_options(gt.common_options)
def analyse_click(output_folders, **kwargs):
    """
    DPK analysis
    """
    analyse_all_folders(output_folders)


def analyse_all_folders(output_folders, **kwargs):
    # logger
    gt.logging_conf(**kwargs)

    fig, ax = plt.subplots()
    is_first = True
    r = None
    for folder in output_folders:
        r = analyse_one_folder(folder, ax, is_first)
        is_first = False

    fig.tight_layout()
    plt.savefig(f'output.pdf')
    # plt.show()

    print(f'Last result : {r}')
    return r


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    analyse_click()

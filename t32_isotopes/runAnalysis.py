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
import math as m

logger = logging.getLogger(__name__)

# Toleranceprevious
TOL = 10

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
	materials = ["C", "C14"]
	physics = "QGSP_BIC_HP"
	number_particles = "500K"

	# compare with the previous folder
	previous_folder = None
	r = None
	# sort folders: the current simple 'output' must be at the end
	output_folders = list(output_folders)
	if 'output' in output_folders:
		output_folders.pop(output_folders.index('output'))
	output_folders.append('output')
	for folder in output_folders:
		if not os.path.isdir(folder):
			continue
		r = analyse_one_folder(folder, previous_folder, materials, physics, number_particles)
		previous_folder = folder
	return r

def analyse_one_folder(folder, previous_folder, materials, physics, number_particles):
	rg = analyse_one_curve(folder, previous_folder, materials, physics, number_particles)
	# return error if one is failed
	if not rg :
		return False
	return True

def analyse_one_curve(folder, previous_folder, materials, physics, number_particles):
	filename_nat = getName(materials[0], physics, number_particles)
	filename_iso = getName(materials[1], physics, number_particles)

	fNat = os.path.join(folder, filename_nat)
	fIso = os.path.join(folder, filename_iso)
	if previous_folder:
		previous_fNat = os.path.join(previous_folder, filename_nat)
		previous_fIso = os.path.join(previous_folder, filename_iso)
		r = augmentation_index(fNat, fIso, previous_fNat, previous_fIso)
		return r
	return True

#===================================
def getName(material, physics, number_particles):
	return "part-" + material + "-" + physics + "-" + number_particles + ".txt"

def augmentation_index(fNat, fIso, ref_fNat, ref_fIso):
	with open(fNat) as ifs:
		nbNeutronsNat = int(ifs.readline().split('\n')[0].split(' ')[-1])
	with open(fIso) as ifs:
		nbNeutronsIso = int(ifs.readline().split('\n')[0].split(' ')[-1])

	with open(ref_fNat) as ifs:
		nbNeutronsNat_ref = int(ifs.readline().split('\n')[0].split(' ')[-1])
	with open(ref_fIso) as ifs:
		nbNeutronsIso_ref = int(ifs.readline().split('\n')[0].split(' ')[-1])

	if nbNeutronsNat_ref == 0:
		print("Too little neutrons in reference data")
		nbNeutronsNat_ref += 0.01
	if nbNeutronsNat == 0:
		print("Too little neutrons")
		nbNeutronsNat += 0.01

	ratio_ref = (nbNeutronsIso_ref - nbNeutronsNat_ref)/nbNeutronsNat_ref*100
	ratio = (nbNeutronsIso - nbNeutronsNat)/nbNeutronsNat*100


	Ni = nbNeutronsIso_ref; sigI = m.sqrt(Ni)
	Nn = nbNeutronsNat_ref; sigN = m.sqrt(Nn)
	S = Ni - Nn ; sigS = m.sqrt(pow(sigN,2) + pow(sigI, 2))
	sig = m.sqrt(pow(sigN/Nn,2) + pow(sigS/S,2))*100

	TOL = 10*sig

	print("Ratio : {} %".format("%.3f"%ratio), "\t| Previous ratio : {} %".format("%.3f"%ratio_ref), "\t| diff. : %.3f"%(ratio - ratio_ref), "\t(tol. : %.3f)"%TOL)

	if (ratio > ratio_ref-TOL) and (ratio < ratio_ref+TOL):
		return True
	return False


# -----------------------------------------------------------------------------
if __name__ == '__main__':
	analyse_command_line()

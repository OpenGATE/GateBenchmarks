#!/usr/bin/env python3

import os
import click


@click.command()
@click.argument('output_folders', nargs=-1, required=True, type=click.Path(exists=True, dir_okay=True))
def analyse_click(output_folders):
	r = analyse_all_folders(output_folders)
	print(f'Test result: {r}')


def analyse_all_folders(output_folders):
	r = True
	for folder in output_folders:
		r = r and analyse_folder(folder)

	return r


def analyse_folder(folder):
	f1 = os.path.join(folder, 'target1_energyEdepSpectrum.txt')
	f2 = os.path.join(folder, 'target2_energyEdepSpectrum.txt')
	f3 = os.path.join(folder, 'target3_energyEdepSpectrum.txt')

	try:
		f1 = open(f1)
		f2 = open(f2)
		f3 = open(f3)
	except Exception:
		print(f'One of ({f1}, {f2}, {f3}) does not exist?')
		exit(1)

	return analyse(f1, f2, f3)


def load_file(f):
	lines = f.readlines()
	data = {}
	is_data = False
	for line in lines:
		line = line.rstrip()
		if is_data:
			values = line.split(' ')
			data[float(values[0])] = float(values[2])
		elif line == '2 0':
			is_data = True

	return data


def find_min_energy(v):
	m = max(v.keys())
	for k, v in v.items():
		if v != 0 and k < m:
			m = k

	return m


def analyse(f1, f2, f3):
	v1 = load_file(f1)
	v2 = load_file(f2)
	v3 = load_file(f3)
	
	print(v2)
	m1 = find_min_energy(v1)
	m2 = find_min_energy(v2)
	m3 = find_min_energy(v3)
        
	return m1 < .0025 and m2 >= .0005 and m3 < .0025


if __name__ == '__main__':
	analyse_click()

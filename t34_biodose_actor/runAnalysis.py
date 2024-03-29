#!/usr/bin/env python3

import click
import numpy as np
import itk
import matplotlib as mpl
import matplotlib.pyplot as plt


def load(mhd: str):
	img = itk.imread(mhd)
	data = itk.GetArrayFromImage(img)
	return data[:, 0, 0]


@click.command()
@click.argument('output_folders', nargs=-1, required=True, type=click.Path(exists=True, dir_okay=True))
@click.option('--figures', is_flag=True)
@click.option('--show', is_flag=True)
def analyse_click(output_folders, figures: bool, show: bool):
	if figures:
		mpl.use('tkagg')

	r = True
	for output_folder in output_folders:
		for particle_name in ["carbon", "proton"]:
			cur_r = analyse_particle(output_folder, particle_name, figures, show)
			if not cur_r:
				print(f"Test failed for: {output_folder}, {particle_name}")

		r = r and cur_r

	print(f'Test result: {r}')


def analyse_particle(output_folder, particle_name, figures, show):
	dose = load(f"{output_folder}/dose_{particle_name}-Dose.mhd")
	dose_from_bio = load(f"{output_folder}/biodose_{particle_name}_dose.mhd")
	biodose = load(f"{output_folder}/biodose_{particle_name}_biodose.mhd")

	dose_err = np.divide(np.abs(dose - dose_from_bio), dose, out=np.zeros_like(dose), where=dose == 0)
	dose_mean_err = np.mean(dose_err)
	dose_ok = dose_mean_err < .05
	# print(f"dose relative difference: (mean) {dose_mean_err*100:.2f}%, (max) {np.max(dose_err)*100:.2f}%")

	rbe = np.divide(biodose, dose_from_bio, out=np.ones_like(biodose), where=dose_from_bio != 0)
	min_rbe = np.min(rbe)
	rbe_ok = min_rbe >= 1
	# print(f"RBE always > 1: {rbe_ok}")

	if figures:
		fig, ax = plt.subplots(figsize=(6.5, 5), dpi=300)
		ax.set_xlabel('depth (mm)')
		ax.set_ylabel('dose (Gy)')

		ax.plot(dose, color='blue', label='dose', linestyle='dashed')
		ax.plot(dose_from_bio, color='blue', label='dose (from biodose actor)')
		ax.plot(biodose, color='orange', label='biodose')

		plt.legend()

		plt.title(f"Data for {output_folder}, {particle_name}")

		plt.tight_layout()
		plt.savefig(f"{output_folder}/fig_{particle_name}.pdf")
		if show:
			plt.show()
		plt.close(fig)

	return dose_ok and rbe_ok


if __name__ == '__main__':
	analyse_click()

#!/usr/bin/env python3
import gatetools as gt
import os
import click
import matplotlib.pyplot as plt
from enum import IntEnum
import uproot
import numpy as np

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('output_folders',
                nargs=-1,
                required=True,
                type=click.Path(exists=True, file_okay=True, dir_okay=True))
@gt.add_options(gt.common_options)
def analyse_click(output_folders, **kwargs):
    r = analyse_one_folder(output_folders[0])
    print(f'Last test return is: {r}')

def analyse_all_folders(output_folders):
  r = analyse_one_folder(output_folders[0])
  print(f'Last test return is: {r}')

class SimulatedSource(IntEnum):
  UNKNOWN = 0
  PPS = 1
  PPSPROMPT = 2
  OPS = 3
  OPSPROMPT = 4

def check_tree(tree, requested_st, requested_dt, check_prompt_gammas):
  n_st = sum(1 for st in tree["sourceType"] if st == requested_st)
  n_dt = sum(1 for dt in tree["decayType"] if dt == requested_dt)
  n_annihilation = sum(1 for gt in tree["gammaType"] if gt == 2)
  n_prompt = 0
  if check_prompt_gammas:
    n_prompt = sum(1 for gt in tree["gammaType"] if gt == 3)
  n_gt = n_annihilation + n_prompt
  if any(n_st != n for n in [n_dt,n_gt]):
    return False, 0, 0
  return True, n_annihilation, n_prompt

def get_edep_annihilation_gammas(tree, array_size):
  edep_array = np.empty(array_size, dtype=float)
  eindex = 0
  for index, gamma_type in enumerate(tree["gammaType"]):
    if gamma_type == 2:
      edep_array[eindex] = tree["edep"][index]
      eindex += 1
  return edep_array

def get_edep_both_gammas_types(tree, annihilation_array_size, prompt_array_size):
  edep_annihilation_array = np.empty(annihilation_array_size, dtype=float)
  edep_prompt_array = np.empty(prompt_array_size, dtype=float)
  aindex = 0
  pindex = 0
  for index, gamma_type in enumerate(tree["gammaType"]):
    if gamma_type == 2:
      edep_annihilation_array[aindex] = tree["edep"][index]
      aindex += 1
    elif gamma_type == 3:
      edep_prompt_array[pindex] = tree["edep"][index]
      pindex += 1
  return edep_annihilation_array, edep_prompt_array


def analyse_pps(tree, edep_plots):
  is_correct, n_annihilation, _ = check_tree(tree, 2, 1, False)
  if is_correct:
    edep_plots["dE_pPs_annihilation"] = get_edep_annihilation_gammas(tree, n_annihilation)
  return is_correct

def analyse_ppsprompt(tree, edep_plots):
  is_correct, n_annihilation, n_prompt = check_tree(tree, 2, 2, True)
  if is_correct:
    edep_annihilation, edep_prompt = get_edep_both_gammas_types(tree, n_annihilation, n_prompt)
    edep_plots["dE_pPsPrompt_annihilation"] = edep_annihilation
    edep_plots["dE_pPsPrompt_prompt"] = edep_prompt
  return is_correct

def analyse_ops(tree, edep_plots):
  is_correct, n_annihilation, _ = check_tree(tree, 3, 1, False)
  if is_correct:
    edep_plots["dE_oPs_annihilation"] = get_edep_annihilation_gammas(tree, n_annihilation)
  return is_correct

def analyse_opsprompt(tree, edep_plots):
  is_correct, n_annihilation, n_prompt = check_tree(tree, 3, 2, True)
  if is_correct:
    edep_annihilation, edep_prompt = get_edep_both_gammas_types(tree, n_annihilation, n_prompt)
    edep_plots["dE_oPsPrompt_annihilation"] = edep_annihilation
    edep_plots["dE_oPsPrompt_prompt"] = edep_prompt
  return is_correct

def analyse_one_file(folder, filename,sim_source,edep_plots):
  file_path = os.path.join(folder, filename)
  branches = ["edep","sourceType","decayType","gammaType"]
  tree = uproot.open(file_path)['Hits'].arrays(branches,library="numpy")
  if sim_source == SimulatedSource.PPS:
    return analyse_pps(tree, edep_plots)
  if sim_source == SimulatedSource.PPSPROMPT:
    return analyse_ppsprompt(tree, edep_plots)
  if sim_source == SimulatedSource.OPS:
    return analyse_ops(tree, edep_plots)
  if sim_source == SimulatedSource.OPSPROMPT:
    return analyse_opsprompt(tree, edep_plots)
  return False

def analyse_one_folder(folder):
  edep_plots  = dict()
  check_results = list()
  check_results.append(analyse_one_file(folder, "pPs.root",SimulatedSource.PPS,edep_plots))
  check_results.append(analyse_one_file(folder, "pPs_prompt.root",SimulatedSource.PPSPROMPT,edep_plots))
  check_results.append(analyse_one_file(folder, "oPs.root",SimulatedSource.OPS,edep_plots))
  check_results.append(analyse_one_file(folder, "oPs_prompt.root",SimulatedSource.OPSPROMPT,edep_plots))

  if not all(cr for cr in check_results):
    return False

  bins_annihilation = [round(0.001*i,2) for i in range(0,400)]
  bins_prompt = [round(0.001*i,2) for i in range(0,1000)]

  _, ax = plt.subplots(ncols=3, nrows=2, figsize=(15, 10))
  ax[0,0].hist(edep_plots["dE_pPs_annihilation"], bins_annihilation)
  ax[0,1].hist(edep_plots["dE_pPsPrompt_annihilation"], bins_annihilation)
  ax[0,2].hist(edep_plots["dE_pPsPrompt_prompt"], bins_prompt)

  ax[1,0].hist(edep_plots["dE_oPs_annihilation"], bins_annihilation)
  ax[1,1].hist(edep_plots["dE_oPsPrompt_annihilation"], bins_annihilation)
  ax[1,2].hist(edep_plots["dE_oPsPrompt_prompt"], bins_prompt)

  plt.savefig('output.pdf')
  plt.show()

  return True

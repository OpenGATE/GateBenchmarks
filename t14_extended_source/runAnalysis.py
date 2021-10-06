#!/usr/bin/env python3
"""
Benchmark for GateExtendedVSource module (emission of gammas from positronium decay).
"""
import gatetools as gt
import os
import click
import matplotlib.pyplot as plt
from enum import IntEnum
import uproot
import numpy as np
from scipy import stats
import csv
from pathlib import Path

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('output_folders',
                nargs=-1,
                required=True,
                type=click.Path(exists=True, file_okay=True, dir_okay=True))
@gt.add_options(gt.common_options)
def analyse_click(output_folders, **kwargs):
  """
  Method called by runBenchmark script.

  Parameters
  ----------
  output_folders : list
   list of output folders
  """
  r = analyse_one_folder(output_folders[0])
  print(f'Last test return is: {r}')

def analyse_all_folders(output_folders):
  """
  Method calls by runBenchmark script.

  Parameters
  ----------
  output_folders : list
   list of output folders

  Returns
  -------
  benchark finihed without errors : bool
  """
  #We have only one output folder for this benchmark
  return analyse_one_folder(output_folders[0])

class GammaType(IntEnum):
  """
  Type of gamma emitted by ExtendedVSource.

  Attributes
  ----------
  ANNIHILATIONGAMMA - annihilation gamma (from positronium decay)
  PROMPTGAMMA - deexcitation gamma (emitted from the atom which is a source of e+ just before the beta+ decay)
  """
  ANNIHILATIONGAMMA = 2
  PROMPTGAMMA = 3

class SourceType(IntEnum):
  """
  Type of positronium.

  Attributes
  ----------
  PARAPOSITRONIUM - pPs (source of 2 annihilation gammas)
  ORTHOPOSITRONIUM - oPs (source of 3 annihilation gammas)
  """
  PARAPOSITRONIUM = 2
  ORTHOPOSITRONIUM = 3

class DecayType(IntEnum):
  """
  Type of positronium decay.

  Attributes
  ----------
  STANDARD - only emitted annihilation gammas from positronium decay
  WITHDEEXCITATION - atom deexcitation (prompt) gamma and annihilation gammas emitted
  """
  STANDARD = 1
  WITHDEEXCITATION = 2

def get_edep_plot_data(tree, source_type, decay_type):
  """
  Collects energies depositions from annihilation and prompt gammas.
  Counts entries for given model (source_type and decay_type).

  Parameters
  ----------
  tree : uproot tree
  source_type : sourceType
  decay_type : decayType

  Returns
  -------
  energies deposited by annihilation gammas, energies deposited by prompt gammas, model counted entries : np.array, np.array, int
  """
  edep_annihilation_recs = list()
  edep_prompt_recs = list()
  expected_entries = 0
  for index, gamma_type in enumerate(tree["gammaType"]):
    if tree["sourceType"][index] == source_type and tree["decayType"][index] == decay_type:
      expected_entries += 1
    if gamma_type == GammaType.ANNIHILATIONGAMMA:
      edep_annihilation_recs.append(tree["edep"][index])
    elif gamma_type == GammaType.PROMPTGAMMA:
      edep_prompt_recs.append(tree["edep"][index])
  return np.array(edep_annihilation_recs, dtype=np.float32), np.array(edep_prompt_recs, dtype=np.float32), expected_entries

def perform_ks_test(edeps, gamma_type, source_type, decay_type):
  """
  Performs the two-sample Kolmogorov-Smirnov test for given data from simulation and reference data (data/ directory).
  Null hypothesis: two distributions are identical.

  Parameters
  ----------
  edep : np.array
   energy depositions
  gamma_type : GammaType
  source_type : SourceType
  decayType : DecayType

  Returns
  -------
  passed test : bool
  """
  source_strings = {SourceType.PARAPOSITRONIUM: "pPs", SourceType.ORTHOPOSITRONIUM: "oPs"}
  decay_strings = {DecayType.STANDARD:"",DecayType.WITHDEEXCITATION:"Prompt"}
  gamma_type_strings = {GammaType.ANNIHILATIONGAMMA:"-annihilation-gamma",GammaType.PROMPTGAMMA:"-prompt-gamma"}
  script_dir_path = Path(os.path.dirname(os.path.abspath(__file__)))
  tests_data_dir_path = script_dir_path/"data"
  file_path = tests_data_dir_path/"".join([source_strings[source_type],decay_strings[decay_type],gamma_type_strings[gamma_type],".csv"])
  with file_path.open(mode="r") as file:
    csvr = csv.reader(file)
    next(csvr)
    test_edeps = list()
    for edep in csvr:
      test_edeps.append(float(edep[0]))
    test_edeps = np.array(test_edeps, dtype=np.float32)
  _, pvalue = stats.ks_2samp(edeps, test_edeps)
  #in scipy.stats.ks_2samp a hypothesis is for two-sided test is: two distributions are identical, F(x)=G(x) for all x
  #We can say with certainty that our hypothesis is not true for pvalue equals 5% or lower.
  pvalue_threshold = 0.05
  return pvalue > pvalue_threshold


def analyse_model(tree, edep_plots, source_type, decay_type):
  """
  Checks if data in tree are correct:
  * number of entries from prompt and annihilation gammas equals entries from the model
  * energy depositions records passed Kolmogorov–Smirnov test

  Parameters
  ----------
  tree : uproot tree
  edep_plots : dict
   for given model new records are added by this method
  source_type : sourceType
  decay_type : decayType

  Returns
  -------
  correct data (tests passed) : bool
  """
  source_strings = {SourceType.PARAPOSITRONIUM: "pPs", SourceType.ORTHOPOSITRONIUM: "oPs"}
  if not source_type in source_strings:
    return False
  if not decay_type in {DecayType.STANDARD, DecayType.WITHDEEXCITATION}:
    return False

  edep_annihilation, edep_prompt, expected_entries = get_edep_plot_data(tree, source_type, decay_type)

  total_edep_len = len(edep_annihilation) + len(edep_prompt)
  if expected_entries != total_edep_len:
    return False

  if decay_type == DecayType.STANDARD:
    edep_plots[source_strings[source_type]] = edep_annihilation
    return perform_ks_test(edep_annihilation, GammaType.ANNIHILATIONGAMMA, source_type, decay_type)
  plot_title = "".join([source_strings[source_type],"Prompt - annihilation gamma"])
  edep_plots[plot_title] = edep_annihilation
  plot_title = "".join([source_strings[source_type],"Prompt - prompt gamma"])
  edep_plots[plot_title] = edep_prompt
  test_1 = perform_ks_test(edep_annihilation, GammaType.ANNIHILATIONGAMMA, source_type, decay_type)
  test_2 = perform_ks_test(edep_prompt, GammaType.PROMPTGAMMA, source_type, decay_type)
  return test_1 and test_2

def analyse_one_file(folder, edep_plots, filename, source_type, decay_type):
  """
  Analyzes single simulation output file:
  * generates plot's data with energy depositions
  * validate simulation data

  Parameters
  ----------
  folder : str
  edep_plots : dict
   for given model new records are added by this method
  filename : str
   name of file with simulation data to check
  source_type : sourceType
  decay_type : decayType

  Returns
  -------
  correct data (tests passed) : bool
  """
  file_path = os.path.join(folder, filename)
  branches = ["edep","sourceType","decayType","gammaType"]
  tree = uproot.open(file_path)['Hits'].arrays(branches,library="numpy")
  return analyse_model(tree, edep_plots, source_type, decay_type)

def analyse_one_folder(folder):
  """
  Analyze single folder and generates benchmark's report.

  Parameters
  ----------
  folder : str

  Returns
  -------
  all simulation data in folder passed tests : bool
  """
  edep_plots  = dict()
  check_results = list()
  check_results.append(analyse_one_file(folder, edep_plots, "pPs.root", SourceType.PARAPOSITRONIUM, DecayType.STANDARD))
  check_results.append(analyse_one_file(folder, edep_plots, "pPs_prompt.root", SourceType.PARAPOSITRONIUM, DecayType.WITHDEEXCITATION))
  check_results.append(analyse_one_file(folder, edep_plots, "oPs.root", SourceType.ORTHOPOSITRONIUM, DecayType.STANDARD))
  check_results.append(analyse_one_file(folder, edep_plots, "oPs_prompt.root", SourceType.ORTHOPOSITRONIUM, DecayType.WITHDEEXCITATION))

  if not all(cr for cr in check_results):
    return False

  bins_annihilation = [round(0.001*i,2) for i in range(0,400)]
  bins_prompt = [round(0.001*i,2) for i in range(0,1000)]

  _, axs = plt.subplots(ncols=3, nrows=2, figsize=(15, 10))

  for index, key in enumerate(edep_plots.keys()):
    x_index = 0 if index < 3 else 1
    y_index = index%3
    axs[x_index,y_index].hist(edep_plots[key], bins_annihilation if not "prompt gamma" in key else bins_prompt)
    axs[x_index,y_index].set_title(key)
    axs[x_index,y_index].set(xlabel=r'$\Delta$E [MeV]', ylabel='counts')

  plt.savefig('output.pdf')
  plt.show()

  return True

# Benchmark for PositroniumSource

`PositroniumSource` is the current implementation of positronium gamma emission in Gate, superseding the legacy `ExtendedVSource` (benchmarked in `t17_extended_source`).
Key improvements over the legacy source:

* Configurable positronium fractions, lifetimes, and decay kinds per component via dedicated macro commands.
* Support for oPs pick-off/quenching (a `k2Gamma` channel from an oPs component), which the legacy source did not model.
* Optional positron range smearing.
* Explicit `setPositronInteractions` command for precise ROOT-level tagging of each decay channel as `kParaPs`, `kOrthoPs`, or `kDirect`. When this command is omitted, `sourceType` in the ROOT output defaults to `1` (generic source gamma); use `setPositronInteractions` when per-species classification is needed in analysis.

## Simulated decays

Runs 4 simulations for 4 different decay configurations:

* pPs → 2 gammas
* pPs\* → 2 gammas + prompt gamma
* oPs → 3 gammas
* oPs\* → 3 gammas + prompt gamma

where pPs is para-positronium, oPs is ortho-positronium, and the prompt gamma is a deexcitation gamma emitted alongside the positronium decay.

A point source at the origin is surrounded by a spherical scintillator detector. Each run simulates 1,000,000 primaries.

## Validation

The test compares reference energy deposition distributions (stored in `data/`) with those generated during simulation, validated using the two-sample Kolmogorov–Smirnov test (p-value threshold 0.05).

An additional check verifies that all recorded hits originate from the expected source gammas (`sourceType == 1`). The test fails if any KS test fails or if unexpected particles are detected.

## How to run

Run all four simulations (requires `Gate` on PATH):

```bash
bash runTest.sh
```

Analyse the output and validate against reference distributions:

```bash
python3 runAnalysis.py output
```

Or run both steps at once from the `GateBenchmarks/` root:

```bash
./runBenchmark.py -t t35_positronium_source
```

## Expected results

`runAnalysis.py` prints `Last test return is: True` and writes `output.pdf` with six energy deposition histograms (one per gamma type per model). The script exits with a non-zero status if any KS test fails or if unexpected particles are detected in the output.

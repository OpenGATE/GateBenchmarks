# Benchmark for PositroniumSource based on the ExtendedVSource benchmark

Runs 4 simulations for 4 different decays:

* pPs --> 2 gammas
* pPs* --> 2 gammas + prompt gamma
* oPs --> 3 gammas
* oPs* --> 3gammas + prompt gamma

where pPs is para-positronium, oPs is ortho-positronium, prompt gamma is deexcitation gamma.

We simulate a point source with spherical detector.

The test compares reference energy deposition distributions with ones generated during simulations and validates them by using the two-sample Kolmogorov-Smirnov test.

Null hypothesis is that two two distributions are identical with p-value threshold equals 0.05 (5%).

Additionally, if data contains signals from other particles test fails because we do not expect them to be present for given macros.

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

# Benchmark for ExtendedVSource

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

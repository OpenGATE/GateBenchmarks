# Tessellated geometry benchmark

A meshed sphere from a binary stl file format filled with vacuum was placed inside a liquid water box. A cylinder shape source that emit photon particles with I125 spectrum was placed next to the meshed sphere. If the particle navigaion runs properly within the tessellated object, no energy should be deposited wihin the volume.

Approximate run time 25s.

## Run & test

from /BenchTessellated

```
Gate tessellatedBench.mac
```

```
python3 analyse/tessellateChecker.py
```

return 0 for Succeed and 1 for Failed

## Authors

* Julien Bert

## Version

v1.0.0
# Merged Actor benchmark

A meshed sphere from a binary stl file format filled with vacuum was placed inside a voxelized box filled with liquid water. A cylinder shape source that emits photon particles with I125 spectrum was placed next to the meshed sphere. Both meshed and voxelized volume are merge into a main volume. The aim is to simulate analytical objects within voxelized volume (see Bert et al., PMB 2016, 61(9), p3347). If the particle navigation runs properly within the tessellated object, no energy should be deposited wihin the volume.

Approximate run time 20s.

## Run & test

```
Gate mergedBench.mac
```

## Authors

* Julien Bert

## Version

v1.0.0
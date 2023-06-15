This test is used to check the validity of the invert command for following filters for actors:

| Filter | normal filter_id | Invert filter_id  |
| --- | --- | --- |
| AngleFilter | 0 | 1 |
| EnergyFilter | 2 | 3 |
| MaterialFilter | 4 | 5 |
| VolumeFilter | 6 | 7 |
| IDFilter | 8 | 9 |
| ParticleFilter | 10 | 11 |



The test is done by using a simple geometry with a single point source, a volume called phantom, which the killer actor attach to, and a piece of material act as detector. 

Angle and energy filter's test is trivial. Material and volume filter is tested with a daughter volume of phantom. Since the IDFilter is broken right now, nothing will be done for it right now. Particle filter is tested by adding a electron source, and carefully remove all secondary hits.
# Paper.IO++ Competition

Designed by ACM AI at UCSD

Competition to be hosted in Winter Quarter 2023

## Instructions

1. Ensure that you have installed `arcade`:

```bash
pip install arcade
```

2. Run our code

We offer 3 simulator environments:

1. `GridV1` - Grid motion-based simulator (w/o Gym API integration)

2. `GridV2` - Grid motion-based simulator (w/ Gym API integration)
   
2. `Angular` - Angular motion-based simulator

```bash
cd src

# to run the angular env:
python main.py --env angular

# or, to run the grid env:
python main.py --env gridv1

# or, to run the grid + gym env:
python main.py --env gridv2
```

The Angular environment is shown below:

![angular simulator](figures/angular_sim.gif)
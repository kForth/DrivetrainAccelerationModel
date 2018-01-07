## Subsystem Acceleration Simulator

This is a python derivation of Ether's model found [here](https://www.chiefdelphi.com/media/papers/2868) (2013-09-24_2231), however significant changes have been made.

Subsystem simulation with loss of traction (wheel slip), motor voltage drop due circuit resistance, accel based on DC motor formulae, and torque-dependent, speed-dependent, and constant friction losses.

2nd-order numerical integration using Heun's Method.

You can output the data as a CSV for easy use in excel or you can view it as a plot thru matplotlib.

Right now you can test any Linear motion, like drivetrains, elevators, or conveyors.

Here's the default config. I recommend creating the model by calling LinearModel.from_json with a dict of any updated values.
```python
{
    "motor_type":             "CIM",      # Type of motor
    "num_motors":             4,          # Number of motors

    "k_rolling_resistance_s": 10,         # Rolling resistance tuning parameter, lbf
    "k_rolling_resistance_v": 0,          # Rolling resistance tuning parameter, lbf/(ft/sec)
    "k_gearbox_efficiency":   0.7,        # Gearbox efficiency fraction

    "gear_ratio":             12.75,      # Gear Ratio, driven:driving
    "effective_diameter":     6,          # Wheel radius, inches
    "incline_angle":          0,          # Incline angle relative to the ground, degrees
    "effective_mass":         150,        # effective mass, lbm

    "check_for_slip":         True,       # Check for wheel slip in friction drives
    "coeff_kinetic_friction": 0.8,        # Coefficient of kinetic friction
    "coeff_static_friction":  1.0,        # Coefficient of static friction

    "motor_current_limit":    100,        # Current limit per motor

    "battery_voltage":        12.7,       # Fully-charged open-circuit battery volts

    "resistance_com":         0.013,      # Battery and circuit resistance from bat to PDB (incl main breaker), ohms
    "resistance_one":         0.002,      # Circuit resistance from PDB to motor (incl 40A breaker), ohms

    "time_step":              0.001,      # Integration step size, seconds
    "simulation_time":        100,        # Integration duration, seconds
    "max_dist":               30,         # Max distance to integrate to, feet

    "elements_to_plot":       [0, 1, 2]   # Elements to plot (pos, vel, accel, current/10)
}
```

### Sample Plot
![Sample Plot](https://raw.githubusercontent.com/kForth/DrivetrainAccelerationModel/master/samples/sample.png "Sample plot comparing 3 different gear ratios.")

### Sample CSV
|time(*s*)|dist(*ft*)|speed(*ft/s*)|accel(*ft/s^2*)|current(*amps/10*)|voltage|slip|
|:--- | :--- | :--- | :--- | :--- | :--- |:--- |
|0|0.00000|0.00000|23.59423|24.77243|9.35572|True|
|0.00100|0.00001|0.02359|23.59423|24.77243|9.35572|True|
|0.00200|0.00005|0.04719|23.59423|24.77243|9.35572|True|
|0.00300|0.00011|0.07078|23.59423|24.77243|9.35572|True|
|0.00400|0.00019|0.09438|23.59423|24.77243|9.35572|True|
|0.00500|0.00029|0.11797|23.59423|24.77243|9.35572|True|
|0.00600|0.00042|0.14157|23.59423|24.77243|9.35572|True|
|0.00700|0.00058|0.16516|23.59423|24.77243|9.35572|True|
|0.00800|0.00076|0.18875|23.59423|24.77243|9.35572|True|
|0.00900|0.00096|0.21235|23.59423|24.77243|9.35572|True|
|0.01000|0.00118|0.23594|23.59423|24.77243|9.35572|True|
|0.01100|0.00143|0.25954|23.59423|24.77243|9.35572|True|


## Optimization

You can also test a range of ratios to optimize your ratio.

### Sample Optimization Plot
![Sample Optimize Plot](https://raw.githubusercontent.com/kForth/DrivetrainAccelerationModel/master/samples/optimize.png "Sample optimization plot for a 150kg 6x MiniCIM robot. (optimize-time_to_dist.csv)")

### Sample Optimization XLSX
![Sample Optimize CSV](https://raw.githubusercontent.com/kForth/DrivetrainAccelerationModel/master/samples/optimize_xlsx.png "Sample optimization xlsx for a 150kg 6x MiniCIM robot. (optimize-time_to_dist.csv)")
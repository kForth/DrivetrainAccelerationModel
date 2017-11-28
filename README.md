## Drivetrain Acceleration Model

This is a python implementation of Ether's model found [here](https://www.chiefdelphi.com/media/papers/2868)(2013-09-24_2231).

Drivetrain acceleration model with loss of traction (wheel slip), motor voltage drop due circuit resistance, accel based on reduced-voltage motor curves, and torque-dependent, speed-dependent, and constant friction losses.

Full python source code.

2nd-order numerical integration using Heun's Method.

You can output the data as a CSV for easy use in excel or you can view it as a plot thru matplotlib.

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

I've also been playing with ratio optimization, you can see my work in optimize.py.

### Sample Optimization Plot
![Sample Optimize Plot](https://raw.githubusercontent.com/kForth/DrivetrainAccelerationModel/master/samples/optimize.png "Sample optimization plot for a 150kg 6x MiniCIM robot. (optimize-time_to_dist.csv)")

### Sample Optimization XLSX
![Sample Optimize CSV](https://raw.githubusercontent.com/kForth/DrivetrainAccelerationModel/master/samples/optimize_xlsx.png "Sample optimization xlsx for a 150kg 6x MiniCIM robot. (optimize-time_to_dist.csv)")
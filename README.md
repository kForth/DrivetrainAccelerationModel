## Drivetrain Acceleration Model

This is a python implementation of Ether's model found [here](https://www.chiefdelphi.com/media/papers/2868)(2013-09-24_2231).

Drivetrain acceleration model with loss of traction (wheel slip), motor voltage drop due circuit resistance, accel based on reduced-voltage motor curves, and torque-dependent, speed-dependent, and constant friction losses.

Full python source code.

2nd-order numerical integration using Heun's Method.

CSV output file can be directly imported into Excel for graphing acceleration, speed, distance, motor amps, and motor voltage vs time.
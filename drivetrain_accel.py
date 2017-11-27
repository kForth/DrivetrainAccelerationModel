# The following constants define the drivetrain being modeled:

Kro = 10  # rolling resistance tuning parameter, lbf
Krv = 0  # rolling resistance tuning parameter, lbf/(ft/sec)
Kf = 0.9  # drivetrain efficiency fraction

Vspec = 12  # motor spec volts
Tspec = 343.4  # motor stall torque, in_oz
Wspec = 5310  # motor free speed, RPM
Ispec = 133  # motor stall amps
n = 4  # number of motors

G = 12.75  # gear ratio
r = 3  # wheel radius, inches

M = 150  # vehicle mass, lbm
uk = 0.7  # coefficient of kinetic friction
us = 1.0  # coefficient of static friction

Rcom = 0.013  # ohms, battery internal resistance plus
# wire and connection resistance
# from battery to PDB (including main breaker)

Vbat = 12.7  # fully-charged open-circuit battery volts

Rone = 0.002  # ohms, circuit wiring and connector resistance
# from PDB to motor (including 40A breaker)

dt = 0.001  # integration step size, seconds
tstop = 1.0  # integration duration, seconds

# -------------- end of user-defined constants -----------------

# derived constants:
Toffset, Tslope = 0, 0  # offset and slope of adjusted Torque vs Speed motor curve
Kt = 0  # motor torque constant, Nm/amp
Vfree = 0  # vehicle speed at motor free speed, meters/sec
W = 0  # vehicle weight, Newtons
F2A = 0  # force to amps

# working variables:

slipping = False  # state variable, init to false
Vm = 0  # Voltage at the motor
V = 0  # vehicle speed, meters/sec
x = 0  # vehicle distance traveled, meters
t = 0  # elapsed time, seconds
a = 0  # vehicle acceleration, meters/sec/sec
A = 0  # current per motor, amps


def English2SI():
    global Kro, Krv, Tspec, Wspec, r, M
    Kro *= 4.448222  # convert lbf to Newtons
    Krv *= 4.448222 * 3.28083  # convert lbf/(ft/s) to Newtons/(meter/sec)
    Tspec *= 0.00706155  # convert oz_in to Newton_meters
    Wspec = Wspec / 60 * 2 * 3.1415926536  # convert RPM to rad/sec
    r = r * 2.54 / 100  # convert inches to meters
    M *= 0.4535924  # convert lbm to kg


def accel(V):  # compute acceleration w/ slip
    global Vm, A
    Wm = V / r * G  # Wm = motor speed associated with vehicle speed
    Tm = Toffset - Tslope * Wm  # available torque at motor @ V, in Newtons
    Tw = Kf * Tm * G  # available torque at one wheel @ V
    Ft = Tw / r * n  # available force at wheels @ V, in Newtons
    F = 0  # slip-adjusted vehicle force due to wheel torque, in Newtons
    if Ft > W * us:
        slipping = True
        F = W * uk
    elif Ft < W * uk:
        slipping = False
        F = Ft
    A = F * F2A  # computed here for output
    Vm = Vbat - n * A * Rcom - A * Rone  # computed here for output
    L = Kro + Krv * V  # rolling resistance force, in Newtons
    Fa = F - L  # net force available for acceleration, in Newtons
    if Fa < 0:
        Fa = 0
    return Fa / M


def print_line():
    print("{0},{1},{2},{3},{4},{5},{6}".format(t, x * 3.28083, V * 3.28083, slipping, a * 3.28083, n * A / 10, Vm))


def Heun():  # numerical integration using Heun's Method
    global t, a, x, V
    t = dt
    while t <= tstop:
        Vtmp = V + a * dt  # kickstart with Euler step
        atmp = accel(Vtmp)
        Vtmp = V + (a + atmp) / 2 * dt  # recalc Vtmp trapezoidally
        a = accel(Vtmp)  # update a
        x += (V + Vtmp) / 2 * dt  # update x trapezoidally
        V = Vtmp  # update V
        print_line()
        t += dt


# for reference only not used:
def Euler():  # numerical integration using Euler's Method
    global t, V, x, a
    t = dt
    while t <= tstop:
        V += a * dt
        x += V * dt
        a = accel(V)
        print_line()
        t += dt


if __name__ == "__main__":
    print("t,feet,ft/s,slip,ft/s/s,amps/10,Vm,{0} Kro={1} Krv={2} Kf={3} Vspec={4} Tspec={5} Wspec={6} Ispec={7} Rcom={8} Vbat={9} Rone={10} n={11} G={12} r={13} M={14} uk={15} us={16}".format(time(), Kro, Krv, Kf, Vspec, Tspec, Wspec, Ispec, Rcom, Vbat, Rone, n, G, r, M, uk, us))

    English2SI()

    # calculate Derived Constants once:
    Toffset = (Tspec * Vbat * Wspec) / (Vspec * Wspec + Ispec * Rone * Wspec + Ispec * n * Rcom * Wspec)
    Tslope = (Tspec * Vspec) / (Vspec * Wspec + Ispec * Rone * Wspec + Ispec * n * Rcom * Wspec)
    Kt = Tspec / Ispec
    W = M * 9.80665
    F2A = r / (n * Kf * G * Kt)  # vehicle total force to per-motor amps conversion

    a = accel(V)  # compute accel at t=0
    print_line()  # output values at t=0

    Heun()  # numerically integrate and output using Heun's method
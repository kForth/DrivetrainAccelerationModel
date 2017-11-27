from time import time


# The following constants define the drivetrain being modeled:

k_rolling_resistance_s = 10  # rolling resistance tuning parameter, lbf
k_rolling_resistance_v = 0  # rolling resistance tuning parameter, lbf/(ft/sec)
k_drivetrain_efficiency = 0.9  # drivetrain efficiency fraction

motor_max_voltage = 12  # motor spec volts
motor_stall_torque = 343.4  # motor stall torque, in_oz
motor_free_speed = 5310  # motor free speed, RPM
motor_stall_current = 133  # motor stall amps
num_motors = 4  # number of motors

gear_ratio = 12.75  # gear ratio
wheel_radius = 3  # wheel radius, inches

vehicle_mass = 150  # vehicle mass, lbm
coeff_kinetic_friction = 0.7  # coefficient of kinetic friction
coeff_static_friction = 1.0  # coefficient of static friction

resistance_com = 0.013  # ohms, resistance of battery, wire, and connectors (including main breaker)

battery_voltage = 12.7  # fully-charged open-circuit battery volts

resistance_one = 0.002  # ohms, resistance of wiring and connector from PDB to motor (including 40A breaker)

time_step = 0.001  # integration step size, seconds
simulation_time = 1.0  # integration duration, seconds

# -------------- end of user-defined constants -----------------

# derived constants:
torque_offset, torque_slope = 0, 0  # offset and slope of adjusted Torque vs Speed motor curve
k_t = 0  # motor torque constant, Nm/amp
max_vehicle_speed = 0  # vehicle speed at motor free speed, meters/sec
vehicle_weight = 0  # vehicle weight, Newtons
force_to_amps = 0  # force to amps

# working variables:

is_slipping = False  # state variable, init to false
sim_voltage = 0  # Voltage at the motor
sim_speed = 0  # vehicle speed, meters/sec
sim_distance = 0  # vehicle distance traveled, meters
sim_time = 0  # elapsed time, seconds
sim_acceleration = 0  # vehicle acceleration, meters/sec/sec
sim_current_per_motor = 0  # current per motor, amps


def convert_units_to_si():
    global k_rolling_resistance_s, k_rolling_resistance_v, motor_stall_torque, motor_free_speed, wheel_radius, vehicle_mass
    k_rolling_resistance_s *= 4.448222  # convert lbf to Newtons
    k_rolling_resistance_v *= 4.448222 * 3.28083  # convert lbf/(ft/s) to Newtons/(meter/sec)
    motor_stall_torque *= 0.00706155  # convert oz_in to Newton_meters
    motor_free_speed = motor_free_speed / 60 * 2 * 3.1415926536  # convert RPM to rad/sec
    wheel_radius = wheel_radius * 2.54 / 100  # convert inches to meters
    vehicle_mass *= 0.4535924  # convert lbm to kg


def calc_max_accel(V):  # compute acceleration w/ slip
    global sim_voltage, sim_current_per_motor, is_slipping
    Wm = V / wheel_radius * gear_ratio  # Wm = motor speed associated with vehicle speed
    max_torque_at_voltage = torque_offset - torque_slope * Wm  # available torque at motor @ V, in Newtons
    max_torque_at_wheel = k_drivetrain_efficiency * max_torque_at_voltage * gear_ratio  # available torque at wheels
    available_force_at_wheel = max_torque_at_wheel / wheel_radius * num_motors  # available force at wheels
    applied_force_at_wheel = 0  # slip-adjusted vehicle force due to wheel torque
    if available_force_at_wheel > vehicle_weight * coeff_static_friction:
        is_slipping = True
        applied_force_at_wheel = vehicle_weight * coeff_kinetic_friction
    elif available_force_at_wheel < vehicle_weight * coeff_kinetic_friction:
        is_slipping = False
        applied_force_at_wheel = available_force_at_wheel
    sim_current_per_motor = applied_force_at_wheel * force_to_amps  # computed here for output
    sim_voltage = battery_voltage - num_motors * sim_current_per_motor * resistance_com - sim_current_per_motor * resistance_one  # computed here for output
    rolling_resistance = k_rolling_resistance_s + k_rolling_resistance_v * V  # rolling resistance force, in Newtons
    net_accel_force = applied_force_at_wheel - rolling_resistance  # net force available for acceleration, in Newtons
    if net_accel_force < 0:
        net_accel_force = 0
    return net_accel_force / vehicle_mass


def integrate_with_heun():  # numerical integration using Heun's Method
    global sim_time, sim_acceleration, sim_distance, sim_speed
    sim_time = time_step
    while sim_time <= simulation_time + time_step:
        Vtmp = sim_speed + sim_acceleration * time_step  # kickstart with Euler step
        atmp = calc_max_accel(Vtmp)
        Vtmp = sim_speed + (sim_acceleration + atmp) / 2 * time_step  # recalc Vtmp trapezoidally
        sim_acceleration = calc_max_accel(Vtmp)  # update a
        sim_distance += (sim_speed + Vtmp) / 2 * time_step  # update x trapezoidally
        sim_speed = Vtmp  # update V
        print_line()
        sim_time += time_step


# for reference only not used:
def integrate_with_euler():  # numerical integration using Euler's Method
    global sim_time, sim_speed, sim_distance, sim_acceleration
    sim_time = time_step
    while sim_time <= simulation_time + time_step:
        sim_speed += sim_acceleration * time_step
        sim_distance += sim_speed * time_step
        sim_acceleration = calc_max_accel(sim_speed)
        print_line()
        sim_time += time_step


def print_line():
    print("{0},{1},{2},{3},{4},{5},{6}".format(sim_time, sim_distance * 3.28083, sim_speed * 3.28083, is_slipping, sim_acceleration * 3.28083, num_motors * sim_current_per_motor / 10, sim_voltage))


if __name__ == "__main__":
    print("t,feet,ft/s,slip,ft/s/s,amps/10,Vm,{0} Kro={1} Krv={2} Kf={3} motor_max_voltage={4} motor_stall_torque={5} motor_free_speed={6} motor_stall_current={7} Rcom={8} Vbat={9} Rone={10} n={11} G={12} r={13} M={14} uk={15} us={16}".format(time(), k_rolling_resistance_s, k_rolling_resistance_v, k_drivetrain_efficiency, motor_max_voltage, motor_stall_torque, motor_free_speed, motor_stall_current, resistance_com, battery_voltage, resistance_one, num_motors, gear_ratio, wheel_radius, vehicle_mass, coeff_kinetic_friction, coeff_static_friction))

    convert_units_to_si()

    # calculate Derived Constants once:
    torque_offset = (motor_stall_torque * battery_voltage * motor_free_speed) / (motor_max_voltage * motor_free_speed + motor_stall_current * resistance_one * motor_free_speed + motor_stall_current * num_motors * resistance_com * motor_free_speed)
    torque_slope = (motor_stall_torque * motor_max_voltage) / (motor_max_voltage * motor_free_speed + motor_stall_current * resistance_one * motor_free_speed + motor_stall_current * num_motors * resistance_com * motor_free_speed)
    k_t = motor_stall_torque / motor_stall_current
    vehicle_weight = vehicle_mass * 9.80665
    force_to_amps = wheel_radius / (num_motors * k_drivetrain_efficiency * gear_ratio * k_t)  # vehicle total force to per-motor amps conversion

    sim_acceleration = calc_max_accel(sim_speed)  # compute accel at t=0
    print_line()  # output values at t=0

    integrate_with_heun()  # numerically integrate and output using Heun's method

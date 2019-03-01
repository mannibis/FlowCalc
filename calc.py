import math
from decimal import Decimal


def pois_metric(pipe_diameter, delta_p, pipe_length):
    """If the flow in the pipe is laminar, you can use the Poiseuille Equation to calculate the flow rate
        mu = 0.001 @ 25 degrees C
        Q = (pi * (D**4) * delta_p) / (128 * mu * pipe_length)
    """
    mu = 0.001  # water @ 25 degrees C
    pois = mu * 10
    flow_rate_lam = (math.pi * (pipe_diameter ** 4) * delta_p) / (128 * pois * pipe_length)

    return flow_rate_lam


def bern_metric(pipe_diameter, delta_p, pipe_length):
    """For turbulent flow, we can use Bernoulli's Equation with a friction term. Assuming the pipe is horizontal,
        (delta_p / rho) + (velocity^2 / 2) = -F
        where F accounts for friction heating and is given in terms of an empirical friction factor, fr.
        Substituting the equation for friction heating into Bernoulli's Equation and solving for velocity:
        V = sqrt((2 * delta_p) / (rho * (4 * fr * (pipe_length / pipe_diameter) - 1)))
        Q = V *  A
    """
    fr_c = 0.003  # assuming Reynolds number is 10**5 and pipe material is smooth copper
    fr_reyn = 0.046 / (reynolds_num(pipe_diameter, delta_p, pipe_length) ** 0.2)  # Taitel and Dukler approximation
    rho = 1000  # density of water @ 4 deg celsius (kg/m**3)

    v = math.sqrt((2 * delta_p) / (rho * (4 * fr_reyn * (pipe_length / pipe_diameter) - 1)))
    flow_rate_turb = v * ((math.pi / 4) * (pipe_diameter ** 2))

    return flow_rate_turb, v


def reynolds_num(pipe_diameter, delta_p, pipe_length):
    rho = 1000  # density of water @ 4 deg celsius (kg/m**3)
    mu = 0.001  # water @ 25 degrees C

    v = pois_metric(pipe_diameter, delta_p, pipe_length) / ((math.pi / 4) * pipe_diameter ** 2)
    reynolds = (rho * pipe_diameter * v) / mu

    return reynolds


def main():
    print "Enter Water Pressure (psig):  "
    delta_p = input()
    print "Enter Pipe Diameter (inches):  "
    pipe_diameter = input()
    print "Enter Length of Pipe (feet):  "
    pipe_length = input()

    pipe_diameter_metric = 0.0254 * float(pipe_diameter)
    pipe_length_metric = 0.3048 * float(pipe_length)
    delta_p_metric = 6894.76 * float(delta_p)

    try:
        flow_rate_lam_metric = pois_metric(pipe_diameter_metric, delta_p_metric, pipe_length_metric)
        flow_rate_lam_imp = flow_rate_lam_metric * 15850.3
        print "Q (laminar)\t\t=\t%.2f gpm" % Decimal(flow_rate_lam_imp)
    except ValueError:
        print "There was a math value error. Check your numbers and try again."
    except TypeError:
        print "There was a type error. Make sure you are entering numbers without units and try again."

    try:
        flow_rate_turb_metric = bern_metric(pipe_diameter_metric, delta_p_metric, pipe_length_metric)[0]
        velocity_metric = bern_metric(pipe_diameter_metric, delta_p_metric, pipe_length_metric)[1]
        flow_rate_turb_imp = flow_rate_turb_metric * 15850.3
        velocity_imp = velocity_metric * 3.28084
        print "Q (turbulent)\t=\t%.2f gpm" % Decimal(flow_rate_turb_imp)
        print "V (turbulent)\t=\t%.2f ft/s" % Decimal(velocity_imp)
    except ValueError:
        print "There was a math value error. Check your numbers and try again."
    except TypeError:
        print "There was a type error. Make sure you are entering numbers without units and try again."

    try:
        print "Reynolds Number\t=\t%.2E" % Decimal(
            reynolds_num(pipe_diameter_metric, delta_p_metric, pipe_length_metric))
    except ValueError:
        print "There was a math value error. Check your numbers and try again."
    except TypeError:
        print "There was a type error. Make sure you are entering numbers without units and try again."

import argparse
import numpy as np
from sympy import Symbol
from sympy.tensor.array import derive_by_array
from sympy.utilities.lambdify import lambdify
import pdb
# Proposed Algorithm - Determining the amount of Compliance for the
# Creation of Cardiovascular Grafts
# Stephannie Jimenez - Esteban Galvis

# Arguments for the client
parser = argparse.ArgumentParser(description='Compliance calculation')

parser.add_argument('--mode', default='healthy',
                    help='Case for changing the parameters value.')

parser.add_argument('--vol', default=5, help='Total volume of blood')

args = parser.parse_args()

if args.mode == 'healthy':
    Rs = 17.5
    Rp = 1.79
    Kr = 2.8
    Kl = 1.12
    V = args.vol
elif args.mode == 'heart-failure':
    Rs = 6.82
    Rp = 1.36
    Kr = 4.72
    Kl = 9.5
    V = args.vol
elif args.mode == 'hypertension':
    Rs = 40.5
    Rp = 3.21
    Kr = 3
    Kl = 1.7
    V = args.vol


def main():
    """Run main."""
    print('Starting program...')

    # Definition of variables
    Csa = Symbol('Csa')
    Csv = Symbol('Csv')
    Cpa = Symbol('Cpa')
    Cpv = Symbol('Cpv')

    # Definition of equations
    Tsa = Csa/Kr + Csa*Rs
    Tsv = Csv/Kr
    Tpa = Cpa/Kl + Cpa*Rp
    Tpv = Cpv/Kl

    Tsum = Tsa+Tsv+Tpa+Tpv

    # Volumes
    Vsa = Tsa*V/Tsum
    Vsv = Tsv*V/Tsum
    Vpa = Tpa*V/Tsum
    Vpv = Tpv*V/Tsum
    Vsum = Vsa + Vsv + Vpa + Vpv
    Vtot = lambdify((Csa, Csv, Cpa, Cpv), Vsum)

    # Pressures
    Psa = Tsa*V/(Csa*Tsum)
    Psv = Tsv*V/(Csv*Tsum)
    Ppa = Tpa*V/(Cpa*Tsum)
    Ppv = Tpv*V/(Cpv*Tsum)

    # Objective Function
    f_obj = V/(Tsum)
    f = lambdify((Csa, Csv, Cpa, Cpv), f_obj)

    # Partial derivatives of objective function
    partial = derive_by_array(f_obj, (Csa, Csv, Cpa, Cpv))
    grad = lambdify((Csa, Csv, Cpa, Cpv), partial)

    # Tolerance - num iterations
    # tol = 0.001
    n = 10000

    # Start seed for the random function
    # np.random.seed(1)

    # Generate random values for init Cpa, Cpv, Csa, Csv
    x = np.random.rand(4)

    min_val = 5000000
    min_x = x

    while(n > 0):
        # Check all x are positive
        for val in x:
            if val < 0:
                val = abs(val)
        
        # Check the volume restriction
        act_v = Vtot(x[0], x[1], x[2], x[3])

        if act_v != V:
            y = V*np.ones(4)
            diff = np.abs(np.subtract(x, y))
            val, idx = min((val, idx) for (idx, val) in enumerate(diff))
            x[idx] = val

        # Calculate gradient given the points
        g = grad(x[0], x[1], x[2], x[3])

        # Calculate the value of the objective function
        act = f(x[0], x[1], x[2], x[3])

        if(act < min_val):
            min_val = act
            min_x = x

        # Modify the actual value depending the gradient
        val, idx = max((val, idx) for (idx, val) in enumerate(g))
        x[idx] = abs(x[idx] + val)
        n = n - 1

    print(' Csa: {} \n Csv: {} \n Cpa: {} \n Cpv: {} \n'.format(
          min_x[0], min_x[1], min_x[2], min_x[3]))


if __name__ == '__main__':
    main()

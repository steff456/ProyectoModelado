import argparse
import numpy as np
import cvxpy as cp
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

    # Start seed for the random function
    np.random.seed(1)

    Csa = cp.Variable(1)
    Csv = cp.Variable(1)
    Cpa = cp.Variable(1)
    Cpv = cp.Variable(1)

    Tsa = Csa/Kr + Csa*Rs
    Tsv = Csv/Kr
    Tpa = Cpa/Kl + Cpa*Rp
    Tpv = Cpv/Kl

    Tsum = Tsa+Tsv+Tpa+Tpv

    f_obj = cp.Minimize(V/(Tsum))

    # Volumes
    Vsa = Tsa*V/Tsum
    Vsv = Tsv*V/Tsum
    Vpa = Tpa*V/Tsum
    Vpv = Tpv*V/Tsum

    # Pressures

    const = []


if __name__ == '__main__':
    main()

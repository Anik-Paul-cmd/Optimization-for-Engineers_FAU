# Optimization for Engineers - Dr.Johannes Hild
# Levenberg-Marquardt descent

# Purpose: Find pmin to satisfy norm(jacobian_R.T @ R(pmin))<=eps

# Input Definition:
# R: error vector class with methods .residual() and .jacobian()
# p0: column vector in R**n (parameter point), starting point.
# eps: positive value, tolerance for termination. Default value: 1.0e-4.
# alpha0: positive value, starting value for damping. Default value: 1.0e-3.
# beta: positive value bigger than 1, scaling factor for alpha. Default value: 100.
# verbose: bool, if set to true, verbose information is displayed.

# Output Definition:
# pmin: column vector in R**n (parameter point)

# Required files:
# d = PrecCGSolver(A,b) from PrecCGSolver.py

# Test cases:
# p0 = np.array([[180],[0]])
# myObjective =  simpleValleyObjective(p0)
# xk = np.array([[0, 0], [1, 2]])
# fk = np.array([[2, 3]])
# myErrorVector = leastSquaresModel(myObjective, xk, fk)
# eps = 1.0e-4
# alpha0 = 1.0e-3
# beta = 100
# pmin = levenbergMarquardtDescent(myErrorVector, p0, eps, alpha0, beta, 1)
# should return pmin close to [[1], [1]]

import numpy as np
import PrecCGSolver as PCG


def matrnr():
    # set your matriculation number here
    matrnr = 23006558
    return matrnr


def levenbergMarquardtDescent(R, p0: np.array, eps=1.0e-4, alpha0=1.0e-3, beta=100, verbose=0):
    if eps <= 0:
        raise TypeError('range of eps is wrong!')

    if alpha0 <= 0:
        raise TypeError('range of alpha0 is wrong!')

    if beta <= 1:
        raise TypeError('range of beta is wrong!')

    if verbose:
        print('Start levenbergMarquardtDescent...')

    countIter = 0
    p = p0

    # INCOMPLETE CODE STARTS
    
    alphak = alpha0
    
    jacobian, residual = R.jacobian(p), R.residual(p)
    
    while np.linalg.norm(jacobian.T @ residual) > eps:
        dk = PCG.PrecCGSolver(jacobian.T @ jacobian + (alphak*np.eye(len(p))), -jacobian.T @ residual)
        resnew = R.residual(p + dk)
        if (0.5 * resnew.T @ resnew) < (0.5 * residual.T @ residual):
            p = p + dk
            alphak = alpha0
        else:
            alphak = beta * alphak
        
        jacobian, residual = R.jacobian(p), R.residual(p)
        
        countIter += 1
        
    p_star = p
    p = np.copy(p_star)    


    # INCOMPLETE CODE ENDS
    if verbose:
        gradp = R.jacobian(p).T @ R.residual(p)
        print('levenbergMarquardtDescent terminated after ', countIter, ' steps with norm of gradient =', np.linalg.norm(gradp))

    return p


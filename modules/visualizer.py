#!/usr/bin/env python3
"""
Visualizer is supposed to visiualize the data from the outputfiles
of the SGLsolver

"""

import os.path
import numpy as np
import matplotlib.pyplot as plt


def _visualizer(directory, scaling):
    """Visualizes the results from the SGLsolver. It reads the textdocuments of
    potential, energies, wavefunctions and expected values and makes plots.

    Args:
        directory: directory of input files and output file
        scaling: scaling factor for better visualization of the wave functions

    Returns:

    """

    # POTENTIAL
    filename = os.path.join(directory, "potential.dat")
    inputpot = open(filename, "r")
    potdata = inputpot.readlines()
    inputpot.close()

    # creates arrays of potential and xvalues for plotting
    nn = np.shape(potdata)[0]
    pot = np.zeros((nn, ), dtype=float)
    xx = np.zeros((nn, ), dtype=float)
    for ii in range(0, nn):
        pot[ii, ] = np.array(potdata[ii].split(" ")[1], dtype=float)
        xx[ii, ] = np.array(potdata[ii].split(" ")[0], dtype=float)

    # ENERGY
    filename = os.path.join(directory, "energies.dat")
    inputener = open(filename, "r")
    enerdata = inputener.readlines()
    inputener.close()

    # creates array of energy values for plotting
    mm = np.shape(enerdata)[0]
    ener = np.zeros((mm, ), dtype=float)
    for ii in range(0, mm):
        ener[ii, ] = np.array(enerdata[ii], dtype=float)

    # WAVEFUNCS
    filename = os.path.join(directory, "wavefuncs.dat")
    inputwave = open(filename, "r")
    wavedata = inputwave.readlines()
    inputwave.close()

    # creates array of wavefunctions for plotting
    waves = np.zeros((nn, mm), dtype=float)
    for ii in range(0, nn):
        for jj in range(0, mm):
            waves[ii, jj] = np.array(wavedata[ii].split(" ")[jj+1],
                                     dtype=float)

    # EXPVALUES
    filename = os.path.join(directory, "expvalues.dat")
    inputexp = open(filename, "r")
    expdata = inputexp.readlines()
    inputexp.close()

    # creates arrays of uncertainty and expected xvalues for plotting
    expxval = np.zeros((mm, ), dtype=float)
    uncer = np.zeros((mm, ), dtype=float)
    for ii in range(0, mm):
        expxval[ii, ] = np.array(expdata[ii].split(" ")[0], dtype=float)
        uncer[ii, ] = np.array(expdata[ii].split(" ")[1], dtype=float)

    # PLOTTING

    # FIRST plot: potential, energies, wavefunctions and expected xvalues
    plt.subplot(1, 2, 1)  # for two plots in one figure
    plt.title(r'Potential, eigenstates, $\langle$x$\rangle$', fontsize=14)

    plt.xlabel("x [Bohr]", fontsize=14)
    plt.ylabel("Energy [Hartree]", fontsize=14)

    # add potential
    plt.plot(xx, pot, linewidth=1.5, color='k',
             label='Potential')
    # add energies as horizontal lines(hlines)
    # reaching from one diagram edge to the other
    plt.hlines(ener, xx[0]-(xx[nn-1]-xx[0])/10, xx[nn-1]+(xx[nn-1]-xx[0])/10,
               colors='0.8', linestyles='solid', label='Energies')

    # add wavefunctions on height of the corresponding eigenvalue
    for ii in range(0, mm):
        energy = ener[ii]
        wave = waves[:, ii]
        if ii % 2:  # alternating colors for better graphical appearance
            color = "red"
        else:
            color = "blue"
        plt.plot(xx, scaling * wave + energy, linewidth=1.0, linestyle="-",
                 color=color)  # scaling is determined by user (default=0.3)

    # add expected x-value
    plt.scatter(expxval, ener, c='green', marker='x', s=100, linewidths=1)

    # modify axes appearance
    ax = plt.gca()
    ax.set_xlim(xx[0]-(xx[nn-1]-xx[0])/10, xx[nn-1]+(xx[nn-1]-xx[0])/10)
    ax.set_ylim(min(pot)-(max(ener)-min(pot))/10,
                max(ener)+(max(ener)-min(pot))/6)
    # limits for x-axis are set as xmin/max minus/plus ten percent
    # of potential width
    # and for y.axis as minimum potential/ maximum energy value minus/plus
    # ten/~17 percent of their difference

    plt.tick_params(axis='y', which='both', right=False)  # remove ticks
    plt.tick_params(axis='x', which='both', top=False)

    # SECOND plot: energies and uncertainty
    plt.subplot(1, 2, 2)
    plt.title(r'$\sigma_x$', fontsize=18)
    plt.xlabel("[Bohr]", fontsize=14)

    # add energies
    plt.hlines(ener, xx[0], 1.1 * xx[nn-1], colors='0.8', linestyles='solid',
               label='Energies')
    # add uncertainty
    plt.scatter(uncer, ener, c='purple', marker='+', s=150, linewidths=2)

    # modify axes appearance
    ax = plt.gca()
    ax.set_xlim(0, 1.1 * max(np.absolute(xx)))
    ax.set_ylim(min(pot)-(max(ener)-min(pot))/10,
                max(ener)+(max(ener)-min(pot))/6)
    # set x limits from zero to maximum of x-vector plus ten percent of it
    # and y limits same as first plot

    plt.tick_params(axis='y', which='both', left=False, right=False,
                    labelleft=False)
    plt.tick_params(axis='x', which='both', top=False)

    # Save the curves in a pdf-document
    filename = os.path.join(directory, 'curves.pdf')
    plt.savefig(filename, format='pdf')

    return()


def visualize(directory, scaling):
    """Visualizes the results from the SGLsolver. It reads the textdocuments of
    potential, energies, wavefunctions and expected values and makes plots.

    Args:
        directory: directory where inputfile is saved
                   and outputfiles will be saved
        scaling: scaling factor for visualization of the wavefunctions

    Returns:
        Nothing. The graphic is saved in the directory as *curves.pdf*.

    """

    # executes private visualizer function to create the plots
    _visualizer(directory, scaling)

    return()

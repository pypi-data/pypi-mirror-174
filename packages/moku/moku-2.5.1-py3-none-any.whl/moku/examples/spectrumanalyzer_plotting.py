#
# moku example: Plotting Spectrum Analyzer
#
# This example demonstrates how you can configure the Spectrum
# Analyzer instrument and plot its spectrum data in real-time.
#
# (c) 2021 Liquid Instruments Pty. Ltd.
#

import matplotlib.pyplot as plt
from moku.instruments import SpectrumAnalyzer

# Connect to your Moku by its ip address using
# SpectrumAnalyzer('192.168.###.###')
# or by its serial number using
# SpectrumAnalyzer(serial=123)
i = SpectrumAnalyzer('192.168.###.###')

try:
    # Configure the Spectrum Analyzer 
    i.set_span(frequency1=0, frequency2=30e3)
    i.set_rbw('Auto')  # Auto-mode

    # Configure ADC inputs
    i.set_frontend(1, coupling='DC', range='10Vpp', impedance="1MOhm")
    i.set_frontend(2, coupling='DC', range='10Vpp', impedance="1MOhm")

    # Set up basic plot configurations
    line1, = plt.plot([])
    line2, = plt.plot([])
    plt.ion()
    plt.show()
    plt.grid(b=True)
    plt.autoscale(axis='x', tight=True)

    # Get an initial frame of data to set any frame-specific plot
    # parameters
    frame = i.get_data()

    # Format the x-axis as a frequency scale
    ax = plt.gca()

    # Get and update the plot with new data
    while True:
        frame = i.get_data()

        # Set the frame data for each channel plot
        line1.set_ydata(frame['ch1'])
        line2.set_ydata(frame['ch2'])
        # Frequency axis shouldn't change, but to be sure
        line1.set_xdata(frame['frequency'])
        line2.set_xdata(frame['frequency'])
        # Ensure the frequency axis is a tight fit
        ax.relim()
        ax.autoscale_view()

        # Redraw the lines
        plt.draw()
        plt.pause(0.001)

except Exception as e:
    print(f'Exception occurred: {e}')
finally:
    # Close the connection to the Moku device
    # This ensures network resources and released correctly
    i.relinquish_ownership()

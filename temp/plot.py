from colour.plotting import *
import pylab

chromaticity_diagram_plot_CIE1931(standalone=False)

#plotting the *xy* chromaticity coordinates.
x, y = ((0.4,0.3,0.2), (0.3, 0.4,0.7))
pylab.plot(x, y, 'o', color='white')

#displaying the plot
render(
        standalone=True,
        limits=(-0.1, 0.9, -0.1, 0.9),
        x_tighten=True,
        y_tighten=True)

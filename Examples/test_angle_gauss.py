from GMXFit.GaussIO import GaussScan
from GMXFit.FitPES import AngleFit


# Create Data object from gaussian output file
gauss = GaussScan("angle_scan.log")

# Pass data object  PES Fitter
angFit = AngleFit(gauss)

# Fit
angFit.Fit()

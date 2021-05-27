from GMXFit.GaussIO import GaussScan
from GMXFit.FitPES import DihedralFit


# Create Data object from gaussian output file
gauss = GaussScan("dihedral_scan.log")

# Pass data object  PES Fitter
dihFit = DihedralFit(gauss)

# Fit to Rychart-Bellman
dihFit.Fit(fitType="DihRB", drawPES=True)

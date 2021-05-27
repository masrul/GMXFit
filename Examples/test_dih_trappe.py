from GMXFit.TraPPE import TrappePES
from GMXFit.FitPES import DihedralFit


# Create a TrappePES object
trappe_pes = TrappePES()

# collect coeffs from TraPPE website/literature
trappe_coeffs = (0.00, 355.03, -68.19, 791.32)
trappe_funType = "CosineA"  # CosineC is also supported

# Pass function type and coeffs to create PES
trappe_pes.createPES(dihType=trappe_funType, coeffs=trappe_coeffs)

# Pass data object to PES Fitter
dihFit = DihedralFit(trappe_pes)

# Fit
dihFit.Fit(fitType="DihFourier", drawPES=True)

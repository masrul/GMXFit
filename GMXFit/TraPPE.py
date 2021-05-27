from GMXFit.UnitConverter import DegreeToRadian, KelvinToKJ
import numpy as np


class TrappePES:
    """
    This class is used to convert dihedral potential from
    TraPPE force field to gromacs format
    """

    def __init__(self):
        self.InternalCoords = np.linspace(-180, 181, num=180) * DegreeToRadian
        self.Energies = np.zeros(360)

    def createPES(self, dihType, coeffs):
        self.coeffs = np.array(coeffs) * KelvinToKJ
        if dihType == "CosineA":
            self.CosineA()
        elif dihType == "CosineC":
            self.CosineC()

    def CosineA(self):
        c0, c1, c2, c3 = self.coeffs
        x = self.InternalCoords

        self.Energies = (
            c0
            + c1 * (1 + np.cos(x))
            + c2 * (1 - np.cos(2 * x))
            + c3 * (1 + np.cos(3 * x))
        )

    def CosineC(self):
        c0, c1, c2, c3, c4, c5, c6 = self.coeffs
        x = self.InternalCoords
        self.Energies = (
            c0
            + c1 * (np.cos(x))
            + c2 * (np.cos(2 * x))
            + c3 * (np.cos(3 * x))
            + c4 * (np.cos(4 * x))
            + c5 * (np.cos(5 * x))
            + c6 * (np.cos(6 * x))
        )

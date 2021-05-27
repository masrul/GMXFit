import numpy as np
from GMXFit.UnitConverter import DegreeToRadian, AtomicUnitToKJ
from GMXFit.Util import fixAngleRange


class GaussScan:
    """
    It scans through gaussian log/out file, and collects
    scanned dihedral/angle & energies
    """

    def __init__(self, dataFile):
        self.dataFile = dataFile
        self.InternalCoords = []
        self.Energies = []
        self.read()
        self.convert()

    def read(self):
        fileExtension = self.dataFile.split(".")[-1]

        if fileExtension == "out" or fileExtension == "log":
            self.readGaussLog()
        elif fileExtension == "txt":
            self.readGaussScanTxt()
        else:
            raise RuntimeError("Unsupported file extension (.%s)" % (fileExtension))

    def readGaussLog(self):
        gFH = open(self.dataFile, "r")
        lines = gFH.readlines()
        gFH.close()

        # get scanning coordinate information
        for line in lines:
            if line.strip().startswith("!") and ("Scan" in line):
                InternalCoordIndex = (
                    line.split()[2][1:].replace("(", "").replace(")", "").split(",")
                )
                InternalCoordIndex = [int(key) for key in InternalCoordIndex]
                InternalCoordName = line.split()[1]
                if len(InternalCoordIndex) == 2:
                    print(
                        "Scanned bond [%s] : %d-%d"
                        % (
                            InternalCoordName,
                            InternalCoordIndex[0],
                            InternalCoordIndex[1],
                        )
                    )
                elif len(InternalCoordIndex) == 3:
                    print(
                        "Scanned angle [%s] : %d-%d-%d"
                        % (
                            InternalCoordName,
                            InternalCoordIndex[0],
                            InternalCoordIndex[1],
                            InternalCoordIndex[2],
                        )
                    )
                elif len(InternalCoordIndex) == 4:
                    print(
                        "Scanned dihedral [%s] : %d-%d-%d-%d"
                        % (
                            InternalCoordName,
                            InternalCoordIndex[0],
                            InternalCoordIndex[1],
                            InternalCoordIndex[2],
                            InternalCoordIndex[3],
                        )
                    )
                break

        # collect internal coordinate and energy
        getCoord = False
        for line in lines:
            if "SCF Done" in line:
                energy = float(line.split("=")[1].split()[0])
            elif "Optimization completed" in line:
                self.Energies.append(energy)

            elif "Optimization stopped" in line:
                self.Energies.append(energy)
                print("Warning : Convergence failure detected!")

            elif "Optimized Parameters" in line:
                getCoord = True

            elif getCoord and ("!" and InternalCoordName in line):
                self.InternalCoords.append(float(line.split(")")[1].split()[0]))
                getCoord = False

    def readGaussScanTxt(self):
        gFH = open(self.dataFile, "r")
        lines = gFH.readlines()
        gFH.close()

        for line in lines:
            if line.startswith("#"):
                continue
            else:
                keys = [float(key) for key in line.split()]
                self.InternalCoords.append(keys[0])
                self.Energies.append(keys[1])

    def convert(self):

        self.InternalCoords = [fixAngleRange(angle) for angle in self.InternalCoords]

        self.InternalCoords = np.array(self.InternalCoords)
        self.Energies = np.array(self.Energies)
        minEnergy = min(self.Energies)

        self.InternalCoords *= DegreeToRadian
        self.Energies = (self.Energies - minEnergy) * AtomicUnitToKJ

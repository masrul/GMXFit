from GMXFit.UnitConverter import RadianToDegree, DegreeToRadian
from GMXFit.Plotter import Plotter
import numpy as np
import scipy.optimize


class DihedralFit:
    def __init__(self, dataObj):
        self.x = dataObj.InternalCoords
        self.y = dataObj.Energies

    def Fit(self, fitType="DihRB", drawPES=False):
        self.drawPES = drawPES
        self.fitType = fitType
        if fitType == "DihRB":
            self.fitRB()
        elif fitType == "DihFourier":
            self.fitFourier()

    def fitRB(self):
        self.popt, _ = scipy.optimize.curve_fit(self.DihedralRB, self.x, self.y)
        a0, a1, a2, a3, a4, a5 = self.popt
        self.yFit = self.DihedralRB(self.x, a0, a1, a2, a3, a4, a5)
        self.getR2()

        # printing
        print("o FitType: Rychart-Bellman")
        print(
            "o Coefficients: %.8f  %.8f  %.8f  %.8f  %.8f  %.8f"
            % (a0, a1, a2, a3, a4, a5)
        )
        print("o R-sqaure: %.3f" % self.R2)

        # plotting
        self.xDraw = np.linspace(-np.pi, np.pi, num=1000)
        self.yDraw = self.DihedralRB(self.xDraw, a0, a1, a2, a3, a4, a5)

        if self.drawPES:
            self.plot()

    def fitFourier(self):
        self.popt, _ = scipy.optimize.curve_fit(self.DihedralFourier, self.x, self.y)
        F1, F2, F3, F4 = self.popt
        self.yFit = self.DihedralFourier(self.x, F1, F2, F3, F4)
        self.getR2()

        # printing
        print("FitType: Fourier")
        print("Coefficients: %.8f  %.8f  %.8f  %.8f" % (F1, F2, F3, F4))
        print("R-sqaure: %.3f" % self.R2)

        # plotting
        self.xDraw = np.linspace(-np.pi, np.pi, num=1000)
        self.yDraw = self.DihedralFourier(self.xDraw, F1, F2, F3, F4)
        if self.drawPES:
            self.plot()

    def getR2(self):
        yMean = np.mean(self.y)

        ssr = np.sum((self.y - self.yFit) ** 2)
        sst = np.sum((self.y - yMean) ** 2)
        self.R2 = 1 - ssr / sst

    def plot(self):
        pl = Plotter(plotType=self.fitType)
        pl.scatterPlot(self.x * RadianToDegree, self.y)
        pl.linePlot(self.xDraw * RadianToDegree, self.yDraw)
        pl.finalize()

    @staticmethod
    def DihedralFourier(x, F1, F2, F3, F4):
        return 0.5 * (
            F1 * (1 + np.cos(x))
            + F2 * (1 - np.cos(2 * x))
            + F3 * (1 + np.cos(3 * x))
            + F4 * (1 - np.cos(4 * x))
        )

    @staticmethod
    def DihedralRB(x, a0, a1, a2, a3, a4, a5):
        return (
            a0
            - a1 * np.cos(x)
            + a2 * (np.cos(x)) ** 2
            - a3 * (np.cos(x)) ** 3
            + a4 * (np.cos(x)) ** 4
            - a5 * (np.cos(x)) ** 5
        )


class AngleFit:
    def __init__(self, dataObj):
        self.x = dataObj.InternalCoords
        self.y = dataObj.Energies

    def Fit(self, fitType="AngleHarmonic"):
        self.fitType = fitType
        if fitType == "AngleHarmonic":
            self.fitHarmonic()

    def fitHarmonic(self):
        self.popt, _ = scipy.optimize.curve_fit(
            self.AngleHarmonic, self.x, self.y, p0=(max(self.x), 1000.0)
        )
        x_eq, k = self.popt
        self.yFit = self.AngleHarmonic(self.x, x_eq, k)
        self.getR2()

        # printing
        print("o FitType: Angle Harmonic ")
        print("o Force constant: %.8f kJ/mol/nm^2" % (k))
        print("o Equilibrium angle: %.2f " % (x_eq * RadianToDegree))
        print("o R-sqaure: %.3f" % self.R2)

        # plotting
        self.xDraw = np.linspace(
            x_eq - 5 * DegreeToRadian, x_eq + 5 * DegreeToRadian, num=1000
        )
        self.yDraw = self.AngleHarmonic(self.xDraw, x_eq, k)
        self.plot()

    def plot(self):
        pl = Plotter(plotType=self.fitType)
        pl.scatterPlot(self.x * RadianToDegree, self.y)
        pl.linePlot(self.xDraw * RadianToDegree, self.yDraw)
        pl.finalize()

    @staticmethod
    def AngleHarmonic(x, x_eq, k):
        return 0.5 * k * (x - x_eq) ** 2.0

    def getR2(self):
        yMean = np.mean(self.y)

        ssr = np.sum((self.y - self.yFit) ** 2)
        sst = np.sum((self.y - yMean) ** 2)
        self.R2 = 1 - ssr / sst

import matplotlib.pyplot as plt
from matplotlib import rc
from distutils.spawn import find_executable


# turn on latex if available.
if find_executable("latex"):
    rc("text", usetex=True)


class Plotter:
    def __init__(self, plotType):
        fig = plt.figure(figsize=(10, 8), facecolor="black")
        self.ax = fig.add_axes([0.1, 0.1, 0.8, 0.75])
        self.ax.set(facecolor="black")
        self.textColor = "orange"
        self.bgColor = "black"
        self.plotType = plotType

    def setLook(self):
        self.ax.set_xlabel(self.xlabel, fontsize=16, color=self.textColor)

        self.ax.set_ylabel(
            self.ylabel, fontsize=16, color=self.textColor,
        )

        self.ax.set_title(
            self.title, fontsize=14, position=(0.5, 1.10), color=self.textColor,
        )

        legend = self.ax.legend(
            ncol=2,
            loc="center",
            fancybox=True,
            framealpha=1.0,
            bbox_to_anchor=(0.5, 01.0),
            fontsize=16,
            facecolor=self.bgColor,
        )
        legend.get_frame().set_edgecolor("white")
        for text in legend.get_texts():
            text.set_color(self.textColor)

        self.ax.set_ylim(0, self.ax.get_ylim()[1] * 1.15)
        self.ax.grid(linewidth=0.30, zorder=0, color="pink")
        self.ax.set_axisbelow(True)
        self.ax.set_facecolor(self.bgColor)

        if self.plotType != "AngleHarmonic":
            self.ax.xaxis.set_major_locator(plt.MultipleLocator(60))
            self.ax.set_xlim(-180, 180)

        for spine in ["bottom", "top", "right", "left"]:
            self.ax.spines[spine].set_color("white")
        self.ax.tick_params(axis="both", colors="white", direction="inout")

    def setTxt(self):

        # Fourier eqation
        FourierEqTxt = r"$U_\mathrm{dih}(\phi)=$"
        FourierEqTxt += r"$\frac{1}{2}$"
        FourierEqTxt += r"$\mathrm{[F_1~(1+cos{\phi})}$"
        FourierEqTxt += r"$\mathrm{~+~F_2~(1-cos{2\phi})}$"
        FourierEqTxt += r"$\mathrm{~+~F_3~(1+cos{3\phi})}$"
        FourierEqTxt += r"$\mathrm{~+~F_4~(1-cos{4\phi})]}$"

        # Rychart-Bellman eqation
        RBEqTxt = r"$U_\mathrm{dih}(\phi)=$"
        RBEqTxt += r"$\mathrm{a_0}$"
        RBEqTxt += r"$\mathrm{-a_1~cos(\phi)}$"
        RBEqTxt += r"$\mathrm{+a_2~cos^2(\phi)}$"
        RBEqTxt += r"$\mathrm{-a_3~cos^3(\phi)}$"
        RBEqTxt += r"$\mathrm{+a_4~cos^4(\phi)}$"
        RBEqTxt += r"$\mathrm{-a_5~cos^5(\phi)}$"

        # Harmonic Angle
        HarAngEqTxt = r"$U_\mathrm{angle}(\theta)=$"
        HarAngEqTxt += r"$\frac{1}{2}(\theta-\theta_\mathrm{eq})^2$"

        # label for dihedral
        dihXLabel = r"$\phi~[^o]$"
        dihYLabel = r"$U_\mathrm{dih}(\phi)~\mathrm{[kJ/mol]}$"

        # label for angle
        angleXLabel = r"$\theta~[^o]$"
        angleYLabel = r"$U_\mathrm{angle}(\theta)~\mathrm{[kJ/mol]}$"

        if self.plotType == "AngleHarmonic":
            self.xlabel = angleXLabel
            self.ylabel = angleYLabel
            self.title = r"$\mathrm{Fitting~for:~}$" + HarAngEqTxt
        elif self.plotType == "DihRB":
            self.xlabel = dihXLabel
            self.ylabel = dihYLabel
            self.title = r"$\mathrm{Fitting~for:~}$" + RBEqTxt
        elif self.plotType == "DihFourier":
            self.xlabel = dihXLabel
            self.ylabel = dihYLabel
            self.title = r"$\mathrm{Fitting~for:~}$" + FourierEqTxt

    def scatterPlot(self, x, y, label=r"$\mathrm{Data}$"):
        self.ax.scatter(
            x,
            y,
            marker="o",
            edgecolor="aqua",
            facecolor=self.bgColor,
            s=60,
            label=label,
            linewidths=1.5,
        )

    def linePlot(self, x, y, label=r"$\mathrm{Fitted}$"):
        self.ax.plot(x, y, linewidth=1.5, label=label, color="red")

    def finalize(self):
        self.setTxt()
        self.setLook()
        plt.show()

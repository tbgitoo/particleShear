from .EvaluationHandler import EvaluationHandler

class EvaluationHandlerPlotter(EvaluationHandler):
    def __init__(self, theTk, theCanvas, x_scale=1, y_scale_strain=1, y_scale_force=1, r=10, offset_x=0, offset_y=0,
                 plotStress=True):
        self.plotStress=plotStress
        super(EvaluationHandlerPlotter, self).__init__()
        self.theTk = theTk
        self.theCanvas = theCanvas
        self.x_scale = x_scale
        self.y_scale_strain = y_scale_strain
        self.y_scale_force = y_scale_force
        self.r = r
        self.offset_x = offset_x
        self.offset_y = offset_y



    def record(self, theEnsemble,theEvaluator=False):
        super(EvaluationHandlerPlotter, self).record(theEnsemble,theEvaluator)

        if self.plotStress:
            t = self.t[len(self.t) - 1]
            strain = self.strain[len(self.strain) - 1]
            force = self.force[len(self.force) - 1]
            shear_stress = self.shear_stress[len(self.shear_stress) - 1]

            self.plot(t, strain, force - self.force[0], shear_stress - self.shear_stress[0])



    def plot(self, t, strain, force,shear_stress):
        # First, x coordinates (common)



        x1 = t * self.x_scale - self.r + self.offset_x
        x2 = x1 + 2 * self.r



        # Then, y for volume shear stress
        y1 = -shear_stress * self.y_scale_force - self.r + self.offset_y #Here, the minus sign is just because of the inverted
        # coordinate system of the canvas graphics (tkinter)
        y2 = y1 + 2 * self.r
        self.theCanvas.create_oval(x1, y1, x2, y2, fill="red",outline="red")

        # Then, y for force
        y1 = -force * self.y_scale_force - self.r + self.offset_y  # Here, the minus sign is just because of the inverted
        # coordinate system of the canvas graphics (tkinter)
        y2 = y1 + 2 * self.r
        self.theCanvas.create_oval(x1, y1, x2, y2, fill="blue", outline="blue")

        # Then, y for strain
        y1 = -strain * self.y_scale_strain - self.r + self.offset_y
        y2 = y1 + 2 * self.r
        self.theCanvas.create_oval(x1, y1, x2, y2, fill="green",outline="green")
        self.theTk.update()

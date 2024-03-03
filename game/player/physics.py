from attr import define


@define
class Physics:
    x: int
    y: int
    x_velocity: float
    y_velocity: float

    def euler(self):
        ...

    def midpoint(self):
        ...

    def runge_kutta(self, order: int = 2):
        ...

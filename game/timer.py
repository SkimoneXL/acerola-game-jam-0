from attr import define
from pygame.time import Clock

from game import game_clock


@define(kw_only=True)
class Timer:
    duration_millis: int
    clock: Clock = game_clock
    cumulative_millis: float = 0.0
    done: bool = False

    def update(self):
        if self.done: return
        self.cumulative_millis += self.clock.get_time()
        if self.cumulative_millis >= self.duration_millis:
            self.done = True

    def reset(self):
        self.cumulative_millis = 0
        self.done = 0

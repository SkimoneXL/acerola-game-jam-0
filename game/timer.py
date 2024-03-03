from attr import define
from pygame.time import Clock
from game import game_clock


@define(kw_only=True)
class Timer:
    duration: int
    _clock: Clock = game_clock
    _cumulative_time: float = 0.0
    done: bool = False

    def update(self):
        if self.done: return
        self._cumulative_time += self._clock.get_time()
        if self._cumulative_time >= self.duration:
            self.done = True

    def __bool__(self):
        return self.done

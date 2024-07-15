from attr import define
from pygame.event import Event, post
from pygame.time import Clock

from game import game_clock


@define(kw_only=True, slots=True)
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
        self.done = False


@define(frozen=True, kw_only=True, slots=True)
class FixedUpdate:
    fixed_update_timer: Timer
    updates_per_second: int
    event_type: int

    @property
    def millis_per_update(self):
        return 1000 / self.updates_per_second

    @staticmethod
    def create(*, event_type: int, updates_per_second: int = 240):
        return FixedUpdate(
            fixed_update_timer=Timer(duration_millis=1000 / updates_per_second),
            updates_per_second=updates_per_second,
            event_type=event_type,
        )

    def update(self):
        self.fixed_update_timer.update()
        if self.fixed_update_timer.done:
            post(Event(
                self.event_type,
                time=self.fixed_update_timer.cumulative_millis,
            ))
            self.fixed_update_timer.reset()

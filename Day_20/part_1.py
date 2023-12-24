from dataclasses import dataclass, field
from collections import deque
from typing import Optional


LOW_PULSE = False
HIGH_PULSE = True


@dataclass(frozen=True)
class Pulse:
    module_name: str
    pulse: bool
    source: str


@dataclass
class Module:
    destinations: list[str] = field(default_factory=lambda: list())

    def receive_pulse(self, pulse: bool, _: str) -> Optional[bool]:
        return pulse


@dataclass
class FlipFlopModule(Module):
    is_on: bool = False

    def receive_pulse(self, pulse: bool, _: str) -> Optional[bool]:
        if pulse:
            # Do nothing if the pulse is a high pulse
            return None

        self.is_on = not self.is_on
        return self.is_on


@dataclass
class ConjonctionModule(Module):
    last_pulses: dict[str, bool] = field(default_factory=lambda: dict())

    def init_state(self, module_name: str):
        self.last_pulses[module_name] = LOW_PULSE

    def receive_pulse(self, pulse: bool, source_module: str) -> Optional[bool]:
        self.last_pulses[source_module] = pulse
        return not all(self.last_pulses.values())


def load_input(input_path: str = "input.txt") -> list[str]:
    with open(input_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line]


def parse_input(
    input_path: str = "input.txt",
) -> dict[str, Module]:
    modules = {"rx": Module(), "output": Module()}
    for line in load_input(input_path):
        module_name, module_destinations = line.split(" -> ")

        module_type = Module
        if module_name[0] == "%":
            module_type = FlipFlopModule
            module_name = module_name[1:]

        if module_name[0] == "&":
            module_type = ConjonctionModule
            module_name = module_name[1:]

        module_destinations = module_destinations.split(", ")
        modules[module_name] = module_type(destinations=module_destinations)

    # init conjonctions
    for name, module in modules.items():
        for destination in module.destinations:
            if isinstance(modules[destination], ConjonctionModule):
                modules[destination].init_state(name)

    return modules


def apply_modules(modules: dict[str, Module]):
    pulses = deque([Pulse("broadcaster", LOW_PULSE, "")])
    i = 0
    high, low = 0, 0
    while pulses:
        i += 1
        pulse = pulses.popleft()

        if pulse.pulse:
            high += 1
        else:
            low += 1

        if pulse.module_name not in modules:
            continue

        module = modules[pulse.module_name]
        result = module.receive_pulse(pulse.pulse, pulse.source)

        if result is None:
            continue

        for destination in module.destinations:
            # print(f"{pulse.module_name} -{'high' if result else 'low'}-> {destination}")
            pulses.append(Pulse(destination, result, pulse.module_name))

    return high, low


def main():
    modules = parse_input()

    N = 1000
    high, low = 0, 0
    for _ in range(N):
        h, l = apply_modules(modules)
        high += h
        low += l

    print(f"{high=} {low=} {high * low=}")


if __name__ == "__main__":
    main()

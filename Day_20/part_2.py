from dataclasses import dataclass, field
from collections import deque, defaultdict
from typing import Optional
import math

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
class Output(Module):
    def receive_pulse(self, pulse: bool, _: str) -> Optional[bool]:
        if pulse is LOW_PULSE:
            exit()

        return None


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
    modules = {"rx": Output()}
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


def apply_modules(
    modules: dict[str, Module], modules_to_watch: set[str]
) -> dict[str, bool]:
    returned = {module_name: False for module_name in modules_to_watch}
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
        if pulse.module_name in returned and result == HIGH_PULSE:
            returned[pulse.module_name] = True

        if result is None:
            continue

        for destination in module.destinations:
            # print(f"{pulse.module_name} -{'high' if result else 'low'}-> {destination}")
            pulses.append(Pulse(destination, result, pulse.module_name))

    return returned


def print_mermaid_graph(
    modules: dict[str, Module],
    output: Optional[str] = "rx",
    distance_from_goal: Optional[int] = 3,
):
    parents = defaultdict(list)
    for name, module in modules.items():
        for dest in module.destinations:
            parents[dest].append(name)

    print("graph LR")
    passed = set()

    def print_childs(module_name: str, depth: int):
        if module_name in passed:
            return
        passed.add(module_name)

        for parent in parents[module_name]:
            if isinstance(modules[module_name], ConjonctionModule):
                print(f"    {parent} --> {module_name}{{{module_name}}}")
            else:
                print(f"    {parent} --> {module_name}[{module_name}]")
            if depth < distance_from_goal:
                print_childs(parent, depth + 1)

    print_childs(output, 0)

    # for name, module in modules.items():
    #     for dest in module.destinations:


def get_nodes_that_matters(
    modules: dict[str, Module], output: str, depth_goal: int = 1
) -> set[str]:
    passed = set()
    parents = defaultdict(list)
    for name, module in modules.items():
        for dest in module.destinations:
            parents[dest].append(name)

    nodes_that_matters = set()

    def find_nodes_that_matters(module_name: str, depth: int):
        if module_name in passed:
            return
        passed.add(module_name)
        if depth > depth_goal:
            return

        for parent in parents[module_name]:
            if depth == depth_goal:
                nodes_that_matters.add(parent)
            else:
                find_nodes_that_matters(parent, depth + 1)

    find_nodes_that_matters(output, 0)

    return nodes_that_matters


def main():
    modules = parse_input()
    # print_mermaid_graph(modules, "rx", 3)

    # find the modules that are part of the cycle
    modules_that_matters = get_nodes_that_matters(modules, "rx", 1)
    # print(f"{modules_that_matters=}")

    counts_for_lcm = {}

    i = 1
    while True:
        returned = apply_modules(modules, modules_that_matters)
        for name, has_low in returned.items():
            if has_low and name not in counts_for_lcm:
                counts_for_lcm[name] = i

        if len(counts_for_lcm) == len(modules_that_matters):
            break

        i += 1

    print(math.lcm(*counts_for_lcm.values()))


if __name__ == "__main__":
    main()

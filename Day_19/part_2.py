from dataclasses import dataclass
from typing import Optional
from functools import reduce, cache


@dataclass(frozen=True)
class Verification:
    category: str
    operation: str
    value: int
    destination: str

    def get_possible_values(self) -> tuple[frozenset[int], frozenset[int]]:
        if self.operation == ">":
            # valid (> value), invalid (<= value)
            return frozenset(range(self.value + 1, 4001)), frozenset(
                range(1, self.value + 1)
            )
        # valid (< value), invalid (>= value)
        return frozenset(range(1, self.value)), frozenset(range(self.value, 4001))

    @staticmethod
    def parse(raw_verification: str) -> "Verification":
        category = raw_verification[0]
        operation = raw_verification[1]
        value, destination = raw_verification[2:].split(":")
        return Verification(category, operation, int(value), destination)


@dataclass(frozen=True)
class Workflow:
    checks: list[Verification]
    destination: str

    @staticmethod
    def parse(raw_workflow: str) -> tuple[str, "Workflow"]:
        name, content = raw_workflow[:-1].split("{")
        splited_content = content.split(",")
        destination = splited_content[-1]
        checks = []
        for raw_verification in splited_content[:-1]:
            checks.append(Verification.parse(raw_verification))

        return name, Workflow(checks, destination)


def parse_rating(raw_rating: str) -> dict[str, int]:
    raw_rating = raw_rating[1:-1]
    dict_values = {}
    for definition in raw_rating.split(","):
        key = definition[0]
        value = int(definition[2:])
        dict_values[key] = value
    return dict_values


def load_input(input_path: str = "input.txt") -> list[str]:
    with open(input_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f]


def compute_workflow(
    workflows: dict[str, Workflow], workflow_name: str, sets: dict[str, frozenset[int]]
) -> int:
    if workflow_name == "R":
        return 0
    elif workflow_name == "A":
        total = 1
        for s in sets.values():
            total *= len(s)
        return total

    total = 0
    workflow = workflows[workflow_name]

    # copy the given sets so we don't update the ones from the parent workflow
    sets = {k: v.copy() for k, v in sets.items()}
    for check in workflow.checks:
        valid, invalid = check.get_possible_values()

        sets_copy = {k: v.copy() for k, v in sets.items()}

        # check is invalid so we continue
        sets[check.category] = sets[check.category].intersection(invalid)

        # check is valid so we go to its destination
        sets_copy[check.category] = sets_copy[check.category].intersection(valid)
        total += compute_workflow(workflows, check.destination, sets_copy)

    return total + compute_workflow(workflows, workflow.destination, sets)


def main():
    workflows = {}
    for line in load_input():
        if not line:
            # finished parsing workflows
            break

        name, w = Workflow.parse(line)
        workflows[name] = w

    sets = {
        "a": frozenset(range(1, 4001)),
        "s": frozenset(range(1, 4001)),
        "m": frozenset(range(1, 4001)),
        "x": frozenset(range(1, 4001)),
    }

    total = compute_workflow(workflows, "in", sets)
    print(total)


if __name__ == "__main__":
    main()

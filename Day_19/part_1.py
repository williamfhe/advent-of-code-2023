from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Verification:
    category: str
    operation: str
    value: int
    destination: str

    def apply(self, rating: dict[str, int]) -> Optional[str]:
        value = rating[self.category]
        if self.apply_operation(value):
            return self.destination

        return None

    def apply_operation(self, value: int) -> bool:
        if self.operation == ">":
            return value > self.value

        return value < self.value

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

    def apply(self, rating: dict[str, int]) -> Optional[str]:
        for check in self.checks:
            destination_workflow = check.apply(rating)
            if destination_workflow:
                return destination_workflow
        return self.destination

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


def is_rating_valid(rating: dict[str, int], workflows: list[Workflow]) -> bool:
    workflow_name = "in"
    while workflow_name and workflow_name not in ("A", "R"):
        workflow_name = workflows[workflow_name].apply(rating)

    return workflow_name == "A"


def main():
    workflows = {}
    parsing_workflow = True
    total_sum = 0
    for line in load_input():
        if not line:
            parsing_workflow = False
            continue

        if parsing_workflow:
            name, w = Workflow.parse(line)
            workflows[name] = w
            continue

        rating = parse_rating(line)
        if is_rating_valid(rating, workflows):
            total_sum += sum(rating.values())

    print(total_sum)


if __name__ == "__main__":
    main()

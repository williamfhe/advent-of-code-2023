from dataclasses import dataclass
import math


@dataclass(frozen=True)
class MapNode:
    current: str
    left: str
    right: str


def load_input(input_path: str = "input.txt") -> list[str]:
    with open(input_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line]


def parse_input(input_path: str = "input.txt") -> tuple[str, dict[str, MapNode]]:
    challenge_input = load_input(input_path)
    instructions = challenge_input[0]
    map_nodes = {}
    for map_node in challenge_input[2:]:
        if not map_node:
            continue

        node_name = map_node[:3]
        left = map_node[7:10]
        right = map_node[12:15]
        map_nodes[node_name] = MapNode(node_name, left, right)

    return instructions, map_nodes


def compute_steps_to_z(
    starting_position: str, instructions: str, map_nodes: dict[str, MapNode]
) -> int:
    steps = 0
    current_position = starting_position
    while True:
        if current_position[2] == "Z":
            return steps

        current_node = map_nodes[current_position]
        direction = instructions[steps % len(instructions)]

        if direction == "L":
            current_position = current_node.left
        else:
            current_position = current_node.right

        steps += 1


def compute_min_steps_for_all(instructions: str, map_nodes: dict[str, MapNode]) -> int:
    starting_nodes = list(filter(lambda n: n[2] == "A", map_nodes.keys()))
    steps_to_first_z = [
        compute_steps_to_z(node, instructions, map_nodes) for node in starting_nodes
    ]

    # tried the Least Common Multiple because forcebrute wasn't working
    # somehow it works because the traveled path to an exit is cyclic
    # wtf ???
    return math.lcm(*steps_to_first_z)


def main():
    instructions, map_nodes = parse_input()
    steps_to_z = compute_min_steps_for_all(instructions, map_nodes)
    print(steps_to_z)


if __name__ == "__main__":
    main()

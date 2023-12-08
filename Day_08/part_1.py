from dataclasses import dataclass


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


def compute_steps_to_z(instructions: str, map_nodes: dict[str, MapNode]) -> int:
    steps = 0
    current_position = "AAA"
    while current_position != "ZZZ":
        current_node = map_nodes[current_position]
        direction = instructions[steps % len(instructions)]
        if direction == "L":
            current_position = current_node.left
        else:
            current_position = current_node.right
        steps += 1

    return steps


def main():
    instructions, map_nodes = parse_input()
    steps_to_z = compute_steps_to_z(instructions, map_nodes)
    print(steps_to_z)


if __name__ == "__main__":
    main()

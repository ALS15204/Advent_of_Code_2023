from math import lcm
from pathlib import Path
from aoc_2023.day_20.model import Broadcaster, FlipFlop, Conjunction, CACHE, Pulse, Output, WATCH, RECORD


SCRIPT_DIR = Path(__file__).parent
INPUT_DATA = SCRIPT_DIR / "input.dat"


def main():
    with open(INPUT_DATA) as f:
        data = f.read().splitlines()
    module_to_connections = {}
    id_to_module = {}
    for line in data:
        module, connection_str = line.split(" -> ")
        if module.startswith("b"):
            module = Broadcaster(module, [])
        elif module.startswith("%"):
            module = FlipFlop(module.strip("%"), [])
        elif module.startswith("&"):
            module = Conjunction(module.strip("&"), [])
        module_to_connections[module] = connection_str.split(", ")
        id_to_module[module.id] = module
    for module, connections in module_to_connections.items():
        for connection in connections:
            if connection not in id_to_module:
                destination = Output(id=connection, connections=[])
            else:
                destination = id_to_module[connection]
            module.add_connection(destination)
            if type(destination) is Conjunction:
                destination.add_parent(module)
    module_to_connections = None
    for _ in range(1000):
        CACHE[Pulse.LOW] += 1
        id_to_module["broadcaster"].trigger(Pulse.LOW)
    print(f"Answer to part 1: {CACHE[Pulse.LOW] * CACHE[Pulse.HIGH]}")

    CACHE.clear()
    CACHE[Pulse.LOW] = 0
    CACHE[Pulse.HIGH] = 0
    for i in range(1000000000000000):
        id_to_module["broadcaster"].trigger(Pulse.LOW, ntry=i)
        if all(v > 0 for v in RECORD.values()):
            count = lcm(*RECORD.values())
            break
    print(f"Answer to part 2: {count}")


if __name__ == "__main__":
    main()
from abc import ABC
from enum import Enum
from typing import List


class Pulse(Enum):
    HIGH = "high"
    LOW = "low"


CACHE = {Pulse.LOW: 0, Pulse.HIGH: 0}
WATCH = ["vg", "kp", "gc", "tx"]
RECORD = dict.fromkeys(WATCH, 0)


class Module(ABC):

    def __init__(self, id: str, connections: List["Module"] = []):
        self.id = id
        self.connections = connections

    def __repr__(self):
        return f"Module_{self.id}"

    def trigger(self, signal: Pulse, source: "Module" = None, ntry: int = 0):
        if signal:
            for connection in self.connections:
                CACHE[signal] += 1
                connection.trigger(signal, source=source, ntry=ntry)

    def add_connection(self, connection: "Module"):
        self.connections.append(connection)


class Broadcaster(Module):
    def __init__(self, id: str, connections: List[Module]):
        super().__init__(id, connections)

    def __repr__(self):
        return f"Broadcast_{self.id}"


class FlipFlop(Module):

    def __init__(self, id: str, connections: List[Module], state: bool = False):
        super().__init__(id, connections)
        self.state = state

    def __repr__(self):
        return f"FlipFlop_{self.id}({self.state})"
    
    def trigger(self, signal: Pulse, source: Module = None, ntry: int = 0):
        out_signal = None
        if signal == Pulse.LOW:
            if self.state:
                out_signal = Pulse.LOW
            else:
                out_signal = Pulse.HIGH
            self._flip()
        super().trigger(out_signal, self, ntry=ntry)

    def _flip(self):
        self.state = not self.state


class Conjunction(Module):

    def __init__(self, id: str, connections: List[Module]):
        super().__init__(id, connections)
        self.memory = {}

    def __repr__(self):
        return f"Conjunction_{self.id}"

    def add_parent(self, parent: Module):
        self.memory[parent] = Pulse.LOW

    def trigger(self, signal: Pulse, source: Module = None, ntry: int = 0):
        out_signal = None
        self.memory[source] = signal
        if all(mem_signal == Pulse.HIGH for mem_signal in self.memory.values()):
            out_signal = Pulse.LOW
        else:
            out_signal = Pulse.HIGH
        super().trigger(out_signal, self, ntry=ntry)


class Output(Module):
    
        def __init__(self, id: str, connections: List[Module]):
            super().__init__(id, connections)
    
        def __repr__(self):
            return f"Output_{self.id}"
    
        def trigger(self, signal: Pulse, source: Module = None, ntry: int = 0):
            if self.id == "rx":
                if ntry > 0 and any(signal == Pulse.HIGH for signal in source.memory.values()):
                    high = [key for key, value in source.memory.items() if value == Pulse.HIGH]
                    for key in high:
                        RECORD[key.id] = ntry
            pass

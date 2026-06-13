#!/usr/bin/env python3
"""Generate minimal .nbt structure files for RedScope GameTests.
Run: python tools/generate_test_structures.py
"""
import gzip
import struct
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Any

TAG_END = 0
TAG_BYTE = 1
TAG_SHORT = 2
TAG_INT = 3
TAG_LONG = 4
TAG_FLOAT = 5
TAG_DOUBLE = 6
TAG_BYTE_ARRAY = 7
TAG_STRING = 8
TAG_LIST = 9
TAG_COMPOUND = 10
TAG_INT_ARRAY = 11
TAG_LONG_ARRAY = 12

@dataclass
class BlockEntry:
    name: str
    state: Dict[str, str] = field(default_factory=dict)
    pos: List[int] = field(default_factory=lambda: [0, 0, 0])

class NbtWriter:
    def __init__(self):
        self._buf = bytearray()

    def write_byte(self, v):
        self._buf += struct.pack(">b", v & 0xFF)

    def write_short(self, v):
        self._buf += struct.pack(">h", v)

    def write_int(self, v):
        self._buf += struct.pack(">i", v)

    def write_long(self, v):
        self._buf += struct.pack(">q", v)

    def write_float(self, v):
        self._buf += struct.pack(">f", v)

    def write_double(self, v):
        self._buf += struct.pack(">d", v)

    def write_string(self, v):
        b = v.encode('utf-8')
        self._buf += struct.pack(">h", len(b)) + b

    def _enc_name(self, name):
        b = name.encode('utf-8')
        return struct.pack(">h", len(b)) + b

    def _enc_value(self, name, value):
        if isinstance(value, bool):
            return struct.pack(">b", TAG_BYTE + 1) + self._enc_name(name) + struct.pack(">b", 1 if value else 0)
        elif isinstance(value, int):
            if -128 <= value <= 127:
                return struct.pack(">b", TAG_BYTE) + self._enc_name(name) + struct.pack(">b", value)
            elif -32768 <= value <= 32767:
                return struct.pack(">b", TAG_SHORT) + self._enc_name(name) + struct.pack(">h", value)
            else:
                return struct.pack(">b", TAG_INT) + self._enc_name(name) + struct.pack(">i", value)
        elif isinstance(value, float):
            return struct.pack(">b", TAG_DOUBLE) + self._enc_name(name) + struct.pack(">d", value)
        elif isinstance(value, str):
            b = value.encode('utf-8')
            return struct.pack(">b", TAG_STRING) + self._enc_name(name) + struct.pack(">h", len(b)) + b
        elif isinstance(value, list):
            return self._enc_array(name, value)
        elif isinstance(value, dict):
            return self._enc_compound(name, value)
        else:
            raise TypeError(f"Unsupported: {type(value)}")

    def _enc_compound(self, name, data):
        buf = bytearray()
        for k, v in data.items():
            buf += self._enc_value(k, v)
        buf += struct.pack(">b", TAG_END)
        return struct.pack(">b", TAG_COMPOUND) + self._enc_name(name) + struct.pack(">i", len(buf)) + bytes(buf)

    def _enc_array(self, name, items):
        if not items:
            payload = struct.pack(">b", TAG_END) + struct.pack(">i", 0)
            return struct.pack(">b", TAG_LIST) + self._enc_name(name) + payload
        first = items[0]
        if isinstance(first, int):
            if all(-128 <= i <= 127 for i in items):
                tag = TAG_BYTE_ARRAY
                payload = struct.pack(">b", TAG_BYTE) + struct.pack(">i", len(items)) + bytes(i & 0xFF for i in items)
            else:
                tag = TAG_INT_ARRAY
                payload = struct.pack(">b", TAG_INT) + struct.pack(">i", len(items)) + bytes(''.join(struct.pack(">i", i) for i in items))
        elif isinstance(first, str):
            tag = TAG_STRING
            buf = bytearray()
            for item in items:
                b = item.encode('utf-8')
                buf += struct.pack(">h", len(b)) + b
            payload = struct.pack(">b", TAG_STRING) + struct.pack(">i", len(items)) + bytes(buf)
        elif isinstance(first, dict):
            tag = TAG_LIST
            buf = bytearray()
            for item in items:
                inner = bytearray()
                for kk, vv in item.items():
                    if isinstance(vv, str):
                        inner += self._enc_str(kk, vv)
                    elif isinstance(vv, bool):
                        inner += self._enc_byte(kk, 1 if vv else 0)
                    elif isinstance(vv, int):
                        inner += self._enc_int(kk, vv)
                inner += struct.pack(">b", 0)
                buf += struct.pack(">b", 10) + self._enc_name(kk) + bytes(inner)
            payload = struct.pack(">b", TAG_LIST) + struct.pack(">i", len(items)) + bytes(buf)
        else:
            raise TypeError(f"Unsupported array item: {type(first)}")
        return struct.pack(">b", tag) + self._enc_name(name) + payload

    def _enc_str(self, name, s):
        b = s.encode('utf-8')
        return struct.pack(">b", TAG_STRING) + self._enc_name(name) + struct.pack(">h", len(b)) + b

    def _enc_int(self, name, v):
        return struct.pack(">b", TAG_INT) + self._enc_name(name) + struct.pack(">i", v)

    def _enc_byte(self, name, v):
        return struct.pack(">b", TAG_BYTE) + self._enc_name(name) + struct.pack(">b", v)

    def finalize(self, root_name):
        # Write the root compound tag
        root_tag = TAG_COMPOUND
        # Get the root data from _root
        data = self._root
        buf = bytearray()
        for k, v in data.items():
            buf += self._enc_value(k, v)
        buf += struct.pack(">b", TAG_END)
        # Write root tag: type + name + payload
        result = struct.pack(">b", root_tag)
        result += self._enc_name(root_name)
        result += struct.pack(">i", len(buf))
        result += bytes(buf)
        return result

def encode_nbt(data, root_name):
    """Encode NBT data to bytes."""
    w = NbtWriter()
    w._root = data
    
    # Write root compound tag
    root_tag = TAG_COMPOUND
    buf = bytearray()
    for k, v in data.items():
        buf += w._enc_value(k, v)
    buf += struct.pack(">b", TAG_END)
    
    result = struct.pack(">b", root_tag)
    result += w._enc_name(root_name)
    result += struct.pack(">i", len(buf))
    result += bytes(buf)
    return result

def write_nbt(name, blocks):
    OUT_DIR = Path(__file__).resolve().parent
    data = make_structure(blocks, size=[8, 4, 8], author="RedScope")
    raw = encode_nbt(data, name)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / f"{name}.nbt").write_bytes(raw)
    print(f"Wrote {OUT_DIR / name}.nbt ({len(raw)} bytes)")


def make_structure(blocks, size, author="RedScope"):
    return {
        "size": size,
        "entities": [],
        "blocks": [
            {
                "pos": b.pos,
                "state": {
                    "Name": b.name,
                    "Properties": b.state if b.state else {}
                },
            }
            for b in blocks
        ],
    }

STRUCTURES = {
    "redstone_line_16": [BlockEntry("minecraft:redstone_wire")],
    "piston_obsidian": [
        BlockEntry("minecraft:sticky_piston", {"facing": "east", "extended": "false"}),
        BlockEntry("minecraft:obsidian"),
    ],
    "comparator_wrong_mode": [
        BlockEntry("minecraft:comparator", {"facing": "east", "mode": "subtract", "powered": "false"}),
    ],
    "torch_burnout": [
        BlockEntry("minecraft:redstone_torch", {"facing": "west"}),
        BlockEntry("minecraft:redstone_wire"),
    ],
    "redstone_multiplexer": [
        BlockEntry("minecraft:repeater", {"facing": "south", "delay": "1", "locked": "false", "powered": "true"}),
    ],
    "double_piston_extender": [
        BlockEntry("minecraft:sticky_piston", {"facing": "east", "extended": "false"}),
        BlockEntry("minecraft:sticky_piston", {"facing": "west", "extended": "false"}),
    ],
    "t_flip_flop": [
        BlockEntry("minecraft:redstone_torch", {"facing": "north"}),
        BlockEntry("minecraft:repeater", {"facing": "east", "delay": "2", "locked": "false", "powered": "true"}),
    ],
    "hopper_clock": [
        BlockEntry("minecraft:hopper", {"facing": "east"}),
        BlockEntry("minecraft:hopper", {"facing": "west"}),
    ],
    "binary_counter": [
        BlockEntry("minecraft:comparator", {"facing": "east", "mode": "subtract", "powered": "false"}),
        BlockEntry("minecraft:redstone_torch", {"facing": "south"}),
    ],
    "repeater_wrong_direction": [
        BlockEntry("minecraft:repeater", {"facing": "north", "delay": "1", "locked": "false", "powered": "true"}),
        BlockEntry("minecraft:repeater", {"facing": "east", "delay": "1", "locked": "false", "powered": "false"}),
    ],
    "vertical_signal_chain": [
        BlockEntry("minecraft:redstone_wire"),
        BlockEntry("minecraft:redstone_wire"),
        BlockEntry("minecraft:redstone_wire"),
    ],
    "alu_slice": [
        BlockEntry("minecraft:comparator", {"facing": "east", "mode": "subtract", "powered": "false"}),
        BlockEntry("minecraft:repeater", {"facing": "south", "delay": "1", "locked": "false", "powered": "true"}),
        BlockEntry("minecraft:redstone_torch", {"facing": "west"}),
    ],
}

for name, data in STRUCTURES.items():
    write_nbt(name, data)

print(f"Done — {len(STRUCTURES)} structures written")
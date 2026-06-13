#!/usr/bin/env python3
"""Generate minimal .nbt structure files for RedScope GameTests.
Run: python tools/generate_test_structures.py
"""
import struct
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class BlockEntry:
    name: str
    state: Dict[str, str] = field(default_factory=dict)
    pos: List[int] = field(default_factory=lambda: [0, 0, 0])

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

def write_nbt(name, blocks):
    """Write a simple NBT structure file."""
    OUT_DIR = Path(__file__).resolve().parent.parent / "src" / "main" / "resources" / "structures"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Build NBT data
    buf = bytearray()
    
    # Root compound tag
    buf += struct.pack(">b", TAG_COMPOUND)
    buf += struct.pack(">h", 0)  # Empty root name
    buf += struct.pack(">i", 0)  # Will be replaced
    
    # Size list
    buf += struct.pack(">b", TAG_LIST)
    buf += struct.pack(">h", 4)
    buf += b'size'
    buf += struct.pack(">b", TAG_INT)
    buf += struct.pack(">i", 3)
    buf += struct.pack(">iii", 8, 4, 8)
    
    # Entities list (empty)
    buf += struct.pack(">b", TAG_LIST)
    buf += struct.pack(">h", 8)
    buf += b'entities'
    buf += struct.pack(">b", TAG_COMPOUND)
    buf += struct.pack(">i", 0)
    
    # Blocks list
    buf += struct.pack(">b", TAG_LIST)
    buf += struct.pack(">h", 6)
    buf += b'blocks'
    buf += struct.pack(">b", TAG_COMPOUND)
    
    blocks_data = bytearray()
    for block in blocks:
        block_entry = bytearray()
        # pos
        block_entry += struct.pack(">b", TAG_LIST)
        block_entry += struct.pack(">h", 3)
        block_entry += b'pos'
        block_entry += struct.pack(">b", TAG_INT)
        block_entry += struct.pack(">i", 3)
        block_entry += struct.pack(">iii", *block.pos)
        
        # state compound
        block_entry += struct.pack(">b", TAG_COMPOUND)
        block_entry += struct.pack(">h", 5)
        block_entry += b'state'
        
        state_data = bytearray()
        # Name
        name_bytes = block.name.encode('utf-8')
        state_data += struct.pack(">b", TAG_STRING)
        state_data += struct.pack(">h", 4)
        state_data += b'Name'
        state_data += struct.pack(">h", len(name_bytes)) + name_bytes
        
        # Properties
        if block.state:
            state_data += struct.pack(">b", TAG_COMPOUND)
            state_data += struct.pack(">h", 10)
            state_data += b'Properties'
            for k, v in block.state.items():
                k_bytes = k.encode('utf-8')
                v_bytes = v.encode('utf-8')
                state_data += struct.pack(">b", TAG_STRING)
                state_data += struct.pack(">h", len(k_bytes)) + k_bytes
                state_data += struct.pack(">h", len(v_bytes)) + v_bytes
            state_data += struct.pack(">b", TAG_END)
        
        state_data += struct.pack(">b", TAG_END)
        block_entry += struct.pack(">i", len(state_data)) + state_data
        block_entry += struct.pack(">b", TAG_END)
        blocks_data += struct.pack(">i", len(block_entry)) + block_entry
    
    buf += struct.pack(">i", len(blocks_data)) + blocks_data
    buf += struct.pack(">b", TAG_END)
    
    # End root compound
    buf += struct.pack(">b", TAG_END)
    
    # Fix the length field (bytes 5-8)
    payload_len = len(buf) - 9
    struct.pack_into(">i", buf, 5, payload_len)
    
    filepath = OUT_DIR / f"{name}.nbt"
    filepath.write_bytes(bytes(buf))
    print(f"Wrote {filepath} ({len(bytes(buf))} bytes)")

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
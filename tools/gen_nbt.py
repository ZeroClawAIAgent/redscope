import gzip, struct
from pathlib import Path

out = Path(__file__).resolve().parent / 'src' / 'main' / 'resources' / 'data' / 'redscope' / 'structures'
out.mkdir(parents=True, exist_ok=True)

def enc_name(n):
    b = n.encode('utf-8')
    return struct.pack('>H', len(b)) + b

def enc_string(name, v):
    b = v.encode('utf-8')
    return struct.pack('>B', 8) + enc_name(name) + struct.pack('>H', len(b)) + b

def enc_int(name, v):
    return struct.pack('>B', 3) + enc_name(name) + struct.pack('>i', v)

def enc_byte(name, v):
    return struct.pack('>B', 1) + enc_name(name) + struct.pack('>b', v)

def enc_compound(name, data):
    buf = bytearray()
    for k, v in data.items():
        if isinstance(v, dict):
            inner = bytearray()
            for kk, vv in v.items():
                if isinstance(vv, str):
                    inner += enc_str(kk, vv)
                elif isinstance(vv, bool):
                    inner += enc_byte(kk, 1 if vv else 0)
                elif isinstance(vv, int):
                    inner += enc_int(kk, vv)
            inner += struct.pack('>B', 0)
            buf += struct.pack('>B', 10) + enc_name(kk) + bytes(inner)
        elif isinstance(v, list):
            if not v:
                payload = struct.pack('>B', 0) + struct.pack('>i', 0)
                buf += struct.pack('>B', 9) + enc_name(kk) + payload
            first = v[0]
            if isinstance(first, dict):
                # list of compounds
                lbuf = bytearray()
                for item in v:
                    inner = bytearray()
                    for kkk, vvv in item.items():
                        if isinstance(vvv, str):
                            inner += enc_str(kkk, vvv)
                        elif isinstance(vvv, bool):
                            inner += enc_byte(kkk, 1 if vvv else 0)
                        elif isinstance(vvv, int):
                            inner += enc_int(kkk, vvv)
                    inner += struct.pack('>B', 0)
                    lbuf += struct.pack('>B', 10) + enc_name(kkk) + bytes(inner)
                payload = struct.pack('>B', 9) + struct.pack('>i', len(v)) + bytes(lbuf)
                buf += struct.pack('>B', 9) + enc_name(kk) + payload
            elif isinstance(first, int):
                payload = struct.pack('>B', 11) + struct.pack('>i', len(v)) + ('i' * len(v)).join(struct.pack('>i', i) for i in v)
                buf += struct.pack('>B', 9) + enc_name(kk) + payload
            elif isinstance(first, str):
                buf += enc_str(kk, ''.join(struct.pack('>H', len(s.encode('utf-8'))) + s.encode('utf-8') for s in v))
                buf += struct.pack('>B', 9) + enc_name(kk) + payload
    buf += struct.pack('>B', 0)
    return struct.pack('>B', 10) + enc_name(name) + bytes(buf)

structures = {
    'redstone_line_16': {'size': [16,1,1], 'entities': [], 'blocks': [{'pos': [0,0,0], 'state': {'Name': 'minecraft:redstone_wire', 'Properties': {}}}]},
    'piston_obsidian': {'size': [3,1,1], 'entities': [], 'blocks': [{'pos': [0,0,0], 'state': {'Name': 'minecraft:sticky_piston', 'Properties': {'facing': 'east', 'extended': 'false'}}}, {'pos': [2,0,0], 'state': {'Name': 'minecraft:obsidian', 'Properties': {}}}]},
    'comparator_wrong_mode': {'size': [1,1,1], 'entities': [], 'blocks': [{'pos': [0,0,0], 'state': {'Name': 'minecraft:comparator', 'Properties': {'facing': 'east', 'mode': 'subtract', 'powered': 'false'}}}]},
    'torch_burnout': {'size': [2,1,1], 'entities': [], 'blocks': [{'pos': [0,0,0], 'state': {'Name': 'minecraft:redstone_torch', 'Properties': {'facing': 'west'}}}, {'pos': [1,0,0], 'state': {'Name': 'minecraft:redstone_wire', 'Properties': {}}}]},
    'redstone_multiplexer': {'size': [1,3,1], 'entities': [], 'blocks': [{'pos': [0,0,0], 'state': {'Name': 'minecraft:repeater', 'Properties': {'facing': 'south', 'delay': '1', 'locked': 'false', 'powered': 'true'}}}]},
    'double_piston_extender': {'size': [3,2,1], 'entities': [], 'blocks': [{'pos': [0,1,0], 'state': {'Name': 'minecraft:sticky_piston', 'Properties': {'facing': 'east', 'extended': 'false'}}}, {'pos': [2,0,0], 'state': {'Name': 'minecraft:sticky_piston', 'Properties': {'facing': 'west', 'extended': 'false'}}}]},
    't_flip_flop': {'size': [3,2,1], 'entities': [], 'blocks': [{'pos': [0,0,0], 'state': {'Name': 'minecraft:redstone_torch', 'Properties': {'facing': 'north'}}, {'pos': [1,0,0], 'state': {'Name': 'minecraft:repeater', 'Properties': {'facing': 'east', 'delay': '2', 'locked': 'false', 'powered': 'true'}}]},
    'hopper_clock': {'size': [2,1,1], 'entities': [], 'blocks': [{'pos': [0,0,0], 'state': {'Name': 'minecraft:hopper', 'Properties': {'facing': 'east'}}, {'pos': [1,0,0], 'state': {'Name': 'minecraft:hopper', 'Properties': {'facing': 'west'}}]},
    'binary_counter': {'size': [2,2,1], 'entities': [], 'blocks': [{'pos': [0,1,0], 'state': {'Name': 'minecraft:comparator', 'Properties': {'facing': 'east', 'mode': 'subtract', 'powered': 'false'}}, {'pos': [1,0,0], 'state': {'Name': 'minecraft:redstone_torch', 'Properties': {'facing': 'south'}}]},
    'redstone_multiplexer': {'size': [3,1,1], 'entities': [], 'blocks': [{'pos': [0,0,0], 'state': {'Name': 'minecraft:repeater', 'Properties': {'facing': 'north', 'delay': '1', 'locked': 'false', 'powered': 'true'}}, {'pos': [1,0,0], 'state': {'Name': 'minecraft:repeater', 'Properties': {'facing': 'east', 'delay': '1', 'locked': 'false', 'powered': 'false'}}, {'pos': [2,0,0], 'state': {'Name': 'minecraft:redstone_wire', 'Properties': {}}]},
    'vertical_signal_chain': {'size': [2,2,1], 'entities': [], 'blocks': [{'pos': [0,1,0], 'state': {'Name': 'minecraft:comparator', 'Properties': {'facing': 'east', 'mode': 'subtract', 'powered': 'false'}}, {'pos': [1,1,0], 'state': {'Name': 'minecraft:repeater', 'Properties': {'facing': 'east', 'delay': '1', 'locked': 'false', 'powered': 'true'}}, {'pos': [0,0,0], 'state': {'Name': 'minecraft:redstone_torch', 'Properties': {'facing': 'west'}}]},
    'alu_slice': {'size': [2,2,1], 'entities': [], 'blocks': [{'pos': [0,1,0], 'state': {'Name': 'minecraft:comparator', 'Properties': {'facing': 'east', 'mode': 'subtract', 'powered': 'false'}}, {'pos': [1,0,0], 'state': {'Name': 'minecraft:repeater', 'Properties': {'facing': 'south', 'delay': '1', 'locked': 'false', 'powered': 'true'}}, {'pos': [0,0,0], 'state': {'Name': 'minecraft:redstone_torch', 'Properties': {'facing': 'west'}}]},
}

for name, data in structures.items():
    raw = enc_compound(name, data)
    gz = gzip.compress(raw)
    p = out / f'{name}.nbt'
    p.write_bytes(gz)
    print(f'{p.name}: {len(gz)} bytes')

print('Done')
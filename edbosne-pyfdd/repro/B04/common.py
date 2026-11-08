"""Small fixture writer and JSON reporting, shared only by the executions under test."""
import json
import math
import os
import struct
import sys
from pathlib import Path
import numpy as np


def record(payload):
    result = bytearray()
    while len(payload) > 128:
        result.extend(bytes([129]) + payload[:128] + bytes([129]))
        payload = payload[128:]
    return bytes(result) + bytes([len(payload)]) + payload + bytes([len(payload)])


def library_path(folder):
    """5x5 positive linear yield on the integer angular coordinates -2..2."""
    rows = [[10.0 + x + 2*y for x in range(-2, 3)] for y in range(-2, 3)]
    header = struct.pack('<hh8f', 5, 5, 0, 0, 1, 1, -2, -2, 0, 0)
    site = struct.pack('<h50s3f', 1, b'positive linear yield', 1, 0, 0)
    flat = [v for row in rows for v in row]
    path = folder / 'tiny.2dl'
    path.write_bytes(b'K' + record(header) + record(site) + record(struct.pack('<25f', *flat)) + bytes([130]))
    return str(path)


def work():
    p = Path(os.environ['CASE_WORK']) / sys.argv[1]
    p.mkdir(exist_ok=True)
    return p


def matrix(value):
    return np.ma.array(value).tolist(fill_value=None)


def agrees(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(agrees(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(agrees(x, y) for x, y in zip(a, b))
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-10)
    return a == b


def finish(actual):
    expected = json.loads((Path(sys.argv[0]).parent / 'correct-output.json').read_text())
    print(json.dumps(actual, indent=2, allow_nan=False))
    assert agrees(actual['normal'], expected['normal']), 'normal input changed'
    if sys.argv[1] == 'before':
        assert not agrees(actual, expected), 'bug did not reproduce'
    else:
        assert agrees(actual, expected), 'patched result disagrees with independent reference'

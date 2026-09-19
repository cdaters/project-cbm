#!/usr/bin/env python3
"""Summarize only bounded numeric VICE telemetry; never copy surrounding private log text."""
import argparse
import json
import math
from pathlib import Path
import re

PATTERN = re.compile(r'CBM_PERFORMANCE sample=(\d+) seconds=([0-9.]+) speed_percent=([0-9.]+) emulated_fps=([0-9.]+) warp=([01])$')


def summarize(text, first, last):
    if not 1 <= first <= last <= 120:
        raise ValueError('sample range must be within 1..120')
    rows = []
    for line in text.splitlines():
        match = PATTERN.search(line)
        if not match:
            if 'CBM_PERFORMANCE' in line:
                raise ValueError('malformed performance record')
            continue
        number = int(match[1])
        if first <= number <= last:
            seconds, speed, fps = map(float, match.group(2, 3, 4))
            if not all(math.isfinite(x) and x >= 0 for x in (seconds, speed, fps)) or seconds < 5 or seconds > 300:
                raise ValueError('invalid measurement')
            rows.append({'sample': number, 'seconds': seconds, 'speed_percent': speed,
                         'emulated_fps': fps, 'warp': int(match[5])})
    complete = [r['sample'] for r in rows] == list(range(first, last+1))
    elapsed = sum(r['seconds'] for r in rows)
    mean = sum(r['seconds']*r['speed_percent'] for r in rows)/elapsed if elapsed else None
    minimum = min((r['speed_percent'] for r in rows), default=None)
    enough = complete and len(rows) >= 12 and elapsed >= 60
    passed = enough and not any(r['warp'] for r in rows) and 98 <= mean <= 102 and minimum >= 95
    return {'format': 'project-cbm.vice-performance-summary', 'schema_version': 1,
            'selected_samples': [first, last], 'complete': complete, 'sample_count': len(rows),
            'seconds': elapsed, 'weighted_speed_percent': mean, 'minimum_speed_percent': minimum,
            'metric_gate': 'PASS' if passed else ('FAIL' if enough else 'INSUFFICIENT'),
            'physical_qualification': 'NOT ESTABLISHED by this parser; requires exact image/model, steady workload selection and owner audio/visual/lifecycle observations',
            'samples': rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('log', type=Path)
    parser.add_argument('--first-sample', type=int, required=True)
    parser.add_argument('--last-sample', type=int, required=True)
    args = parser.parse_args()
    if args.log.stat().st_size > 131072:
        raise ValueError('expected bounded engineering log')
    report = summarize(args.log.read_text(errors='replace'), args.first_sample, args.last_sample)
    print(json.dumps(report, indent=2))
    return 0 if report['metric_gate'] == 'PASS' else 2


if __name__ == '__main__':
    raise SystemExit(main())

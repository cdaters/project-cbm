#!/usr/bin/env python3
"""Bounded native comparison with original generated C64 exercise and validated audio.

Use a NEW directory on the approved external-backed native Linux filesystem.
These CPU ratios are diagnostic; they never qualify a Raspberry Pi or KMS display.
No owner media, real user configuration, credentials or network access is used.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import time
import wave


def exercise():
    """Original three-voice/filter plus screen/CPU write loop, BASIC SYS entry."""
    code = bytearray([0x78])  # SEI: exercise is independent of Kernal IRQ work.
    registers = [(0xd418, 31), (0xd417, 0xf7), (0xd416, 80), (0xd415, 7)]
    registers += [(0xd400 + 7*i + j, v) for i in range(3) for j, v in
                  [(0, 0x80+i*13), (1, 0x20+i*7), (2, 0), (3, 8),
                   (5, 9), (6, 0xf9), (4, 0x21)]]
    for address, value in registers:
        code += bytes([0xa9, value, 0x8d, address & 255, address >> 8])
    loop = 0x080d + len(code)
    # Sustained CPU/screen writes while the initialized SID voices play.
    # Writing SID registers on every CPU loop would dominate with an unusual
    # register-write stress case rather than ordinary continuous music output.
    code += bytes([0xee, 0, 4, 0xee, 1, 4, 0x4c, loop & 255, loop >> 8])
    return bytes([1, 8, 11, 8, 10, 0, 0x9e]) + b'2061' + bytes([0, 0, 0]) + code


def audio_check(path):
    with wave.open(str(path), 'rb') as w:
        frames, rate, channels = w.getnframes(), w.getframerate(), w.getnchannels()
        payload = w.readframes(frames)
    if not 19 <= frames/rate <= 22 or len(set(payload)) < 16:
        raise ValueError('missing, short or silent benchmark audio')
    return {'frames': frames, 'rate': rate, 'channels': channels,
            'seconds': frames/rate, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('package_root', type=Path)
    p.add_argument('output', type=Path)
    p.add_argument('--case', choices=['baseline', 'no-crt', 'interpolation', 'combined', 'x64', 'single-size', 'single-size-no-crt'], action='append')
    args = p.parse_args()
    if os.uname().sysname != 'Linux':
        raise ValueError('native Linux required')
    package = args.package_root.resolve(strict=True)
    args.output.mkdir(exist_ok=False)
    output = args.output.resolve()
    (output/'exercise.prg').write_bytes(exercise())
    cases = {'baseline': ('x64sc', []), 'no-crt': ('x64sc', ['-VICIIfilter', '0']),
             'interpolation': ('x64sc', ['-residsamp', '1']),
             'combined': ('x64sc', ['-VICIIfilter', '0', '-residsamp', '1']),
             'x64': ('x64', []), 'single-size': ('x64sc', ['+VICIIdsize']),
             'single-size-no-crt': ('x64sc', ['+VICIIdsize', '-VICIIfilter', '0'])}
    results = []
    for case in args.case or list(cases):
        engine, options = cases[case]
        for trial in range(2):
            dest = output/f'{case}-{trial}'
            dest.mkdir()
            command = [str(package/'usr/bin'/engine), '-default', '-directory',
                       str(package/'usr/share/vice'), '-sdl2backend', 'software',
                       '-sounddev', 'wav', '-soundarg', str(dest/'audio.wav'),
                       '+warp', '+autostart-warp', '-speed', '100', '-seed', '1',
                       '-limitcycles', '20000000', '-autostartprgmode', '1',
                       '-autostart', str(output/'exercise.prg'), '+logcolorize', '-logfile', '-', *options]
            env = dict(os.environ, HOME=str(dest), XDG_CONFIG_HOME=str(dest),
                       XDG_STATE_HOME=str(dest), TERM='linux', SDL_VIDEODRIVER='dummy',
                       SDL_AUDIODRIVER='dummy', CBM_PRESENTATION_DIAGNOSTICS='1')
            before = resource.getrusage(resource.RUSAGE_CHILDREN)
            start = time.monotonic()
            with (dest/'vice.log').open('w') as log:
                run = subprocess.run(command, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=90)
            elapsed = time.monotonic()-start
            after = resource.getrusage(resource.RUSAGE_CHILDREN)
            log = (dest/'vice.log').read_text()
            if run.returncode != 1 or 'cycle limit reached' not in log or 'AUTOSTART: Done.' not in log:
                raise ValueError('benchmark did not complete the cycle budget and autostart')
            audio = audio_check(dest/'audio.wav')
            row = dict(case=case, trial=trial, engine=engine, cpu_seconds=after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime,
                       wall_seconds=elapsed, audio=audio,
                       executable_sha256=hashlib.sha256((package/'usr/bin'/engine).read_bytes()).hexdigest())
            results.append(row)
            (output/'results.json').write_text(json.dumps(results, indent=2)+'\n')
            print(json.dumps(row), flush=True)


if __name__ == '__main__':
    main()

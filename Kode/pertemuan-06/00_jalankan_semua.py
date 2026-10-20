"""Jalankan semua demo, simpan keluaran, dan berhenti bila pemeriksaan gagal."""
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
HASIL = ROOT/'Hasil'/'pertemuan-06'
HASIL.mkdir(parents=True, exist_ok=True)
for p in sorted(HERE.glob('[0-9][0-9]_*.py')):
    if p.name.startswith('00_'):
        continue
    r = subprocess.run([sys.executable, str(p)], capture_output=True, text=True)
    (HASIL/(p.stem+'.txt')).write_text(r.stdout+r.stderr, encoding='utf-8')
    if r.returncode:
        print(r.stdout+r.stderr)
        raise SystemExit('Program gagal: '+p.name)
    print('Berhasil:', p.name)
print('Seluruh demo dan verifikasi pertemuan 06 selesai.')

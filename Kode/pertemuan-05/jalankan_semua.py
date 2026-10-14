"""Jalankan semua demo, simpan keluarannya, dan hentikan jika pemeriksaan gagal."""
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
HASIL = ROOT / "Hasil" / "pertemuan-05"
HASIL.mkdir(parents=True, exist_ok=True)
for p in sorted(HERE.glob("[0-9][0-9]_*.py")):
    r = subprocess.run([sys.executable, str(p)], capture_output=True, text=True)
    (HASIL/(p.stem+".txt")).write_text(r.stdout+r.stderr, encoding="utf-8")
    if r.returncode:
        print(r.stdout+r.stderr)
        raise SystemExit(f"Program gagal: {p.name}")
    print(f"Berhasil: {p.name}")
print("Seluruh demo dan pemeriksaan selesai.")

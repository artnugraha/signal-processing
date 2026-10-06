"""Jalankan seluruh demo dan buat ulang PNG/SVG tanpa ketergantungan lokasi kerja."""
from pathlib import Path
import subprocess
import sys
root=Path(__file__).resolve().parent
for path in sorted(root.glob('[0-9][0-9]_*.py')):
    if path.name != Path(__file__).name:
        print('Menjalankan',path.name,flush=True)
        subprocess.run([sys.executable,str(path)],check=True)

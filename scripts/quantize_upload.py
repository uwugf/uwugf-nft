from PIL import Image
from pathlib import Path
import sys
src=Path('images'); dst=Path('output/upload/images'); dst.mkdir(parents=True, exist_ok=True)
files=sorted(src.glob('*.png'), key=lambda p: int(p.stem) if p.stem.isdigit() else 0)
files=[f for f in files if f.stem.isdigit()]
tot=0
for i,f in enumerate(files,1):
    out=dst/f.name
    if not out.exists():
        im=Image.open(f).convert('RGB')
        im.quantize(colors=256, method=Image.MEDIANCUT).save(out, optimize=True)
    tot+=out.stat().st_size
    if i%500==0: print(f"  {i}/{len(files)}  {tot/1073741824:.2f} GB", flush=True)
print(f"done: {len(files)} files, {tot/1073741824:.2f} GB")

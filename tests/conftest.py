import sys, os
from pathlib import Path

current = Path(os.path.abspath(__file__)).parent.parent
src_dir = current / "src"
sys.path.insert(0, str(src_dir))
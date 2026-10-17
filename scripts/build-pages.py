"""Stage only the public homepage, explorers and licence for GitHub Pages."""
from pathlib import Path
import shutil

root = Path(__file__).resolve().parents[1]
destination = root / 'dist'
destination.mkdir(exist_ok=True)
for name in ('index.html', 'style.css'):
    shutil.copyfile(root / 'web' / name, destination / name)
for count in ('three', 'four', 'five'):
    name = f'{count}-round-schedule-explorer.html'
    shutil.copyfile(root / 'solutions' / name, destination / name)
shutil.copyfile(root / 'LICENSE', destination / 'LICENSE.txt')
(destination / '.nojekyll').touch()
expected = {'index.html', 'style.css', 'LICENSE.txt', '.nojekyll',
            *(f'{count}-round-schedule-explorer.html' for count in ('three', 'four', 'five'))}
assert {p.name for p in destination.iterdir()} == expected, 'Unexpected files in dist; review before publishing'
print(f'Staged {len(expected)} public files in {destination}')

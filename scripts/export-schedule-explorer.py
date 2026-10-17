"""Export the visualization fragment, forwarding URL roster names to its frame."""
import argparse
from pathlib import Path
import subprocess
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('source', type=Path)
parser.add_argument('destination', type=Path)
parser.add_argument('--renderer', type=Path, required=True)
parser.add_argument('--round-count', type=int, choices=(3, 4, 5), default=4)
args = parser.parse_args()
subprocess.run([sys.executable, str(args.renderer), str(args.source),
                str(args.destination), '--force'], check=True)
html = args.destination.read_text()
marker = '  const initialGlobals = {\n    widgetState: state,'
assert html.count(marker) == 1, 'Standalone shell changed; check URL integration'
roster = Path(__file__).with_name('explorer-url-roster.js').read_text()
html = html.replace(marker, roster + f'\n  state = explorerUrlRoster(state, globalThis.location.search, {args.round_count});\n' + marker)
args.destination.write_text(html)

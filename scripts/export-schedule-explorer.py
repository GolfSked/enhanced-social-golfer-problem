"""Export the visualization fragment, forwarding URL roster names to its frame."""
import argparse
from html import escape
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
# The renderer forwards frame links over a MessageChannel. Opening a new tab
# after that asynchronous hop is blocked by Safari. Keep the HTTPS validation,
# but navigate this page instead; the frame already requires a user gesture.
popup = '''      if (globalThis.navigator.userActivation?.isActive === true) {
        const anchor = document.createElement("a");
        anchor.href = href;
        anchor.rel = "noopener noreferrer";
        anchor.target = "_blank";
        document.body.appendChild(anchor);
        anchor.click();
        anchor.remove();
      }'''
assert html.count(popup) == 1, 'Standalone link handling changed; review navigation'
html = html.replace(popup, '      globalThis.location.assign(href);')
marker = '  const initialGlobals = {\n    widgetState: state,'
assert html.count(marker) == 1, 'Standalone shell changed; check URL integration'
roster = Path(__file__).with_name('explorer-url-roster.js').read_text()
html = html.replace(marker, roster + f'\n  state = explorerUrlRoster(state, globalThis.location.search, {args.round_count});\n' + marker)
theme = (Path(__file__).resolve().parents[1] / 'web' / 'explorer-theme.css').read_text()
version = (Path(__file__).resolve().parents[1] / 'web' / 'version.txt').read_text().strip()
assert version and all(c.isalnum() or c in '.-' for c in version)
html = html.replace('__EXPLORER_VERSION__', version)
version_meta = f'<meta name="application-version" content="{version}">'
html = html.replace('&lt;/head&gt;', escape(version_meta) + '\n&lt;/head&gt;', 1)
html = html.replace('</head>', version_meta + '\n</head>', 1)
theme_style = '<style id="golf-explorer-theme">' + theme + '</style>'
# srcdoc is escaped in the outer page. Embed the same skin inside and outside
# the frame so there are no stylesheet requests and standalone downloads work.
assert html.count('&lt;/head&gt;') == 1
html = html.replace('&lt;/head&gt;', escape(theme_style) + '\n&lt;/head&gt;', 1)
html = html.replace('</head>', theme_style + '\n</head>', 1)
args.destination.write_text(html)

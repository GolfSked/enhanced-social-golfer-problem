# Public schedule explorer site

The GitHub Pages deployment publishes only `dist/`, staged by:

```sh
node tests/check_explorer_url.cjs
python3 scripts/build-pages.py
python3 -m http.server 8765 --directory dist
```

The homepage is `web/index.html`; the three standalone exports remain in
`solutions/`. Editable visualization fragments are retained in
`web/explorer-sources/`. The export helper accepts a renderer path supplied by
the Codex visualization skill, and `--round-count 3`, `4` or `5`.

`web/explorer-theme.css` is the shared palette for the homepage and explorer
exports. Re-export the three explorers after changing it; the homepage loads
the same file directly. `web/version.txt` supplies the visible release number
and the explorers' `application-version` metadata.

`.github/workflows/pages.yml` tests, stages and publishes changes on `main`.
In GitHub Settings → Pages, select **GitHub Actions** as the build source.
The expected project URL is:
`https://golfsked.github.io/enhanced-social-golfer-problem/`.

## Analytics

No visitor analytics, advertising or tracking pixels are installed. The
homepage has no JavaScript or third-party assets. Explorer selections are
stored locally by the standalone wrapper; the explorers do not submit player
names or round settings to an application server. URLs containing names can
appear in browser history, recipient links and hosting logs. GitHub Pages
records access logs for security. The exported explorer UI includes optional
CDN-hosted icon/tooltip helpers from its original visualization runtime.

Repository clone counts under `analytics/` measure source-code downloads;
they are separate from website visits. If useful later, add aggregate site
analytics as a deliberate follow-up rather than sending player or course
parameters to a tracking service.

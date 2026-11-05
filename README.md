# demo

Static GitHub Pages site that logs the top macOS CPU process every ~2 minutes (`cpu-log.json` + `scripts/append_cpu_sample.py`).

## Publish

1. Push to `main`.
2. On GitHub, open **Settings > Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**, then `main` and `/ (root)`.
4. After a minute the site is live at https://finespine.github.io/demo/.

## Preview locally

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000.

# Names Site

A tiny static website (plain HTML, CSS, and JavaScript) with two pages:

- **`index.html`** — the display page. Shows the title and every name that's been added.
- **`input.html`** — the input page. Set a title, type a name, and click **Add Name**. Names you add here show up on the display page immediately.

No backend or build step — data is kept in the browser's `localStorage`, shared between the two pages.

## Running locally

Just open `index.html` or `input.html` in a browser, or serve the folder with any static file server, e.g.:

```bash
python3 -m http.server
```

then visit `http://localhost:8000`.

## Hosting on GitHub Pages

This repo includes a GitHub Actions workflow (`.github/workflows/deploy.yml`) that deploys the site to GitHub Pages automatically on every push to `main`.

To turn it on (one-time, in the repo's GitHub settings):

1. Go to **Settings → Pages**.
2. Under **Build and deployment → Source**, choose **GitHub Actions**.
3. Merge/push to `main` — the workflow will publish the site and the Pages URL will show up in the **Actions** tab and in Settings → Pages.

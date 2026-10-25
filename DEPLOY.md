# Deploying tradelab as a live dashboard

Everything needed is in this folder. Pick one of the two layouts.

## A. Its own repository (recommended, zero settings clicks)

1. On GitHub create an empty repository, e.g. `rgprince84-prog/tradelab`
   (public — GitHub Pages on a private repository needs a paid plan).
2. Push this folder as `main`:

       cd tradelab
       git init -b main
       git add -A
       git commit -m "tradelab: research pipeline + live dashboard"
       git remote add origin https://github.com/rgprince84-prog/tradelab.git
       git push -u origin main

3. Seed the data so the page is populated immediately (optional; otherwise the first
   scheduled run does it, including the deep backtests):

       python -m tradelab dashboard --dest site/data        # or use the site/data/ shipped in the bundle
       cd site && cp -r data /tmp/tl-data && cd /tmp/tl-data && git init -b tradelab-data && git add -A \
         && git commit -m "tradelab data seed" && git push --force https://github.com/rgprince84-prog/tradelab.git HEAD:tradelab-data

4. Actions → **tradelab** → *Run workflow* (tick **backtests** if you skipped step 3).
   The first run enables GitHub Pages and deploys. The page is then at

       https://rgprince84-prog.github.io/tradelab/

   and refreshes hourly at :12 UTC on weekdays, with the deep backtests every Sunday.

## B. Inside the existing user-site repository (rgprince84-prog.github.io)

GitHub Pages serves that repository's default branch, so the page must live there, but
nothing else on `main` is touched and the workflow never commits to `main`.

1. Push this folder as an orphan branch `tradelab`:

       cd tradelab && git init -b tradelab && git add -A && git commit -m "tradelab" \
         && git push https://github.com/rgprince84-prog/rgprince84-prog.github.io.git tradelab

2. Push the data seed (shipped in `site/data/`) as orphan branch `tradelab-data`
   (same commands as A.3, with this repository's URL).
3. On `main`, add exactly two files and push:
   - `.github/workflows/tradelab.yml`  ← copy of the file in this folder
   - `tradelab/index.html`             ← `deploy/user-site/tradelab/index.html` (its meta tag already
     points at the raw URL of the `tradelab-data` branch)
4. Actions → **tradelab** → *Run workflow*. The page is at https://rgprince84-prog.github.io/tradelab/.

Caveat: the "staging deploy" commits in that repository mirror the PropertyFlow website tree
and delete files that are not in the source. Whatever produces them must keep
`.github/workflows/` and `tradelab/` — otherwise the schedule and the page disappear.

## What the workflow does each run

- checks out the code, restores `.cache/` (Actions cache, one save per day),
- restores the previous `site/data/` from the `tradelab-data` branch,
- `python -m tradelab pipeline --tf 1h` and `--tf 4h`,
- on Sundays (or on demand) the deep backtests: 1d since 2016 and 1h since 2024, all with
  Monte Carlo,
- `python -m tradelab dashboard --dest site/data`,
- force-pushes `site/data/` as a single orphan commit to `tradelab-data` (so that branch
  never grows), and in layout A deploys `site/` to GitHub Pages.

Yahoo Finance rate-limits shared runners now and then; the data layer then keeps the
cached bars and the run still completes. Scheduled workflows are disabled by GitHub after
60 days without any commit to the repository; the hourly bot commits keep it alive.

## Local preview

    pip install -r requirements.txt
    python -m tradelab pipeline --tf 1h            # or any backtest
    python -m tradelab dashboard --dest site/data
    python -m http.server 8000 --directory site    # http://localhost:8000/

# Rail Express — Documentation

Source for the Rail Express Unity template's documentation site, built with
[MkDocs](https://www.mkdocs.org/) and ready to publish on [Read the Docs](https://readthedocs.org/).

## Building locally

```bash
pip install -r requirements.txt
mkdocs serve
```

Then open <http://127.0.0.1:8000>.

## Publishing on Read the Docs

This repo already includes `.readthedocs.yaml`. To go live:

1. Sign in to [readthedocs.org](https://readthedocs.org/) and import this repository.
2. Read the Docs will pick up `.readthedocs.yaml` automatically on the next build — no further
   configuration needed.
3. Once your project has a live URL, update `DocsUrl` in
   `Assets/Rail Express/Scripts/Editor/AboutWindow.cs` in the main Rail Express project so the
   in-editor About window's **Documentation** button points at it.

## Structure

```
docs/
  index.md                  Home
  overview.md                Project structure, scenes, managers, Editor Tools menu
  level-editor.md            Building levels
  rails-and-trains.md        Rail types, intersections, train physics
  gameplay-systems.md        Passengers, coins, wagons, victory/defeat, restart flow
  environment-and-colors.md  Fillers, Sea/Rocks, color presets
  ui.md                      UI screens
  monetization.md            Ad providers & IAP
  save-system.md             SaveController API and the two settings assets
  faq.md
mkdocs.yml                   Site nav & theme
.readthedocs.yaml            Read the Docs build config
requirements.txt             Python deps for the RTD build
```

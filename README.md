
This repository contains notebook templates, code snippets, and banners to accompany the Callysto curriculum-notebooks repository.

## Notebook Templates

Templates contributed here are available in a Jupyter notebook through [`nbtemplate`](https://github.com/callysto/nbplus/tree/master/nbtemplate), one of our notebook extensions. With `nbtemplate` installed, click on the <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M96 348h320v36H96zM96 128h320v36H96zM96 200.7h320v35.6H96zM96 275.8h320v35.6H96z"/></svg> icon. Any templates found in `templateConfig.json` will be displayed, and choosing a notebook template copies its cells into the current notebook.

Contributions should be added to the `/templates` directory. Then, create an entry in `templateConfig.json` to point to the templates source url. Each entry must be a JSON object with an `id` and `url` key, at minimum.

e.g.

```json
{
    "id": "A sample JSON object",
    "url": "https://raw.githubusercontent.com/</path/to/template.ipynb>",
    "someKey": "someValue"
}
```

## Code Snippets

We are aggregating useful snippets, "shorts," that provide minimal and self-contained examples of the many libraries, tools, and methods available to us in Jupyter. These snippets are available through [`nbtemplate`](https://github.com/callysto/nbplus/tree/master/nbtemplate). With `nbtemplate` installed, click on "Blocks" in the menubar to see a dropdown list of shorts. Selecting a short will copies it cells into the current notebook, and executes these cells.

Contributions should be added to the `/blocks` directory. Then, create an entry in `blockConfig.json` to point to the templates source url. Each entry must be a JSON object with an `id` and `url` key, at minimum.

e.g.

```json
{
    "id": "a_short_id",
    "title": "A description that appears as a tooltip",
    "text": "The Short Name",
    "url": "https://raw.githubusercontent.com/</path/to/short.ipynb>",
    "submenu": [
      { ... },
      { ... }
    ]
}
```

## Banners

We have developed a Jupyter magics implementation of the Callysto banners. In Jupyter, within a code cell (Python 3):

```
!git clone https://github.com/callysto/notebook-templates.git
!cd notebook-templates; cp -f banner_magics.py ~/.ipython/profile_default/startup
```

Then, restart the kernel. Use `%top_banner` and `%bottom_banner` in separate code cells to insert the top and bottom banners, respectively.

These magics will be initialized upon kernel startup in any notebook.

## Contributing

Commit directly to `master`, or from your developer branch to `master`. If you want your code to be reviewed before committing, open a pull request with the word "review" in the pull request title.

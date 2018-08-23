# Notebook Templates

Notebook templates meant to accompany the Callysto curriculum-notebooks repo.

## Banners

We've developed Jupyter magics implementation of the Callysto banners. In Jupyter, within a code cell (Python 3):

```
!git clone https://github.com/callysto/notebook-templates.git
!cd notebook-templates; cp banner_magics.py ~/.ipython/profile_default/startup
```

Then, restart the kernel. Use `%top_banner` and `%bottom_banner` in separate code cells to insert the top and bottom banners, respectively.

## Contributing

Commit directly to master, or from your developer branch to master. If you want your code to be reviewed before committing open a pull request with the word "review" in the pull request title.

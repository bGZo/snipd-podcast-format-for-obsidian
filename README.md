# Snipd export format

> [!NOTE]
> This is a very early version, if something help, I would maintain it.


Snipd export all snips to a singal file by default. And they cannot be queried by obsidian. That's okey when you just only have severals snips. But after two years usage, I have more than 3,000 snips on platform.

Export 3000 snips, format it manually, then delete them one by one?

Okey, sounds like a hell.

I make this scripts for separate them to them files, then you could copy them to obsidian.


## Quick Start

`poetry` is required. If you do not install, please following:

```shell
# install pipx on ubuntu
sudo apt install pipx

# install poetry
pipx install poetry
```

Then following should works. Enjoy.

```shell
poetry install 
poetry run snipd snipd-export.md -o /path/you/want/export
```


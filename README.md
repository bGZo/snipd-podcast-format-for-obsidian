# Snipd export format

> [!NOTE]
> This is a very early version.

## Why

Snipd could export all snips, but only with a signal file by default. They're kind of meaningless with obsidian. 

I guess that's ok when you just only have lot of snips. But after two years usage, I have more than 3,000 snips on platform. If you just format it manually, sounds like a hell, right?

So this script is used to separate them to them files, then you could import to obsidian easily. Finally, you could delete account for snipd, and restart your workflow again.


## How to use it?

```shell
pipx install snipd_export_parser
```

Run the command to get start:

```shell
snipd --help
```

## Contribute it

If you want to contribute, please feel free to open an issue or pull request.

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


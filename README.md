# Ba-Nanos

## Intro

Ba-Nanos is an application that applies a Neural Style Transfer using PyTorch on
user provided images. Anyone can use the application by visiting [our site](#).

## Team Members

[Cristian Abad](https://github.com/achrrr)

[Savannah Chhann](https://github.com/shirokuma-cafe)

[Brendan Costello](https://github.com/BrendanCostello)

[Methila Deb](https://github.com/methiladeb)

## Technologies Used for This Project

- Flask
- Heroku
- MongoDB
- Node.js
- Pytorch
- Tailwind CSS

## Demo

Coming Soon...

## Dependencies

This process is only tested on Python 3.10. To install this version manually on
macOS using [Homebrew](https://brew.sh):

```shell
brew install python@3.10
```

You'll want to create a virtual environment first:

```shell
python3 -m venv .venv
```

Then, you must activate the virtual environment:

Windows (`cmd.exe`):

```cmd
.venv\Scripts\activate.bat
```

Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

POSIX (macOS/Linux `bash`/`zsh`):

```shell
source .venv/bin/activate
```

(If you have previously set up a virtual environment with another Python
version, you may want to remove it with `rm -rf .venv`, then follow steps to
create a new virtual environment linked against Python 3.10.)

Then install the required modules:

```shell
pip install -r requirements.txt
```

To update the list of required packages after installing a new one:

```shell
pip freeze > requirements.txt
```

To activate the backend:

First, activate the virtual environment using the steps above. Then, copy the
`.env.sample` file to `.env` and modify it with the information it requires.
Finally, this command will start the Flask server:

```bash
flask --app backend.main run
```

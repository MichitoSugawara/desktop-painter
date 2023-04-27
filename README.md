# Desktop Painter

This application is a paint application for Windows, created with Python. It allows you to draw on the screen with a pen without changing the active window. The Ctrl key can be used for operations, preventing interference with other applications and enabling smooth and seamless painting on the screen.
![Alt Text](https://i.gyazo.com/379ced97ada3ae442fbcd4cb2d4d79d0.gif)

## Features
This interface can be operated using the Ctrl key.
- 筆(Toggle pen mode): In this mode, pressing and holding the Ctrl key allows you to draw on the screen.
- 色(Change color): You can change the color of the pen.
- 消(Clear): You can clear all the drawings.
- …(Switch direction): Press and hold the Ctrl key, move the mouse to the desired location, and release the key to move the interface to that location.
- ×(Quit this app)

## System Requirements

- Windows 7or later (I don't know)
- Python 3.7or later (I don't know)

## Quick setup dev environment

1. Run ``$ cp .env.example .env`` to set environment variables
2. Run `$ pip install --user pipenv` to install pipenv (If you already installed it, you can skip this)
3. Run ``$ pipenv install`` to resolve project dependencies
4. Run ``$ pipenv run dev`` to execute this app
5. If you would like to build EXE file, you can run ``$ pipenv run build`` as you can see in Pipfile.

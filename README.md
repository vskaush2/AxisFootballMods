# Axis Football 2021 NFL Roster Mods
We use Python to change the default football rosters in Axis Football 2021 into custom Madden NFL 22 rosters. We update the baseline mods from this [link](https://netorg4493362-my.sharepoint.com/:f:/g/personal/info_vault-interactive_com/ElWUoN0vbwVIrw1AxY5L7jMB8vDlezT2eXz4OURwQvBPmA?e=roW0JC): 

## Downloading Requirements
- Download [PyCharm (free edition)](https://www.jetbrains.com/pycharm/).
- Download [Steam] (https://store.steampowered.com/).
- Purchase and download `Axis Football 2021` on Steam.
- Download [Python 3.10](https://www.python.org/downloads/).

## Importing Project
- Open PyCharm and select `Get from VCS`.
- Enter this project's .git link.
- Specify the download location to be the `PyCharmProjects` folder.

## Installing Project Dependencies Automatically
- You may be prompted by PyCharm to install a Virtual Environment based on the `requirements.txt` file.
- Follow the onscreen instructions to do so.
- Make sure you specify your installed Python 3 for creating the Virtual Environment.

## Installing Project Dependencies Manually
- Open PyCharm Settings and locate the `Project: AxisFootballMods` pane.
- Click on `Project Interpreter`.
- Add a new `VirtualEnv` environment with your system Python.
- Restart PyCharm and open its local`Terminal` located in the bottom of the PyCharm window.
- Type the command `pip3 install -r requirements.txt` to install project dependencies.

## Jupyter Server Instructions
  - Open the local `Terminal` on PyCharm.
  - Type the command `jupyter notebook` to open up a new Jupyter Server.
  - Click on the `AxisFootballModsDemo.ipynb` file to open the notebook.
  - Run each code cell using the toolbar on top of the window.

## Changing Game Files Instructions
- On Steam, right click on `Axis Football 2021` in the left window pane.
- Click on `Manage > Browse local game files`.
- Overwrite the game's current `Mods` folder with the `Mods` folder inside this project's directory.
- Run the game in Steam.
- In the game, click on `Settings > Data` and turn on `Use Mods` 
- Restart and run the game !

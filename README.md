# Axis Football 2020 NFL Roster Mods
We use Python to change the default football rosters in Axis Football 2020 into custom Madden NFL 22 rosters. We update the baseline mods from the link: https://steamcommunity.com/linkfilter/?url=https://netorg4493362-my.sharepoint.com/:f:/g/personal/info_vault-interactive_com/EjETTB_vcK5Ht4wyQSvQOZEB3neA96YRnrxtNL3YuCQQ-Q?e=Vbvxc9

## Downloading Requirements
- Download PyCharm (free edition) from https://www.jetbrains.com/pycharm/.
- Download Steam from https://store.steampowered.com/.
- Purchase and download `Axis Football 2020` on Steam.
- Download the latest version of Python 3 from https://www.python.org/downloads/.

## Importing Project
- Open PyCharm and select `Get from VCS`.
- Enter this project's .git link.
- Specify the download location to be the `PyCharmProjects` folder.

## Installing Project Dependencies
- Open PyCharm Settings and locate the `Project: AxisFootballMods` pane.
- Click on `Project Interpreter`.
- Add a new `VirtualEnv` environment with your system Python.
- Restart PyCharm and open its local`Terminal`.
- Type the command `pip3 install -r requirements.txt` to install project dependencies.


## Jupyter Server Instructions
  - Open the local `Terminal` on PyCharm.
  - Enter the command `jupyter notebook` to open up a new Jupyter Server.
  - Click on the `AxisFootballModsDemo.ipynb` file to open the notebook.
  - Run each code cell using the toolbar on top of the window.

## Changing Game Files Instructions
- On Steam, right click on `Axis Football 2020` in the left window pane.
- Click on `Manage > Browse local game files`.
- Overwrite the game's current `Mods` folder with the `Mods` folder inside this project's directory.
- Run the game in Steam !


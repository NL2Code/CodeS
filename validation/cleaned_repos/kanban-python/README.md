# kanban-python

> A Terminal Kanban Application written in Python to boost your productivity

## Introduction
Welcome to **kanban-python**, your Terminal Kanban-Board Manager.

The [clikan] Kanban App inspired me to write
my own Terminal Kanban Application since I preferred a more simple and guided workflow.

**kanban-python** also comes with more features, like custom column creation,
automatic scanning and customizable config file to support you being productive.

This package was developed with [pyscaffold], which provides awesome project templates
and takes over much of the boilerplate for python packaging.
It was a great help for developing my first package and I can highly recommend it.

## Features
<details><summary>Colorful and Interactive</summary>

- kanban-python uses [rich] under the hood to process user input
and display nice looking kanban-boards to the terminal.
- Each task has a unique `ID` per board and also has an optional `Tag` and `Due Date` associated with it,
which are displayed alongside its `Title`

</details>


<details><summary>Following the XDG basedir convention</summary>

- kanban-python utilizes [platformdirs] `user_config_dir` to save the config file and `user_data_dir` for
the board specific task files. After creating your first board, you can use `kanban configure` to show the current settings table.
The config path in the table caption and the path for the task files can be found in the kanban_boards section.

</details>


<details><summary>Scanning of Files for automatic Task Creation</summary>

- kanban-python can scan files of defined types for specific patterns at start of line.
Check [Automatic Task Creation](#automatic-task-creation) for more Infos.

</details>


<details><summary>Customizable Configfile</summary>

- A `pykanban.ini` file gets created on first initialization in a `kanban-python` folder in your `user_config_dir`-Directory.
This can be edited manually or within the kanban-python application. It tracks the location for all your created boards. \
![configfile](https://raw.githubusercontent.com/Zaloog/kanban-python/main/images/image_config.PNG)
   * `Active_Board`: current board that is shown when using `kanban`-command
   * `Done_Limit`: If the amount of tasks exceed this number in the  <span style="color:green">Done</span> column,
   the first task of that column gets its status updated to <span style="color:gold">Archived</span> and is moved into that column. (default: `10`)
   * `Column_Min_Width`: Sets the minimum width of columns. (default: `40`)
   * `Show_Footer`: Shows the table footer with package name and version. (default: `True`)
   * `Files`: Space seperated filetypes to search for patterns to create tasks. (default: `.py .md`)
   * `Patterns`: Comma seperated patterns to search for start of line to create tasks. <br />(default: `# TODO,#TODO,# BUG`)

</details>


<details><summary>Task Storage File for each Board</summary>

- Each created board comes with its own name and `pykanban.json` file,
which stores all tasks for that board. The files are stored in board specific folders under `$USER_DATA_DIR/kanban-python/kanban_boards/<BOARDNAME>`.
When changing Boards you also get an overview over tasks in visible columns for each board and the most urgent or overdue task on that board.
![change_view](https://raw.githubusercontent.com/Zaloog/kanban-python/main/images/image_kanban_change.PNG)

</details>


<details><summary>Customizable Columns</summary>

- kanban-python comes with 5 pre-defined colored columns: [Ready, Doing, Done, Archived, Deleted]
More column can be added manually in the `pykanban.ini`, the visibility can be configured in the settings
with `kanban configure`.

</details>


<details><summary>Time Tracking of Task duration in Doing</summary>

- For each task it is tracked, how long it was in the
 <span style="color:yellow">Doing</span> column, based on the moments when you update the task status.
 The initial Task structure on creation looks as follows:
![task](https://raw.githubusercontent.com/Zaloog/kanban-python/main/images/image_task_example.PNG)

</details>


<details><summary>Report Creation for completed Tasks</summary>

- When you use [kanban report](#create-report) a github-like contribution map is displayed for the current year,
Also a markdown file is created with all tasks comleted based on the moment, when the tasks were moved to Done Column.
![task](https://raw.githubusercontent.com/Zaloog/kanban-python/main/images/image_kanban_report_document.PNG)

</details>

## Usage
After Installation of kanban-python, there are 5 commands available:

### Create new Boards
  ```bash
  kanban init
  ```
Is used to create a new kanban board i.e. it asks for a name and then creates a `pykanban.json` file with a Welcome Task.
On first use of any command, the `pykanban.ini` configfile and the `kanban-python` folder will be created automatically.

### Interact with Tasks/Boards
  ```bash
  kanban
  ```
This is your main command to interact with your boards and tasks. It also gives the option to show the current settings and adjust them.
Adjusting the settings can also be done directly by using the command `kanban configure`.

Use `Ctrl-C` or `Ctrl-D` to exit the application at any time. :warning: If you exit in the middle of creating/updating a task,
or changing settings, your progress wont be saved.

### Automatic Task Creation
  ```bash
  kanban scan
  ```
After executing this command, kanban-python scans your current Directory recursively for the defined filetypes and searches for lines that start with the pattern provided.

After confirmation to add the found tasks to table they will be added to the board. The alphanumeric Part of the Pattern will be used as tag.
The filepath were the task was found will be added as description of the task.

### Create Report
  ```bash
  kanban report
  ```
Goes over all your Boards and creates a single markdown file by checking the `Completion Dates` of your tasks.
Also shows a nice github-like contribution table for the current year.

### Change Settings
  ```bash
  kanban configure
  ```
To create a new custom Columns, you have to edit the `pykanban.ini` manually and add a new column name + visibility status
under the `settings.columns.visible` section. The other options are all customizable now via the new settings menu.
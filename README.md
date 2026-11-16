# County

> [!NOTE]
> Python is required to use the command with the provided command shims.  
> Instruction on how to build a standalone executable are available below.

Whenever I am writing some code for a project I sometimes wonder how many lines of code I have written.  
This project is a simple command line tool that counts the number of lines in a given file or directory.   
It can be useful for developers who want to keep track of their codebase size or for anyone who wants to analyze the size of their text files but I've just made it for fun :)  

Supports project directories with multiple file types and can be run recursively to count lines in subdirectories.  

## Windows command shim explained

`@` prevents the command from being echoed to the terminal.
`python` runs the Python interpreter.  
`%*` forwards all arguments to the `county.py` script.  
`%~dp0` expands to the drive letter and path of the batch file, allowing the script to be run from any directory.

## Run from any directory on Windows

The repository includes `county.cmd`, a Windows command shim that runs `county.py`.

1. Add this repository folder to your user PATH (this can also be done with the Windows GUI):

   ```powershell
   $countyPath = "C:\your\path\to\repo\folder"
   [Environment]::SetEnvironmentVariable(
       "Path",
       [Environment]::GetEnvironmentVariable("Path", "User") + ";$countyPath",
       "User"
   )
   ```

2. Open a new terminal.
3. Use the command from any directory:

   ```text
   county .\src
   county -r C:\path\to\project
   ```

You may need to or, at least, restart all open Powershell/CMD instances.
The `python` command must be available on PATH.  
If your Python installation uses the Python launcher instead, change `python` to `py` in `county.cmd`.

## Run from any directory on Linux or macOS

> [!IMPORTANT]  
> Not tested, I don't use Linux regularly for day-to-day development.  
> Please let me know if you encounter any issues.  

The repository includes `county`, an executable shell script that runs `county.py`.

1. Make the script executable:

   ```bash
   chmod +x county
   ```

2. Add this repository folder to your PATH for the current terminal:

   ```bash
   export PATH="/path/to/County:$PATH"
   ```

3. Make the PATH change permanent. Use the command for your shell:

   **Bash:**

   ```bash
   echo 'export PATH="/path/to/County:$PATH"' >> ~/.bashrc
   ```

   **Zsh (the default shell on modern macOS):**

   ```bash
   echo 'export PATH="/path/to/County:$PATH"' >> ~/.zshrc
   ```

4. Reload your shell configuration, or open a new terminal:

   ```bash
   source ~/.bashrc  # Bash
   source ~/.zshrc   # Zsh
   ```

5. Use the command from any directory:

   ```text
   county ./src
   county -r /path/to/project
   ```

The `python3` command must be available on PATH.

## Build a standalone executable

The executable bundles Python, so Python is only required on the machine that
builds it.

1. Install PyInstaller:

   ```bash
   python -m pip install pyinstaller
   ```

2. From the repository directory, build the executable:

   ```bash
   python -m PyInstaller --onefile --name county county.py
   ```

3. Locate the generated file:

   Generated file location:
   - Windows: `dist\county.exe`
   - Linux/macOS: `dist/county`

   On Linux/macOS, make the generated file executable before adding it to PATH:

   ```bash
   chmod +x dist/county
   ```

4. Add the generated file to a directory on the user's PATH:

   Move the executable to a directory on the user's PATH, or add the directory containing the executable to the user's PATH.

`county -r /path/to/project` is then available for use without installing Python.

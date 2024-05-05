# Pirated WordPress Cleanup Script

This Python script automates the process of cleaning up a pirated WordPress site by reinstalling a fresh version of WordPress along with essential plugins, and removing malicious .php files from the uploads directory.

## Features

- **Backup Creation**: Allows creating a backup of the WordPress directory before making changes.
- **Deletion of Unnecessary Files and Directories**: Deletes unnecessary files and directories, excluding essential WordPress files.
- **Reinstallation of WordPress**: Downloads the latest version of WordPress and reinstalls it in the specified directory, ensuring a clean and legitimate installation.
- **Fresh Plugin Installation**: Fetches URLs for essential plugins and installs them, ensuring the site has necessary functionality without compromise.
- **Removal of Malicious PHP Files**: Deletes malicious .php files found within the uploads directory, enhancing the security and integrity of the WordPress site.


## Requirements

- Python 3.x
- `curl` command-line tool
- `tar` command-line tool
- `unzip` command-line tool

## Usage

1. Clone the repository to your local machine:

```bash
git clone https://github.com/abidarm/clean-wordpress-site.git
```

2. Navigate to the cloned directory:

```bash
cd clean-wordpress-site
```

3. Execute the script providing the starting directory of your WordPress installation as an argument:

```bash
python script.py /path/to/your/wordpress
```

Replace /path/to/your/wordpress with the absolute path to your WordPress installation directory.

## Disclaimer

This script performs operations that could potentially modify or delete files and directories in your WordPress installation. Use it at your own risk.

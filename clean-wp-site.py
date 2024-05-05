import os
import sys
import subprocess

def create_backup(directory, script_directory):
    # Task: Create a backup of starting_directory
    backup_filename = os.path.basename(directory) + ".tar.gz"
    backup_path = os.path.join(script_directory, backup_filename)

    subprocess.run(f"tar -czf {backup_path} -C {script_directory} {os.path.basename(directory)}", shell=True, check=True)

    print(f"Backup created: {backup_path}")

def delete_files_and_directories(directory, script_file):
    # Task: Save plugin folders before deletion
    plugin_folders = set()

    for root, dirs, files in os.walk(directory, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            normalized_path = dir_path.replace(os.sep, "/")

            if normalized_path == script_file:
                continue  # Skip deletion of the script file itself

            relative_path = os.path.relpath(normalized_path, os.path.join(directory, "wp-content/plugins"))
            if "wp-content/plugins" in normalized_path and "/" not in relative_path and "." not in relative_path:
                plugin_folders.add(relative_path)

            if "wp-content/uploads" not in normalized_path and dir != "wp-config.php" and not os.listdir(normalized_path):
                os.rmdir(normalized_path)

        for file in files:
            file_path = os.path.join(root, file)
            normalized_path = file_path.replace(os.sep, "/")

            if normalized_path == script_file:
                continue  # Skip deletion of the script file itself

            if "wp-content/uploads" not in normalized_path and file != "wp-config.php":
                os.remove(normalized_path)

    return plugin_folders

def delete_php_files(directory):
    # Task: Delete files with .php extension inside wp-content/uploads
    deleted_php_files = []
    uploads_directory = os.path.join(directory, "wp-content/uploads")

    subprocess.run(f"find {uploads_directory} -type f -name '*.php' -exec sh -c 'echo \"{}\"; rm \"{}\"' \;", shell=True)

    return deleted_php_files

def download_and_extract_wordpress(url, extract_path):
    # Task: Download and extract WordPress
    try:
        subprocess.run(f"curl -sSL {url} | tar -xzf - -C {extract_path} --strip-components=1", shell=True, check=True)
        print("WordPress downloaded and extracted successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error: Unable to download or extract WordPress archive. {e}")
        sys.exit(1)

def list_direct_subfolders(directory, target_folder):
    # Helper function: List direct subfolders of a directory
    subfolders = [d for d in os.listdir(os.path.join(directory, target_folder)) if os.path.isdir(os.path.join(directory, target_folder, d))]
    return subfolders

def generate_plugin_urls(plugin_folders):
    # Task: Generate plugin URLs
    plugin_urls = set()
    for folder in plugin_folders:
        plugin_urls.add(f"https://downloads.wordpress.org/plugin/{folder}.latest-stable.zip")
    return plugin_urls

def create_plugins_directory(directory):
    # Task: Create "wp-content/plugins/" directory if not exists
    plugins_directory = os.path.join(directory, "wp-content/plugins")
    if not os.path.exists(plugins_directory):
        os.makedirs(plugins_directory)
        print("Created 'wp-content/plugins/' directory.")

def download_and_extract_plugins(plugin_urls, extract_path, plugin_folders):
    # Task: Download and extract plugins
    for url, plugin_name in zip(plugin_urls, plugin_folders):
        subprocess.run(f"curl -sSL {url} --output temp.zip", shell=True, check=True)
        subprocess.run(f"unzip -o temp.zip -d {extract_path} > /dev/null 2>&1", shell=True, check=True)
        subprocess.run("rm temp.zip", shell=True, check=True)
        print(f"Downloaded and extracted plugin: {plugin_name}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <starting_directory>")
        sys.exit(1)

    starting_directory = os.path.abspath(sys.argv[1])
    script_file = os.path.abspath(sys.argv[0])
    script_directory = os.path.dirname(script_file)

    # Create a backup of starting_directory
    # create_backup(starting_directory, script_directory)

    # Save plugin folders before deletion
    plugin_folders = delete_files_and_directories(starting_directory, script_file)

    # Delete files with .php extension inside wp-content/uploads
    deleted_php_files = delete_php_files(starting_directory)
    
    try:
        # Download and extract WordPress
        archive_url = "https://wordpress.org/latest.tar.gz"
        download_and_extract_wordpress(archive_url, starting_directory)

        # Generate plugin URLs
        plugin_urls = generate_plugin_urls(plugin_folders)

        # Create "wp-content/plugins/" directory if not exists
        create_plugins_directory(starting_directory)

        # Download and extract plugins
        download_and_extract_plugins(plugin_urls, os.path.join(starting_directory, "wp-content/plugins"), plugin_folders)

        print("\nPlugin download and extraction process completed successfully!")

        # Show plugin folders at the end
    except Exception as e:
        
        print(f"\nAn error occurred: {e}")
        print("\nPlugin folders under wp-content/plugins:")
        for folder in sorted(plugin_folders):
            print(folder)
        sys.exit(1)

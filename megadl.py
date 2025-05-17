import subprocess
import os
import shutil # To check if megaget is installed
import traceback

def is_tool_installed(name):
    """Check whether `name` is on PATH and marked as executable."""
    return shutil.which(name) is not None

def download_with_megacmd(mega_url, download_base_dir_name="megacmd_downloads"):
    """
    Downloads a file from a given Mega link using the 'mega-get' command-line tool.

    Args:
        mega_url (str): The full Mega link (e.g., https://mega.nz/file/...).
        download_base_dir_name (str): The name of the sub-directory within the chosen root
                                      (shared storage or Termux home) to download files into.
    """
    print(f"Attempting to download using MEGAcmd: {mega_url}")

    if not mega_url.startswith("https://mega.nz/"):
        print("Error: Invalid Mega link format. It should start with 'https://mega.nz/'.")
        return

    megacmd_executable = None
    if is_tool_installed("mega-get"):
        megacmd_executable = "mega-get"
    elif is_tool_installed("megaget"): # Some systems might have it as megaget
        megacmd_executable = "megaget"
    
    if not megacmd_executable:
        print("Error: 'mega-get' or 'megaget' command not found.")
        print("Please ensure MEGAcmd is installed in Termux and in your PATH.")
        print("Try: pkg install megacmd")
        return
    
    print(f"Using '{megacmd_executable}' for download.")

    # Determine download root path (shared storage or Termux internal)
    termux_shared_download_root = os.path.expanduser("~/storage/downloads")
    chosen_download_root = ""

    if os.path.exists(termux_shared_download_root) and os.access(termux_shared_download_root, os.W_OK):
        chosen_download_root = termux_shared_download_root
        print(f"INFO: Will attempt to download to your shared Download folder base: {chosen_download_root}")
    else:
        chosen_download_root = os.path.expanduser("~") # Termux home directory
        print(f"WARNING: Could not access shared Download folder ('~/storage/downloads').")
        print("         This might be because 'termux-setup-storage' hasn't been run or permissions were denied.")
        print(f"INFO: Will download relative to Termux internal storage: {chosen_download_root}")

    # Create the specific download directory (e.g., ~/storage/downloads/megacmd_downloads)
    final_download_directory = os.path.join(chosen_download_root, download_base_dir_name)
    
    try:
        if not os.path.exists(final_download_directory):
            os.makedirs(final_download_directory, exist_ok=True)
            print(f"Ensured download directory exists: {final_download_directory}")
    except PermissionError:
        print(f"Error: Permission denied to create directory '{final_download_directory}'.")
        print("If using Termux and targeting shared storage, ensure 'termux-setup-storage' has been run and permissions granted.")
        return
    except Exception as e_mkdir:
        print(f"Error creating directory '{final_download_directory}': {e_mkdir}")
        return

    # Corrected command: mega-get <URL> <LOCAL_DESTINATION_DIRECTORY>
    # mega-get will download the file into this directory, keeping its original name.
    command = [
        megacmd_executable,
        mega_url,
        final_download_directory # This is the local path where the file will be saved
    ]

    print(f"Executing command: {' '.join(command)}")
    print("MEGAcmd will handle the download. This might take a while...")
    print("You should see progress output from MEGAcmd directly in the terminal.")

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)
        
        if process.stdout:
            for line in iter(process.stdout.readline, ''):
                print(line, end='') 
        
        process.wait() 
        
        if process.returncode == 0:
            print(f"\nMEGAcmd finished successfully.")
            print(f"File should be downloaded in: {final_download_directory}")
            print("Please check that directory for your file (it will have its original name from Mega).")
        else:
            # The error message from mega-get should have already been printed
            print(f"\nMEGAcmd failed with error code: {process.returncode}")
            print("Review the output above from MEGAcmd for specific error details.")


    except FileNotFoundError:
        print(f"Error: The command '{megacmd_executable}' was not found. Is MEGAcmd installed and in PATH?")
    except Exception as e:
        print(f"An unexpected error occurred while trying to run MEGAcmd: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    print("Mega.nz File Downloader (using MEGAcmd)")
    print("-----------------------------------------")
    print("Make sure MEGAcmd is installed: pkg install megacmd")
    print("And storage is set up if needed: termux-setup-storage")
    print("-----------------------------------------")

    while True:
        mega_link_input = input(f"Enter Mega link (or 'exit' to quit):\n").strip()

        if mega_link_input.lower() == 'exit':
            print("Exiting downloader.")
            break
        
        if not mega_link_input:
            print("No link provided. Please try again.")
            continue

        download_with_megacmd(mega_link_input, download_base_dir_name="megacmd_downloads")
        print("-----------------------------------------")
import os

# This function saves the scan results into separate text files inside the given folder
def save_results(results, folder):
    # Create the output folder if it doesn't already exist
    os.makedirs(folder, exist_ok=True)

    # Go through each result section (like 'emails', 'whois', etc.)
    for k in results:
        # Open a file named after the result key (e.g., 'emails.txt') for writing
        with open(os.path.join(folder, f"{k}.txt"), "w") as f:
            # Join all lines with a newline and write them to the file
            f.write("\n".join(results[k]))


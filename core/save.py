import os

def save_results(results, folder):
    os.makedirs(folder, exist_ok=True)
    for k in results:
        with open(os.path.join(folder, f"{k}.txt"), "w") as f:
            f.write("\\n".join(results[k]))

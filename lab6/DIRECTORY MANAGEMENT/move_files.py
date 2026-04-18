import os
import shutil

# Ensure folder exists
os.makedirs("Practice6/data/moved", exist_ok=True)

# Move file
if os.path.exists("sample.txt"):
    shutil.move("sample.txt", "Practice6/data/moved/sample.txt")
    print("File moved successfully.")
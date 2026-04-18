import os
# Create nested directories
os.makedirs("Practice6/data/files", exist_ok=True)
print("Directories created.")
# List files and folders
items = os.listdir("Practice6")
print("Inside Practice6:", items)

# Current working directory
print("Current directory:", os.getcwd())
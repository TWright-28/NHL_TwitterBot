import os

# Define the folder path where you want to delete .png files
folder_path = '../NHL_TwitterBot'

# Iterate through the files in the folder
for filename in os.listdir(folder_path):
    # Check if the file ends with ".png"
    if filename.endswith(".jpg"):
        # Construct the full file path
        file_path = os.path.join(folder_path, filename)
        
        # Try to remove the file
        try:
            os.remove(file_path)
            print(f"Deleted: {filename}")
        except Exception as e:
            print(f"Failed to delete {filename}: {str(e)}")
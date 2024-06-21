import os

# Define the directory path
directory = os.path.join(os.path.expanduser('~'), 'Downloads', 'test_files_directory')

# Create the directory if it doesn't exist
if not os.path.exists(directory):
    os.makedirs(directory)

# Create a test file within the directory
test_file_path = os.path.join(directory, "test.txt")
with open(test_file_path, "w") as test_file:
    test_file.write("This is a test file.")

print(f"Test file created at: {test_file_path}")

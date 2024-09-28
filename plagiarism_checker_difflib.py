import os
import sys
import difflib
from itertools import combinations

# Function to read the content of a file
def read_code(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to calculate similarity ratio between two files
def calculate_similarity(file1, file2):
    content1 = read_code(file1).splitlines()
    content2 = read_code(file2).splitlines()
    
    # Use difflib to compare files
    similarity = difflib.SequenceMatcher(None, content1, content2).ratio()
    return similarity

# Function to detect plagiarism in the class assignments
def detect_plagiarism(folder_path, threshold=0.8):
    files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.java')]
    plagiarism_cases = []

    # Compare each pair of files
    for file1, file2 in combinations(files, 2):
        similarity = calculate_similarity(file1, file2)
        
        # Report plagiarism if similarity exceeds threshold
        if similarity > threshold:
            plagiarism_cases.append((file1, file2, similarity))

    return plagiarism_cases

# Path to the folder containing the student assignments
folder_path = sys.argv[1]

# Detect plagiarism
threshold = 0.8  # Set similarity threshold (0 to 1), adjust based on sensitivity
plagiarism_results = detect_plagiarism(folder_path, threshold)

# Display plagiarism cases
if plagiarism_results:
    print(f"Plagiarism detected in the following pairs of files (threshold: {threshold}):\n")
    for file1, file2, similarity in plagiarism_results:
        print(f"{file1} and {file2} have a similarity of {similarity:.2f}")
else:
    print("No plagiarism detected.")

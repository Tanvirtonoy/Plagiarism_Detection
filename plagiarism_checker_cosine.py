import os
import sys
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to preprocess Java code (remove comments, normalize variable names, etc.)
def preprocess_java_code(code):
    # Remove single-line comments (// ...)
    code = re.sub(r'//.*', '', code)
    # Remove multi-line comments (/* ... */)
    code = re.sub(r'/\*[\s\S]*?\*/', '', code)
    # Remove import statements and package declarations
    code = re.sub(r'^\s*(import|package)\s+.*;', '', code, flags=re.MULTILINE)
    # Normalize variable names (replace them with a common token, e.g., VAR)
    code = re.sub(r'\b[a-zA-Z_]\w*\b', 'VAR', code)
    # Remove excess whitespace
    code = re.sub(r'\s+', ' ', code)
    return code

# Function to read and preprocess Java files
def read_and_preprocess_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    ##return preprocess_java_code(code)
    return code

# Function to detect plagiarism using NLP techniques (TF-IDF + Cosine Similarity)
def detect_plagiarism(folder_path, threshold=0.8):
    # Read and preprocess all Java files in the folder
    files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.java')]
    preprocessed_files = [read_and_preprocess_file(file) for file in files]
    
    # Apply TF-IDF vectorization
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(preprocessed_files)
    
    # Compute cosine similarity between all pairs of documents
    similarity_matrix = cosine_similarity(tfidf_matrix)
    
    # Find plagiarism cases (pairs with similarity > threshold)
    plagiarism_cases = []
    num_files = len(files)
    
    for i in range(num_files):
        for j in range(i+1, num_files):
            similarity = similarity_matrix[i][j]
            if similarity > threshold:
                plagiarism_cases.append((files[i], files[j], similarity))
    
    return plagiarism_cases

def detect_plagiarism2(folder_path, threshold=0.8):
    # Read and preprocess all Java files in the folder
    files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.java')]
    preprocessed_files = [read_and_preprocess_file(file) for file in files]
    
    # Apply TF-IDF vectorization
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(preprocessed_files).toarray()
    
    # Find plagiarism cases (pairs with similarity > threshold)
    plagiarism_cases = []
    num_files = len(files)
    
    for i in range(num_files):
        for j in range(i+1, num_files):
            similarity = cosine_similarity([tfidf_matrix[i],tfidf_matrix[j]])[0][1]
            if similarity > threshold:
                plagiarism_cases.append((files[i], files[j], similarity))
    
    return plagiarism_cases

# Path to the folder containing the Java assignments
folder_path = sys.argv[1]

# Detect plagiarism
threshold = 0.9  # Set similarity threshold (0 to 1), adjust based on sensitivity
plagiarism_results = detect_plagiarism2(folder_path, threshold)

# Display plagiarism cases
if plagiarism_results:
    print(f"Plagiarism detected in the following pairs of files (threshold: {threshold}):\n")
    for file1, file2, similarity in plagiarism_results:
        print(f"{file1} and {file2} have a similarity of {similarity:.2f}")
else:
    print("No plagiarism detected.")

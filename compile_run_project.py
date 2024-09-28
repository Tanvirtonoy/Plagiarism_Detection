import os
import sys
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to compile and run a Java project
def compile_and_run_project(project_path, output_dir):
    try:
        # Create a directory for output files if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Get the project name (assumed to be the folder name)
        project_name = os.path.basename(project_path)
        
        # Compile the project (assume all .java files are in the project folder)
        compile_cmd = f"mvn install -f {project_path}/pom.xml"
        compile_result = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)
        
        # Create output file for compilation result
        compile_output_file = os.path.join(output_dir, f"{project_name}_compile_output.txt")
        with open(compile_output_file, 'w') as f:
            f.write(compile_result.stdout if compile_result.stdout else compile_result.stderr)
        
        # Check if the compilation was successful
        if compile_result.returncode != 0:
            print(f"Compilation failed for {project_name}, check {compile_output_file} for details.")
            return
        
        # Run the project (assuming Main class is the entry point)
        run_cmd = f"~/hadoop-3.2.2/bin/hadoop jar {project_path}/target/*.jar Twitter {project_path}/small-twitter.csv {project_path}/tmp_dir {output_dir}/output_{project_name}"
        run_result = subprocess.run(run_cmd, shell=True, capture_output=True, text=True)
        
        # Create output file for execution result
        run_output_file = os.path.join(output_dir, f"{project_name}_run_output.txt")
        with open(run_output_file, 'w') as f:
            f.write(run_result.stdout if run_result.stdout else run_result.stderr)
        
        #print(f"Project {project_name} compiled and ran successfully. Results saved in {run_output_file}.")
    
    except Exception as e:
        print(f"Error processing project {project_name}: {str(e)}")

# Function to build and run all Java projects in parallel
def build_and_run_all_projects(folder_path, output_dir):
    # Get a list of all project directories
    projects = [os.path.join(folder_path, d) for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]
    # Get a list of all project files
    #project_files = [os.path.join(folder_path, d) for d in os.scandir(folder_path) if d.is_file()]
    # Use ThreadPoolExecutor to run projects in parallel
    with ThreadPoolExecutor(max_workers=4) as executor:  # Adjust the number of workers (threads) based on system capacity
        futures = {executor.submit(compile_and_run_project, project, output_dir): project for project in projects}
        
        for future in as_completed(futures):
            project = futures[future]
            try:
                future.result()  # Get the result of the task (if any exception, it will be raised here)
            except Exception as e:
                print(f"Error running project {project}: {str(e)}")

# Main execution
if __name__ == "__main__":
    # Path to the folder containing student projects (each project is in its own folder)
    projects_folder = sys.argv[1]
    
    # Path to the folder where output files will be stored
    output_folder = sys.argv[2]
    
    # Build and run all projects
    build_and_run_all_projects(projects_folder, output_folder)

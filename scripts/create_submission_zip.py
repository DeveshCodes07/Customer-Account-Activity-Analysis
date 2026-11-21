import os
import zipfile

def create_submission_zip():
    root_dir = os.path.abspath('.')
    zip_path = os.path.join(root_dir, 'CAAA_Complete_Project_Submission.zip')
    docs_zip_path = os.path.join(root_dir, 'docs', 'CAAA_Complete_Project_Submission.zip')
    
    # Exclude patterns
    exclude_dirs = {'.venv', '.git', '__pycache__', '.pytest_cache', 'submission_lms'}
    exclude_files = {'CAAA_Complete_Project_Submission.zip', 'temp_clean.docx'}
    
    print(f"Creating project submission ZIP: {zip_path}...")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zout:
        for root, dirs, files in os.walk(root_dir):
            # Modify dirs in-place to skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]
            
            for file in files:
                if file in exclude_files or file.startswith('~') or file.startswith('temp_'):
                    continue
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, root_dir)
                zout.write(abs_path, rel_path)
                
    print(f"ZIP created successfully! Size: {os.path.getsize(zip_path)} bytes ({os.path.getsize(zip_path)/(1024*1024):.2f} MB)")
    
    # Copy to docs/ as well
    import shutil
    shutil.copy2(zip_path, docs_zip_path)
    print(f"Copied to: {docs_zip_path}")

if __name__ == '__main__':
    create_submission_zip()

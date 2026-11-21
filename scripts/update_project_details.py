import os
import re
import zipfile
import shutil

REPLACEMENTS = [
    # Mentor
    (r"Prof\.\s*Alpna\s*Lodhi,\s*Assistant\s*Professor\s*\(MCA\)", "Mr. Dinesh, Mentor (Data Analytics)"),
    (r"Prof\.\s*Alpna\s*Lodhi,\s*Department\s*of\s*Computer\s*Applications", "Mr. Dinesh, Mentor (Data Analytics)"),
    (r"Prof\.\s*Alpna\s*Lodhi", "Mr. Dinesh"),
    (r"Alpna\s*Lodhi", "Mr. Dinesh"),
    (r"Mentor:\s*&lt;name&gt;", "Mentor: Mr. Dinesh"),
    (r"Mentor:\s*<name>", "Mentor: Mr. Dinesh"),
    (r"Mentor:\s*Prof\.\s*Alpna\s*Lodhi", "Mentor (Data Analytics): Mr. Dinesh"),
    
    # Batch ID
    (r"MCA\s*2nd\s*Year\s*Data\s*Analyst\s*-\s*ABES_OND26_MCA\s*Batch\s*&lt;no&gt;", "MCA 2nd Year Data Analyst - Batch 01"),
    (r"MCA\s*2nd\s*Year\s*Data\s*Analyst\s*-\s*ABES_OND26_MCA\s*Batch\s*<no>", "MCA 2nd Year Data Analyst - Batch 01"),
    (r"ABES_OND26_MCA\s*Batch\s*&lt;no&gt;", "Batch 01"),
    (r"ABES_OND26_MCA\s*Batch\s*<no>", "Batch 01"),
    (r"ABES_OND26_MCA", "Batch 01"),
    (r"Batch\s*&lt;no&gt;", "Batch 01"),
    (r"Batch\s*<no>", "Batch 01"),
    
    # Project ID
    (r"&lt;Project\s*ID&gt;", "P063"),
    (r"<Project\s*ID>", "P063"),
    (r"Project\s*ID:\s*CAAA", "Project ID: P063"),
    (r"Project\s*Document\s*\|\s*CAAA", "Project Document | P063"),
    (r"CAAA\s*-\s*Customer\s*Account\s*Activity\s*Analysis", "P063 - Customer Account Activity Analysis"),
    (r"CAAA\s*-\s*FinEdge", "P063 - FinEdge"),
    (r"FinEdge\s*CAAA", "FinEdge P063"),
    (r"\(CAAA\)", "(P063)")
]

def update_zip_office_file(file_path):
    temp_path = file_path + ".tmp"
    modified = False
    
    with zipfile.ZipFile(file_path, 'r') as zin, zipfile.ZipFile(temp_path, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename.endswith(('.xml', '.rels', '.txt')):
                try:
                    text = data.decode('utf-8')
                    orig_text = text
                    for pattern, repl in REPLACEMENTS:
                        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
                    if text != orig_text:
                        modified = True
                        data = text.encode('utf-8')
                except UnicodeDecodeError:
                    pass
            zout.writestr(item, data)
            
    if modified:
        shutil.move(temp_path, file_path)
        print(f"Updated: {file_path}")
    else:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        print(f"No changes needed: {file_path}")
    return modified

def update_text_file(file_path):
    if not os.path.exists(file_path):
        return False
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    orig_text = text
    for pattern, repl in REPLACEMENTS:
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
    if text != orig_text:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Updated text file: {file_path}")
        return True
    return False

def main():
    print("=== STARTING BATCH UPDATE OF ROLL NO, BATCH ID, PROJECT ID, AND MENTOR ===")
    print("Roll No: 2500320140050")
    print("Batch ID: Batch 01")
    print("Project ID: P063")
    print("Project Mentor: Mr. Dinesh (Data Analytics)\n")
    
    # 1. Update text/code files
    text_targets = [
        "app.py",
        "README.md",
        "BUILD_PLAN.md",
        "src/generate_data.py",
        "scripts/generate_github_report.py",
        "scripts/generate_complete_code_doc.py",
        "scripts/stage_lms_submission.py"
    ]
    for tf in text_targets:
        update_text_file(os.path.abspath(tf))
        
    # 2. Update all Office documents in docs/ and root
    office_targets = []
    for root, dirs, files in os.walk('.'):
        if any(p in root for p in ['.git', '.venv', '__pycache__', '.pytest_cache', 'submission_lms']):
            continue
        for f in files:
            if f.endswith(('.docx', '.pptx', '.xlsx')) and not f.startswith('~') and not f.startswith('temp'):
                office_targets.append(os.path.join(root, f))
                
    for of in sorted(office_targets):
        update_zip_office_file(os.path.abspath(of))
        
    print("\nAll files successfully updated!")

if __name__ == '__main__':
    main()

import os
import re
import zipfile
import subprocess
import shutil

def strip_update_fields(docx_path, out_path):
    with zipfile.ZipFile(docx_path, 'r') as zin, zipfile.ZipFile(out_path, 'w') as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == 'word/settings.xml':
                data = re.sub(rb'<w:updateFields[^>]*/>', b'', data)
            zout.writestr(item, data)

def polish_xml_files():
    print("--- 1. Polishing XML in docx, pptx, and xlsx ---")
    replacements = [
        (r"Batch\s*01\s*Batch\s*01", "Batch 01"),
        (r"https://github\.com/deveshkumar-abes/2500320140050-caaa", "https://github.com/DeveshCodes07/Customer-Account-Activity-Analysis"),
        (r"https://2500320140050-caaa\.streamlit\.app", "https://customer-account-activity-analysis.streamlit.app")
    ]
    
    for root, dirs, files in os.walk('.'):
        if any(p in root for p in ['.git', '.venv', '__pycache__', '.pytest_cache', 'submission_lms']):
            continue
        for f in files:
            if f.endswith(('.docx', '.pptx', '.xlsx')) and not f.startswith('~') and not f.startswith('temp'):
                p = os.path.join(root, f)
                temp_p = p + ".tmp"
                modified = False
                with zipfile.ZipFile(p, 'r') as zin, zipfile.ZipFile(temp_p, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
                    for item in zin.infolist():
                        data = zin.read(item.filename)
                        if item.filename.endswith(('.xml', '.rels', '.txt')):
                            try:
                                text = data.decode('utf-8')
                                orig = text
                                for pat, rep in replacements:
                                    text = re.sub(pat, rep, text, flags=re.IGNORECASE)
                                if text != orig:
                                    modified = True
                                    data = text.encode('utf-8')
                            except UnicodeDecodeError:
                                pass
                        zout.writestr(item, data)
                if modified:
                    shutil.move(temp_p, p)
                    print(f"Polished: {p}")
                else:
                    if os.path.exists(temp_p):
                        os.remove(temp_p)

def reexport_all_pdfs():
    print("\n--- 2. Re-exporting all PDFs via Word COM and PowerPoint COM ---")
    
    # 2.1 Rebuild GitHub Report & Complete Code DOCX first
    subprocess.run(["python", "scripts/generate_github_report.py"], check=True)
    subprocess.run(["python", "scripts/generate_complete_code_doc.py"], check=True)
    
    # 2.2 Re-export Presentation PPTX -> PDF
    subprocess.run(["python", "scripts/test_ppt_convert.py"], check=True)
    
    # 2.3 Re-export All Step Documents to PDF
    subprocess.run(["python", "scripts/convert_all_steps_to_pdf.py"], check=True)
    
    # Copy presentation to all steps folder
    shutil.copy2("docs/CAAA_Presentation.pdf", "docs/all_step_documents_pdf/18_CAAA_Presentation.pdf")
    shutil.copy2("docs/CAAA_Presentation.pdf", "docs/all_step_documents_pdf/CAAA_Presentation.pdf")
    print("Presentation PDF synced to all_step_documents_pdf/")

def restage_lms_and_zip():
    print("\n--- 3. Re-staging LMS Submission and Re-creating Submission ZIP ---")
    subprocess.run(["python", "scripts/stage_lms_submission.py"], check=True)
    subprocess.run(["python", "scripts/create_submission_zip.py"], check=True)
    print("All tasks completed successfully!")

if __name__ == '__main__':
    polish_xml_files()
    reexport_all_pdfs()
    restage_lms_and_zip()

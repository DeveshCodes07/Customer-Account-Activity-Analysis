import os
import shutil

src_map = {
    "docs/CAAA_Project_Document.pdf": "2500320140050_DeveshKumar_Project_Report.pdf",
    "docs/CAAA_Presentation.pdf": "2500320140050_DeveshKumar_Presentation.pdf",
    "docs/CAAA_Complete_Code.pdf": "2500320140050_DeveshKumar_Source_Code.pdf",
    "docs/08_Database_Design.xlsx": "2500320140050_DeveshKumar_Database_Schema.xlsx",
    "data/caaa_data.xlsx": "2500320140050_DeveshKumar_Project_Database.xlsx",
    "docs/CAAA_GitHub_Report.pdf": "2500320140050_DeveshKumar_GitHub_and_Streamlit_Details.pdf",
    "docs/all_step_documents_pdf/01_Project_Understanding.pdf": "2500320140050_DeveshKumar_01_Project_Understanding.pdf",
    "docs/all_step_documents_pdf/02_HMW_Statements.pdf": "2500320140050_DeveshKumar_02_HMW.pdf",
    "docs/all_step_documents_pdf/03_Needs_Analysis.pdf": "2500320140050_DeveshKumar_03_Needs_Analysis.pdf",
    "docs/04_Traceability_Matrix.xlsx": "2500320140050_DeveshKumar_04_Traceability_Matrix.xlsx",
    "docs/all_step_documents_pdf/05_BRD.pdf": "2500320140050_DeveshKumar_05_BRD.pdf",
    "docs/all_step_documents_pdf/07_TRD.pdf": "2500320140050_DeveshKumar_07_TRD.pdf",
    "docs/all_step_documents_pdf/09_ER_Diagram.pdf": "2500320140050_DeveshKumar_09_ER_Diagram.pdf",
    "docs/all_step_documents_pdf/10_Dataset_Validation_Report.pdf": "2500320140050_DeveshKumar_10_Data_Validation_Report.pdf",
    "docs/all_step_documents_pdf/11_User_Stories.pdf": "2500320140050_DeveshKumar_11_User_Stories.pdf",
    "docs/all_step_documents_pdf/12_UI_Framework.pdf": "2500320140050_DeveshKumar_12_UI_Framework.pdf",
    "docs/all_step_documents_pdf/13_Test_Cases.pdf": "2500320140050_DeveshKumar_13_Test_Cases.pdf",
    "CAAA_Complete_Project_Submission.zip": "2500320140050_DeveshKumar_Project.zip"
}

out_dir = os.path.abspath("submission_lms")
os.makedirs(out_dir, exist_ok=True)

total_size = 0
print("Staging LMS submission files:")
for src, dst in src_map.items():
    if os.path.exists(src):
        dst_path = os.path.join(out_dir, dst)
        shutil.copy2(src, dst_path)
        size = os.path.getsize(dst_path)
        total_size += size
        print(f" - {dst} ({size/(1024*1024):.2f} MB)")
    else:
        print(f" MISSING: {src}")

print(f"\nTotal staged files: {len(src_map)} (Limit: <= 20 files)")
print(f"Total size: {total_size/(1024*1024):.2f} MB (Limit: < 100 MB)")

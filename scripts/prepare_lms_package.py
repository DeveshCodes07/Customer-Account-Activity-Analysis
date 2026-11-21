import os
import shutil

src_list = [
    # 1. Project Report (PDF)
    ("docs/CAAA_Project_Document.pdf", "2500320140050_DeveshKumar_Project_Report.pdf"),
    
    # 2. Presentation (PPT as PDF)
    ("docs/CAAA_Presentation.pdf", "2500320140050_DeveshKumar_Presentation.pdf"),
    
    # 3. Source Code PDF
    ("docs/CAAA_Complete_Code.pdf", "2500320140050_DeveshKumar_Source_Code.pdf"),
    
    # 4. Database Schema (XLSX)
    ("docs/08_Database_Design.xlsx", "2500320140050_DeveshKumar_Database_Schema.xlsx"),
    
    # 5. Project Database (XLSX)
    ("data/caaa_data.xlsx", "2500320140050_DeveshKumar_Project_Database.xlsx"),
    
    # 6. GitHub and Streamlit Details PDF
    ("docs/CAAA_GitHub_Report.pdf", "2500320140050_DeveshKumar_GitHub_and_Streamlit_Details.pdf"),
    
    # 7-18. Other Project Documents in step order
    ("docs/all_step_documents_pdf/01_Project_Understanding.pdf", "2500320140050_DeveshKumar_01_Project_Understanding.pdf"),
    ("docs/all_step_documents_pdf/02_HMW_Statements.pdf", "2500320140050_DeveshKumar_02_HMW.pdf"),
    ("docs/all_step_documents_pdf/03_Needs_Analysis.pdf", "2500320140050_DeveshKumar_03_Needs_Analysis.pdf"),
    ("docs/04_Traceability_Matrix.xlsx", "2500320140050_DeveshKumar_04_Traceability_Matrix.xlsx"),
    ("docs/all_step_documents_pdf/05_BRD.pdf", "2500320140050_DeveshKumar_05_BRD.pdf"),
    ("docs/all_step_documents_pdf/07_TRD.pdf", "2500320140050_DeveshKumar_07_TRD.pdf"),
    ("docs/08_Database_Design.xlsx", "2500320140050_DeveshKumar_08_Database_Design.xlsx"),
    ("docs/all_step_documents_pdf/09_ER_Diagram.pdf", "2500320140050_DeveshKumar_09_ER_Diagram.pdf"),
    ("docs/all_step_documents_pdf/10_Dataset_Validation_Report.pdf", "2500320140050_DeveshKumar_10_Data_Validation_Report.pdf"),
    ("docs/all_step_documents_pdf/11_User_Stories.pdf", "2500320140050_DeveshKumar_11_User_Stories.pdf"),
    ("docs/all_step_documents_pdf/12_UI_Framework.pdf", "2500320140050_DeveshKumar_12_UI_Framework.pdf"),
    ("docs/all_step_documents_pdf/13_Test_Cases.pdf", "2500320140050_DeveshKumar_13_Test_Cases.pdf")
]

def main():
    target_dir = os.path.abspath("LMS_Upload_Ready_Package")
    os.makedirs(target_dir, exist_ok=True)
    
    print(f"Creating LMS_Upload_Ready_Package at: {target_dir}")
    
    total_size = 0
    pdf_count = 0
    xlsx_count = 0
    
    for src, dst in src_list:
        if os.path.exists(src):
            dst_path = os.path.join(target_dir, dst)
            shutil.copy2(src, dst_path)
            size = os.path.getsize(dst_path)
            total_size += size
            if dst.endswith('.pdf'):
                pdf_count += 1
            elif dst.endswith('.xlsx'):
                xlsx_count += 1
            print(f"Copied: {dst} ({size/(1024*1024):.2f} MB)")
        else:
            print(f"ERROR: Missing source file {src}")
            
    print("\n--- Package Verification ---")
    files = sorted(os.listdir(target_dir))
    print(f"Total files in LMS_Upload_Ready_Package: {len(files)}")
    print(f"PDF files: {pdf_count}")
    print(f"XLSX files: {xlsx_count}")
    print(f"Total package size: {total_size/(1024*1024):.2f} MB")
    
    # Assert constraints
    assert len(files) == 18, f"Expected 18 files, got {len(files)}"
    assert pdf_count == 14, f"Expected 14 PDFs, got {pdf_count}"
    assert xlsx_count == 4, f"Expected 4 XLSXs, got {xlsx_count}"
    assert all(not f.endswith(('.zip', '.ppt', '.pptx')) for f in files), "Forbidden extensions (.zip, .ppt, .pptx) found!"
    print("All constraints verified successfully!")

if __name__ == '__main__':
    main()

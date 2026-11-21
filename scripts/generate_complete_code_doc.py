import os
import subprocess
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=60, bottom=60, left=90, right=90):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def set_table_borders(table, color="D9D9D9"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="{color}"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="{color}"/>
            <w:left w:val="single" w:sz="4" w:space="0" w:color="{color}"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="{color}"/>
            <w:insideH w:val="none"/>
            <w:insideV w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def build_complete_code_doc():
    doc = docx.Document()
    
    # Page setup A4, 2cm margins
    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(0.787)
    section.bottom_margin = Inches(0.787)
    section.left_margin = Inches(0.787)
    section.right_margin = Inches(0.787)
    section.header_distance = Inches(0.492)
    section.footer_distance = Inches(0.492)
    
    # Header & Footer
    hdr = section.header.paragraphs[0]
    hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hrun = hdr.add_run("ABES Engineering College | Complete System Source Code | P063")
    hrun.font.name = "Calibri"
    hrun.font.size = Pt(8)
    hrun.font.color.rgb = RGBColor(0x7F, 0x7F, 0x7F)
    
    ftr = section.footer.paragraphs[0]
    ftr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    frun = ftr.add_run("Devesh Kumar | Roll No 2500320140050     Source Code Compendium")
    frun.font.name = "Calibri"
    frun.font.size = Pt(8)
    frun.font.color.rgb = RGBColor(0x7F, 0x7F, 0x7F)
    
    # Title Page
    p_inst = doc.add_paragraph()
    r_inst = p_inst.add_run("HCLTech Career Shaper Programme | ABES Engineering College, Ghaziabad")
    r_inst.font.name = "Calibri"
    r_inst.font.size = Pt(10)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(0xA5, 0x1C, 0x30)
    
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(24)
    r_title = p_title.add_run("COMPLETE PRODUCTION SOURCE CODE COMPENDIUM")
    r_title.font.name = "Georgia"
    r_title.font.size = Pt(20)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x15, 0x15, 0x14)
    
    p_sub = doc.add_paragraph()
    r_sub = p_sub.add_run("Project ID: P063 — FinEdge Retail Banking Customer Account Activity Analysis")
    r_sub.font.name = "Georgia"
    r_sub.font.size = Pt(12)
    r_sub.font.color.rgb = RGBColor(0xA5, 0x1C, 0x30)
    
    meta_data = [
        ("Candidate Name", "Devesh Kumar"),
        ("University Roll No", "2500320140050"),
        ("Academic Programme", "MCA 2nd Year (Data Analytics)"),
        ("Batch ID", "Batch 01"),
        ("Faculty Mentor", "Mr. Dinesh, Mentor (Data Analytics)"),
        ("Industry Client", "FinEdge Digital Solutions Pvt. Ltd., Noida"),
        ("Repository URL", "https://github.com/DeveshCodes07/Customer-Account-Activity-Analysis"),
        ("Branch & State", "main | Verified Clean & Fully Tested (15/15 passed)"),
        ("Technology Stack", "Python 3.14, Streamlit 1.67, SQLite 3, Pandas, Scipy, Plotly, Tailwind CSS"),
        ("Version & Date", "v1.0 Final — 20 November 2026")
    ]
    
    t_meta = doc.add_table(rows=len(meta_data), cols=2)
    t_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, (k, v) in enumerate(meta_data):
        row = t_meta.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.8)
        set_cell_margins(c0)
        set_cell_margins(c1)
        set_cell_shading(c0, "F4F1F1")
        
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(k)
        r0.font.name = "Calibri"
        r0.font.size = Pt(9.5)
        r0.font.bold = True
        
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(v)
        r1.font.name = "Calibri"
        r1.font.size = Pt(9.5)
        if "http" in v:
            r1.font.bold = True
            r1.font.color.rgb = RGBColor(0x00, 0x56, 0xB3)
            
    doc.add_page_break()
    
    # Files to include
    code_files = [
        ("app.py", "Main Control Tower & Routing Hub", "Python / Streamlit"),
        (".streamlit/config.toml", "Streamlit UI Theme & Color Palette", "TOML Configuration"),
        ("requirements.txt", "Pinned Dependencies & Python Environment", "Package Requirements"),
        ("data/schema.sql", "SQLite 3NF Schema & Analytical View DDL", "SQL DDL"),
        ("src/data_loader.py", "Cross-Platform Pathlib SQLite Connector", "Python Backend"),
        ("src/data_cleaner.py", "Data Cleansing, Imputation & Canonical Aliases", "Python Backend"),
        ("src/analytics.py", "Core Financial Analytics & Risk Engine", "Python Backend"),
        ("src/ui.py", "Tailwind CSS CDN Component Library", "Python / HTML / CSS"),
        ("src/generate_data.py", "Reproducible Synthetic Banking Generator (Seed 42)", "Python Backend"),
        ("pages/1_📊_Portfolio_Overview.py", "Screen 1: Portfolio Overview & HNW Pareto", "Python / Streamlit"),
        ("pages/2_📈_Transaction_Trends.py", "Screen 2: Monthly Trends & Ticket Size Flow", "Python / Streamlit"),
        ("pages/3_⚡_Channel_Analytics.py", "Screen 3: Channel Throughput & Failure Alerts", "Python / Streamlit"),
        ("pages/4_👤_Customer_360.py", "Screen 4: Customer Drilldown & Penalty Simulator", "Python / Streamlit"),
        ("pages/5_⚠️_Dormancy_and_Churn.py", "Screen 5: 4-Tier Dormancy & Churn Contraction", "Python / Streamlit"),
        ("pages/6_👥_Demographic_Insights.py", "Screen 6: Occupation Boxplots & OLS Scatter", "Python / Streamlit"),
        ("tests/test_data.py", "Database Schema, Integrity & Performance Tests", "Pytest Suite"),
        ("tests/test_analysis.py", "Analytical Formulation & Numerical Verification", "Pytest Suite"),
        ("tests/test_app.py", "Streamlit AppTest Headless Multi-Page Tests", "Pytest Suite")
    ]
    
    # Table of Contents
    h_toc = doc.add_paragraph()
    r_htoc = h_toc.add_run("Source Code Inventory & Table of Contents")
    r_htoc.font.name = "Georgia"
    r_htoc.font.size = Pt(14)
    r_htoc.font.bold = True
    r_htoc.font.color.rgb = RGBColor(0xA5, 0x1C, 0x30)
    
    t_toc = doc.add_table(rows=len(code_files) + 1, cols=4)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_names = ["File Path", "Functional Purpose", "Type", "Line Count"]
    widths = [Inches(2.5), Inches(2.7), Inches(1.2), Inches(0.6)]
    for j, (name, w) in enumerate(zip(col_names, widths)):
        cell = t_toc.rows[0].cells[j]
        cell.width = w
        set_cell_margins(cell, top=60, bottom=60)
        set_cell_shading(cell, "A51C30")
        p = cell.paragraphs[0]
        r = p.add_run(name)
        r.font.name = "Calibri"
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for i, (rel_path, desc, ftype) in enumerate(code_files):
        row = t_toc.rows[i + 1]
        line_cnt = 0
        if os.path.exists(rel_path):
            with open(rel_path, 'r', encoding='utf-8', errors='ignore') as f:
                line_cnt = len(f.readlines())
        for j, val in enumerate([rel_path, desc, ftype, str(line_cnt)]):
            cell = row.cells[j]
            cell.width = widths[j]
            set_cell_margins(cell)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Consolas" if j in (0, 3) else "Calibri"
            r.font.size = Pt(8.5)
            
    doc.add_page_break()
    
    # Add each code file
    for rel_path, desc, ftype in code_files:
        if not os.path.exists(rel_path):
            continue
        with open(rel_path, 'r', encoding='utf-8', errors='ignore') as f:
            code_text = f.read()
        lines = code_text.splitlines()
        
        # File Header
        h_file = doc.add_paragraph()
        h_file.paragraph_format.space_before = Pt(14)
        h_file.paragraph_format.space_after = Pt(2)
        r_hf = h_file.add_run(f"Module: {rel_path}")
        r_hf.font.name = "Georgia"
        r_hf.font.size = Pt(12)
        r_hf.font.bold = True
        r_hf.font.color.rgb = RGBColor(0xA5, 0x1C, 0x30)
        
        p_subf = doc.add_paragraph()
        p_subf.paragraph_format.space_after = Pt(6)
        r_subf = p_subf.add_run(f"Description: {desc} | Type: {ftype} | Lines: {len(lines)}")
        r_subf.font.name = "Calibri"
        r_subf.font.size = Pt(8.5)
        r_subf.font.color.rgb = RGBColor(0x7F, 0x7F, 0x7F)
        
        # Code Table
        t_code = doc.add_table(rows=1, cols=1)
        t_code.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = t_code.rows[0].cells[0]
        cell.width = Inches(7.0)
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        set_cell_shading(cell, "F8F9FA")
        set_table_borders(t_code, color="D0D5DD")
        
        p_code = cell.paragraphs[0]
        p_code.paragraph_format.space_before = Pt(0)
        p_code.paragraph_format.space_after = Pt(0)
        p_code.paragraph_format.line_spacing = Pt(9.5)
        
        # Add formatted numbered lines
        for idx, line in enumerate(lines, 1):
            r_num = p_code.add_run(f"{idx:4d}  ")
            r_num.font.name = "Consolas"
            r_num.font.size = Pt(7.5)
            r_num.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
            
            r_text = p_code.add_run(line + "\n")
            r_text.font.name = "Consolas"
            r_text.font.size = Pt(7.5)
            r_text.font.color.rgb = RGBColor(0x1F, 0x24, 0x28)
            
        doc.add_paragraph() # Spacing between files
        
    out_docx = os.path.abspath("docs/CAAA_Complete_Code.docx")
    doc.save(out_docx)
    print("Complete Code DOCX saved to:", out_docx)
    return out_docx

if __name__ == '__main__':
    docx_file = build_complete_code_doc()
    pdf_file = os.path.abspath("docs/CAAA_Complete_Code.pdf")
    
    ps_cmd = f'''
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    try {{
        $doc = $word.Documents.Open('{docx_file}', $false, $true)
        $doc.ExportAsFixedFormat('{pdf_file}', 17)
        $doc.Close($false)
        Write-Output "Complete Code PDF created successfully"
    }} finally {{
        $word.Quit()
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
    }}
    '''
    res = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True)
    print("STDOUT:", res.stdout)
    print("STDERR:", res.stderr)
    print("PDF exists:", os.path.exists(pdf_file), "Size:", os.path.getsize(pdf_file) if os.path.exists(pdf_file) else 0)

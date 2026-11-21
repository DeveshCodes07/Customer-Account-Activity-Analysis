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

def convert_all_steps():
    docs_dir = os.path.abspath('docs')
    out_dir = os.path.abspath('docs/all_step_documents_pdf')
    os.makedirs(out_dir, exist_ok=True)
    
    docx_files = [f for f in sorted(os.listdir(docs_dir)) if f.endswith('.docx') and not f.startswith('~') and not f.startswith('temp')]
    print(f"Found {len(docx_files)} DOCX files to convert...")
    
    # PowerShell script to batch convert using a single Word instance
    ps_lines = [
        "$word = New-Object -ComObject Word.Application",
        "$word.Visible = $false",
        "$word.DisplayAlerts = 0",
        "try {"
    ]
    
    clean_tmps = []
    for f in docx_files:
        src = os.path.join(docs_dir, f)
        base_name = os.path.splitext(f)[0]
        pdf_out = os.path.join(out_dir, base_name + ".pdf")
        tmp_clean = os.path.join(docs_dir, f"temp_{base_name}.docx")
        
        strip_update_fields(src, tmp_clean)
        clean_tmps.append(tmp_clean)
        
        # Word COM conversion commands
        ps_lines.append(f'    Write-Output "Converting {f}..."')
        ps_lines.append(f'    $doc = $word.Documents.Open("{tmp_clean}", $false, $true)')
        ps_lines.append(f'    $doc.ExportAsFixedFormat("{pdf_out}", 17)')
        ps_lines.append(f'    $doc.Close($false)')
        
    ps_lines.extend([
        '    Write-Output "All step documents converted to PDF successfully!"',
        '} finally {',
        '    $word.Quit()',
        '    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null',
        '}'
    ])
    
    ps_script = "\n".join(ps_lines)
    ps_file = os.path.abspath('scripts/batch_convert.ps1')
    with open(ps_file, 'w', encoding='utf-8') as f:
        f.write(ps_script)
        
    print("Executing batch conversion via Word COM...")
    res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_file], capture_output=True, text=True)
    print("STDOUT:", res.stdout)
    if res.stderr:
        print("STDERR:", res.stderr)
        
    # Clean up temp files
    for tmp in clean_tmps:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except Exception:
                pass
    if os.path.exists(ps_file):
        os.remove(ps_file)
        
    generated = os.listdir(out_dir)
    print(f"Generated {len(generated)} PDFs in {out_dir}:")
    for g in sorted(generated):
        print(f" - {g} ({os.path.getsize(os.path.join(out_dir, g))} bytes)")

if __name__ == '__main__':
    convert_all_steps()

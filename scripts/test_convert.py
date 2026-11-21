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

if __name__ == '__main__':
    src = os.path.abspath('docs/CAAA_Project_Document.docx')
    tmp = os.path.abspath('docs/temp_clean.docx')
    pdf = os.path.abspath('docs/CAAA_Project_Document.pdf')
    strip_update_fields(src, tmp)
    print("Cleaned docx written to:", tmp)
    
    ps_cmd = f'''
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    try {{
        $doc = $word.Documents.Open('{tmp}', $false, $true)
        $doc.ExportAsFixedFormat('{pdf}', 17)
        $doc.Close($false)
        Write-Output "PDF created successfully"
    }} finally {{
        $word.Quit()
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
    }}
    '''
    res = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True)
    print("STDOUT:", res.stdout)
    print("STDERR:", res.stderr)
    if os.path.exists(tmp):
        os.remove(tmp)
    print("PDF exists:", os.path.exists(pdf), "Size:", os.path.getsize(pdf) if os.path.exists(pdf) else 0)

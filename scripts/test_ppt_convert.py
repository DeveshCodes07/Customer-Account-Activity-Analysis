import os
import subprocess

if __name__ == '__main__':
    pptx = os.path.abspath('docs/CAAA_Presentation.pptx')
    pdf = os.path.abspath('docs/CAAA_Presentation.pdf')
    print("Converting PPTX to PDF:", pptx)
    ps_cmd = f'''
    $ppt = New-Object -ComObject PowerPoint.Application
    try {{
        $pres = $ppt.Presentations.Open('{pptx}', $true, $false, $false)
        $pres.SaveAs('{pdf}', 32)
        $pres.Close()
        Write-Output "PPT PDF created successfully"
    }} finally {{
        $ppt.Quit()
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($ppt) | Out-Null
    }}
    '''
    res = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True)
    print("STDOUT:", res.stdout)
    print("STDERR:", res.stderr)
    print("PDF exists:", os.path.exists(pdf), "Size:", os.path.getsize(pdf) if os.path.exists(pdf) else 0)

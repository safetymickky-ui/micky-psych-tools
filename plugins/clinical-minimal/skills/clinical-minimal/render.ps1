# Export .docx / .pptx / .xlsx to PDF with the installed Office apps, for visual QA.
# Usage: powershell -ExecutionPolicy Bypass -File render.ps1 <file> [<file> ...]
param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Paths)
foreach ($p in $Paths) {
  $src = (Resolve-Path $p).Path
  $pdf = [IO.Path]::ChangeExtension($src, '.pdf')
  switch ([IO.Path]::GetExtension($src).ToLower()) {
    '.docx' { $app = New-Object -ComObject Word.Application; $app.Visible = $false
              $d = $app.Documents.Open($src, $false, $true); $d.SaveAs2($pdf, 17); $d.Close($false); $app.Quit() }
    '.pptx' { $app = New-Object -ComObject PowerPoint.Application
              $d = $app.Presentations.Open($src, $true, $false, $false); $d.SaveAs($pdf, 32); $d.Close(); $app.Quit() }
    '.xlsx' { $app = New-Object -ComObject Excel.Application; $app.Visible = $false; $app.DisplayAlerts = $false
              $d = $app.Workbooks.Open($src, 0, $true); $d.ExportAsFixedFormat(0, $pdf); $d.Close($false); $app.Quit() }
    default { Write-Error "Unsupported: $src"; continue }
  }
  [void][Runtime.InteropServices.Marshal]::ReleaseComObject($app)
  Write-Output $pdf
}

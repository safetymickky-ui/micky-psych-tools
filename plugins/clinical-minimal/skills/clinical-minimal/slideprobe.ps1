# Measure a deck as PowerPoint lays it out: one PNG per slide plus every shape's box, the box its text
# really occupies, its line breaks and font sizes, and each slide's animation/transition state.
# Called by slidecheck.py. Usage: powershell -File slideprobe.ps1 <deck.pptx> <outdir>
param([string]$Deck, [string]$Out)
$src = (Resolve-Path $Deck).Path
New-Item -ItemType Directory -Force $Out | Out-Null
$app = New-Object -ComObject PowerPoint.Application
$pres = $app.Presentations.Open($src, $true, $false, $false)
$slides = @()
foreach ($s in $pres.Slides) {
  $n = '{0:D2}' -f $s.SlideIndex
  $s.Export((Join-Path $Out "slide-$n.png"), 'PNG', 1600, 900)
  $shapes = @()
  foreach ($sh in $s.Shapes) {
    $o = [ordered]@{ id = $sh.Id; name = $sh.Name; type = $sh.Type
                     x = $sh.Left; y = $sh.Top; w = $sh.Width; h = $sh.Height; text = '' }
    if ($sh.HasTextFrame -and $sh.TextFrame.HasText) {
      $tf = $sh.TextFrame; $tr = $tf.TextRange
      $o.text = $tr.Text
      $o.wrap = $tf.WordWrap
      $o.margins = @($tf.MarginLeft, $tf.MarginTop, $tf.MarginRight, $tf.MarginBottom)
      $o.bound = @($tr.BoundLeft, $tr.BoundTop, $tr.BoundWidth, $tr.BoundHeight)
      $sizes = @(); foreach ($r in $tr.Runs()) { if ($r.Text.Trim()) { $sizes += $r.Font.Size } }
      $o.sizes = $sizes
      $lines = @(); $i = 1
      while ($i -le 60) { $ln = $tr.Lines($i, 1); if ($ln.Length -eq 0) { break }; $lines += $ln.Text; $i++ }
      $o.lines = $lines
    }
    if ($sh.HasTable) {
      $o.rows = $sh.Table.Rows.Count
    }
    $shapes += $o
  }
  $slides += [ordered]@{ index = $s.SlideIndex; png = "slide-$n.png"; shapes = $shapes
                         builds = $s.TimeLine.MainSequence.Count
                         transition = $s.SlideShowTransition.EntryEffect }
}
$doc = [ordered]@{ deck = $src; width = $pres.PageSetup.SlideWidth; height = $pres.PageSetup.SlideHeight
                   slides = $slides }
$pres.Close(); $app.Quit()
[void][Runtime.InteropServices.Marshal]::ReleaseComObject($app)
$doc | ConvertTo-Json -Depth 6 | Out-File -Encoding utf8 (Join-Path $Out 'probe.json')

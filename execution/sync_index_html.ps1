# انسخ التقرير إلى index.html في الجذر (لـ Vercel يعرض / بدون 404)
$root = Split-Path -Parent $PSScriptRoot
Copy-Item -Path (Join-Path $root "reports\azka_facebook_report.html") -Destination (Join-Path $root "index.html") -Force
Write-Host "OK: index.html updated from reports/azka_facebook_report.html"

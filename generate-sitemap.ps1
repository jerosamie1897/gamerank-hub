param(
  [Parameter(Mandatory = $false)]
  [ValidatePattern('^https://')]
  [string]$SiteUrl = 'https://gamerankhub.com'
)

$baseUrl = $SiteUrl.TrimEnd('/')
$lastModified = Get-Date -Format 'yyyy-MM-dd'
$excluded = @('search.html')
$pages = Get-ChildItem -Path $PSScriptRoot -Filter '*.html' -File -Recurse |
  Where-Object {
    $relative = [IO.Path]::GetRelativePath($PSScriptRoot, $_.FullName).Replace('\', '/')
    $excluded -notcontains $relative
  } |
  ForEach-Object {
    $relative = [IO.Path]::GetRelativePath($PSScriptRoot, $_.FullName).Replace('\', '/')
    if ($relative -eq 'index.html') { $relative = '' }
    [PSCustomObject]@{
      Url = if ($relative) { "$baseUrl/$relative" } else { "$baseUrl/" }
      Priority = if (-not $relative) { '1.0' } else { '0.8' }
    }
  }

$entries = $pages | Sort-Object Url | ForEach-Object {
  "  <url><loc>$($_.Url)</loc><lastmod>$lastModified</lastmod><priority>$($_.Priority)</priority></url>"
}

$xml = @"
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
$($entries -join "`n")
</urlset>
"@

$outputPath = Join-Path $PSScriptRoot 'sitemap.xml'
[IO.File]::WriteAllText($outputPath, $xml, [Text.UTF8Encoding]::new($false))
Write-Host "Generated $outputPath with $($pages.Count) URLs for $baseUrl"

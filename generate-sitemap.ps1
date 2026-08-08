param(
  [Parameter(Mandatory = $true)]
  [ValidatePattern('^https://')]
  [string]$SiteUrl
)

$baseUrl = $SiteUrl.TrimEnd('/')
$lastModified = Get-Date -Format 'yyyy-MM-dd'
$pages = @(
  @{ Path = '/'; Priority = '1.0' }
  @{ Path = '/best-free-games.html'; Priority = '0.9' }
  @{ Path = '/browser-games.html'; Priority = '0.9' }
  @{ Path = '/game-guides.html'; Priority = '0.9' }
  @{ Path = '/about.html'; Priority = '0.5' }
)

$entries = $pages | ForEach-Object {
  @"
  <url>
    <loc>$baseUrl$($_.Path)</loc>
    <lastmod>$lastModified</lastmod>
    <priority>$($_.Priority)</priority>
  </url>
"@
}

$xml = @"
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
$($entries -join "`n")
</urlset>
"@

$outputPath = Join-Path $PSScriptRoot 'sitemap.xml'
[System.IO.File]::WriteAllText($outputPath, $xml, [System.Text.UTF8Encoding]::new($false))
Write-Host "Generated $outputPath for $baseUrl"

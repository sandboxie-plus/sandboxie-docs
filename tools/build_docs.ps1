#Requires -Version 7.0

param(
    [Parameter(Mandatory = $true)]
    [string]$BuildRoot
)

$ErrorActionPreference = 'Stop'
$ResolvedBuildRoot = (Resolve-Path -LiteralPath $BuildRoot -ErrorAction Stop).Path
$Marker = Join-Path $ResolvedBuildRoot '.prepared-docs'
if (!(Test-Path -LiteralPath $ResolvedBuildRoot -PathType Container) -or
    !(Test-Path -LiteralPath $Marker -PathType Leaf) -or
    (Get-Content -LiteralPath $Marker -Raw).Trim() -ne 'sandboxie-docs-prepared-v1' -or
    (Test-Path -LiteralPath (Join-Path $ResolvedBuildRoot '.git'))) {
    throw 'BuildRoot must be a separate build directory created by tools/prepare_docs.py.'
}
foreach ($RequiredPath in @('mkdocs.yml', 'docs/zh', 'material')) {
    if (!(Test-Path -LiteralPath (Join-Path $ResolvedBuildRoot $RequiredPath))) {
        throw "Prepared build input is missing: $RequiredPath"
    }
}

$DirZh = 'zh'
$DirZhCn = 'zh-CN'
Push-Location -LiteralPath $ResolvedBuildRoot
try {
    python -m mkdocs build
    if ($LASTEXITCODE -ne 0) { throw "MkDocs build failed with exit code $LASTEXITCODE" }
    python -m mkdocs build --no-directory-urls --site-dir site_
    if ($LASTEXITCODE -ne 0) { throw "MkDocs build failed with exit code $LASTEXITCODE" }

    # Process HTML files in both root and /zh language folders
    $languagePaths = "", "zh"  # "" for root, "zh" for Chinese
    $contentFolders = "Content", "PlusContent"

    Write-Host "=== Starting file copy process ===" -ForegroundColor Cyan

    foreach ($lang in $languagePaths) {
        foreach ($folder in $contentFolders) {
            # Construct source and destination paths
            $sourcePath = if ($lang) { Join-Path "site_" $lang | Join-Path -ChildPath $folder }
                         else { Join-Path "site_" $folder }

            $destPath = if ($lang) { Join-Path "./site" $lang | Join-Path -ChildPath $folder }
                       else { Join-Path "./site" $folder }

            Write-Host "`nProcessing folder: $sourcePath" -ForegroundColor Yellow
            Write-Host "Destination folder: $destPath" -ForegroundColor Yellow

            # Skip if source doesn't exist
            if (!(Test-Path $sourcePath)) {
                Write-Host "Source path not found. Skipping." -ForegroundColor DarkYellow
                continue
            }

            # Get all HTML files
            $htmlFiles = Get-ChildItem -Path $sourcePath -Filter "*.html" -Recurse -File

            if ($htmlFiles.Count -eq 0) {
                Write-Host "No HTML files found." -ForegroundColor DarkYellow
                continue
            }

            Write-Host "Found $($htmlFiles.Count) HTML files to process" -ForegroundColor Green

            foreach ($file in $htmlFiles) {
                # Get relative path (e.g., "subdir/file.html") from source folder
                $relativePath = $file.FullName.Substring((Resolve-Path $sourcePath).Path.Length + 1)
                $destinationFile = Join-Path $destPath $relativePath

                Write-Host "`n[File] Source: $($file.FullName)" -ForegroundColor Gray
                Write-Host "       Destination: $destinationFile" -ForegroundColor Gray

                # Ensure destination directory exists
                $destinationDir = [System.IO.Path]::GetDirectoryName($destinationFile)
                if (!(Test-Path $destinationDir)) {
                    Write-Host "Creating directory: $destinationDir" -ForegroundColor Blue
                    New-Item -ItemType Directory -Path $destinationDir -Force | Out-Null
                }

                # Copy file
                Write-Host "Copying file..." -ForegroundColor DarkCyan
                Copy-Item -Path $file.FullName -Destination $destinationFile -Force

                if (Test-Path $destinationFile) {
                    Write-Host "Successfully copied." -ForegroundColor Green
                } else {
                    Write-Host "Failed to copy!" -ForegroundColor Red
                }
            }
        }
    }

    Write-Host "`n=== Copy process completed ===" -ForegroundColor Cyan

    # Rename target language directory to source language directory in the final site directory
    $langDirs = Get-ChildItem site -Recurse -Directory | Where-Object { $_.Name -eq "$DirZh" }
    foreach ($dir in $langDirs) {
        $newPath = Join-Path $dir.Parent.FullName "$DirZhCn"
        Rename-Item -Path $dir.FullName -NewName "$DirZhCn"
    }

    # Update references in HTML files
    $htmlFiles = Get-ChildItem site -Recurse -Filter "*.html"
    foreach ($file in $htmlFiles) {
        $content = Get-Content $file -Raw
        $updatedContent = $content -replace "/$DirZh/", "/$DirZhCn/"
        if ($content -ne $updatedContent) {
            Set-Content $file $updatedContent
        }
    }

    # # Use extra.js
    # # Process lunr language files
    # $lunrFiles = Get-ChildItem site -Recurse -Filter "lunr.zh.min.js"
    # Write-Host "Found $($lunrFiles.Count) lunr.zh.min.js files"

    # foreach ($lunrFile in $lunrFiles) {
        # $newPath = Join-Path $lunrFile.Directory.FullName "lunr.zh-CN.min.js"
        # Write-Host "Copying $($lunrFile) to $newPath"
        # Copy-Item -Path $lunrFile -Destination $newPath
    # }

    # # Use extra.js
    # # Process search_index.json files
    # $searchIndexFiles = Get-ChildItem site -Recurse -Filter "search_index.json"
    # Write-Host "Found $($searchIndexFiles.Count) search_index.json files"

    # foreach ($searchFile in $searchIndexFiles) {
        # Write-Host "Processing search index: $($searchFile)"

        # try {
            # $jsonContent = Get-Content $searchFile -Raw | ConvertFrom-Json

            # # Check and update lang array in config
            # if ($jsonContent.config -and $jsonContent.config.lang -contains $DirZh) {
                # Write-Host "Found '$DirZh' in lang array, updating to '$DirZhCn'"
                # $jsonContent.config.lang = $jsonContent.config.lang | ForEach-Object {
                    # if ($_ -eq $DirZh) { $DirZhCn } else { $_ }
                # }

                # # Convert back to JSON and save
                # $jsonContent | ConvertTo-Json -Depth 10 | Set-Content $searchFile
                # Write-Host "Successfully updated $($searchFile)"
            # } else {
                # Write-Host "No '$DirZh' found in lang array or config missing"
            # }
        # } catch {
            # Write-Host "Error processing $($searchFile): $_"
        # }
    # }

    # Process sitemap.xml files recursively
    $sitemapFiles = Get-ChildItem site -Recurse -Filter "sitemap.xml"
    Write-Host "Found $($sitemapFiles.Count) sitemap.xml files"

    foreach ($sitemap in $sitemapFiles) {
        Write-Host "Processing sitemap: $($sitemap)"

        # Update references in sitemap.xml
        $content = Get-Content $sitemap -Raw
        $updatedContent = $content -replace "/$DirZh/", "/$DirZhCn/"

        if ($content -ne $updatedContent) {
            Write-Host "Updated $DirZh→$DirZhCn references in $($sitemap)"
            $updatedContent | Set-Content $sitemap
        } else {
            Write-Host "No $DirZh→$DirZhCn references found in $($sitemap)"
        }

        # Process corresponding .gz file
        $gzPath = "$($sitemap).gz"
        if (Test-Path $gzPath) {
            Write-Host "Found existing gzip file: $gzPath - deleting it"
            Remove-Item -Force $gzPath
        }

        # Create new gzip file
        Write-Host "Creating new gzip file: $gzPath"
        $bytes = [System.Text.Encoding]::UTF8.GetBytes($updatedContent)
        $ms = New-Object System.IO.MemoryStream
        $gzip = New-Object System.IO.Compression.GZipStream($ms, [System.IO.Compression.CompressionMode]::Compress)
        $gzip.Write($bytes, 0, $bytes.Length)
        $gzip.Close()
        [System.IO.File]::WriteAllBytes($gzPath, $ms.ToArray())

        Write-Host "Successfully processed $($sitemap)"
    }

    if ($sitemapFiles.Count -eq 0) {
        Write-Warning "No sitemap.xml files found in the repository"
    }
} finally {
    Pop-Location
}

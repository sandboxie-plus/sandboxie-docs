Push-Location $PSScriptRoot/..

foreach ($file in Get-ChildItem site_ -Recurse -File) {
    $rp = Resolve-Path -Relative $file -RelativeBasePath site_
    $match_path = Join-Path "./site" $rp
    if (!(Test-Path $match_path)) {
        Copy-Item $file $match_path
    }
}

Pop-Location
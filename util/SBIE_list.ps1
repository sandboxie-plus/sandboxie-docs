Push-Location $PSScriptRoot/..
$space_len = 4
$c = Get-ChildItem "docs/Content" -Filter "SBIE*" | `
    ForEach-Object { "$( ' '*$space_len )- Content/$( $_.BaseName ).md" }
#Set-Clipboard -Value $c
Write-Output $c
Pop-Location
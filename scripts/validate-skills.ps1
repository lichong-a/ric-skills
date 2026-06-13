[CmdletBinding()]
param(
    [switch]$WarningsAsErrors,
    [switch]$Quiet
)

$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"
$RepositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Arguments = @((Join-Path $PSScriptRoot "validate-skills.py"), "--root", $RepositoryRoot)

if ($WarningsAsErrors) {
    $Arguments += "--warnings-as-errors"
}
if ($Quiet) {
    $Arguments += "--quiet"
}

& python @Arguments
exit $LASTEXITCODE

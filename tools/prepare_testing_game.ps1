param(
    [Parameter(Mandatory=$true)][string]$Build,
    [string]$Source = 'E:\SRWZ3',
    [switch]$Write
)
$ErrorActionPreference = 'Stop'
$projectRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$destination = Join-Path $projectRoot 'game'
$sourceRoot = (Resolve-Path -LiteralPath $Source).Path.TrimEnd('\')
$buildRoot = (Resolve-Path -LiteralPath $Build).Path
if (Test-Path -LiteralPath $destination) { throw 'game already exists. Use install_build.ps1 to update it safely.' }
function Assert-PlainPath([string]$Path) {
    $cursor = $Path
    while ($cursor) {
        if ((Test-Path -LiteralPath $cursor) -and
            ((Get-Item -LiteralPath $cursor -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)) {
            throw "Refusing linked path: $cursor"
        }
        $parent = Split-Path -Parent $cursor
        if ($parent -eq $cursor) { break }
        $cursor = $parent
    }
}
Assert-PlainPath $destination
Assert-PlainPath $sourceRoot
Assert-PlainPath $buildRoot
$sourceGame = Join-Path $sourceRoot 'PS3_GAME'
Assert-PlainPath $sourceGame
$discFile = Join-Path $sourceRoot 'PS3_DISC.SFB'
Assert-PlainPath $discFile
foreach ($required in @($discFile, (Join-Path $sourceGame 'PARAM.SFO'), (Join-Path $sourceGame 'USRDIR\EBOOT.BIN'))) {
    if (!(Test-Path -LiteralPath $required -PathType Leaf)) { throw "Missing disc file: $required" }
}
$sourceItems = @(Get-ChildItem -LiteralPath $sourceGame -Recurse -Force)
if ($sourceItems | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }) {
    throw 'Source game contains linked paths.'
}
$manifestPath = Join-Path $buildRoot 'build_manifest.json'
$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
if ($manifest.schema -ne 1 -or !$manifest.ui_regression_checks -or !$manifest.version) {
    throw 'Build is not validated and numbered.'
}
foreach ($entry in $manifest.files.PSObject.Properties) {
    if ([IO.Path]::GetFileName($entry.Name) -ne $entry.Name) { throw 'Unsafe manifest filename.' }
    $path = Join-Path $buildRoot $entry.Name
    Assert-PlainPath $path
    if ((Get-Item -LiteralPath $path).Length -ne $entry.Value.bytes -or
        (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash -ne $entry.Value.sha256) {
        throw "Build verification failed: $path"
    }
}
Push-Location $projectRoot
try {
    $layoutText = & python -c "import sys,json;sys.path.insert(0,'tools');from deploy import LAYOUT;print(json.dumps(LAYOUT))"
    if ($LASTEXITCODE -ne 0) { throw 'Cannot read deployment layout.' }
    $layout = $layoutText | ConvertFrom-Json
} finally { Pop-Location }
$overrides = @{}
foreach ($entry in $layout.PSObject.Properties) {
    if (!$manifest.files.PSObject.Properties[$entry.Name]) { throw "Missing build file: $($entry.Name)" }
    $target = [IO.Path]::GetFullPath((Join-Path (Join-Path $sourceGame ('USRDIR\' + $entry.Value)) $entry.Name))
    if (!$target.StartsWith($sourceGame + '\', [StringComparison]::OrdinalIgnoreCase) -or
        !(Test-Path -LiteralPath $target -PathType Leaf)) { throw "Invalid game target: $target" }
    $overrides[$target] = Join-Path $buildRoot $entry.Name
}
# Plan the entire disc tree, substituting only files from the coherent build.
$plan = @()
$files = @($sourceItems | Where-Object { !$_.PSIsContainer }) + @(Get-Item -LiteralPath $discFile)
foreach ($file in $files) {
    $sourcePath = $file.FullName
    if ($overrides.ContainsKey($sourcePath)) { $sourcePath = $overrides[$sourcePath] }
    $relative = $file.FullName.Substring($sourceRoot.Length + 1)
    $plan += [pscustomobject]@{relative=$relative; source=$sourcePath;
        sha256=(Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash}
}
Write-Output "Verified $($manifest.version): $($plan.Count) complete disc files, including $($overrides.Count) translated build files."
Write-Output "Single runnable destination: $destination"
if (!$Write) { Write-Output 'Dry run complete. Nothing changed.'; exit 0 }
New-Item -ItemType Directory -Path $destination | Out-Null
foreach ($entry in $plan) {
    $target = Join-Path $destination $entry.relative
    New-Item -ItemType Directory -Path (Split-Path -Parent $target) -Force | Out-Null
    Copy-Item -LiteralPath $entry.source -Destination $target
    if ((Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash -ne $entry.sha256) {
        throw "Copy failed verification: $target. Folder is incomplete; do not launch it."
    }
}
Copy-Item -LiteralPath $manifestPath -Destination (Join-Path $destination 'build_manifest.json')
Copy-Item -LiteralPath (Join-Path $buildRoot 'message_coverage.json') -Destination (Join-Path $destination 'message_coverage.json')
$audit = @{version=$manifest.version; game=$destination; build=$buildRoot; files=$plan;
    registration_changed=$false; complete_disc_verified=$true}
[IO.File]::WriteAllText((Join-Path $destination 'folder_audit.json'), ($audit | ConvertTo-Json -Depth 5))
Write-Output "Ready on disk: $destination ($($plan.Count) files hash-verified)."
Write-Output 'RPCS3 registration/cache have not been changed. Use install_build.ps1 with RPCS3 closed before testing.'

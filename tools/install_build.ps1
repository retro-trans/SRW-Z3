param(
    [Parameter(Mandatory=$true)][string]$Build,
    [switch]$Write
)
$ErrorActionPreference = 'Stop'
$projectRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$buildRoot = (Resolve-Path -LiteralPath $Build).Path
$gameRoot = Join-Path $projectRoot 'game\PS3_GAME'
$discRoot = Join-Path $gameRoot 'USRDIR'
$cachePath = 'E:\RPCS3\dev_hdd0\game\BLJS10256_DATA'
$registrationPath = 'E:\RPCS3\config\games.yml'
. (Join-Path $PSScriptRoot 'testing_registration.ps1')
if (Get-Process rpcs3 -ErrorAction SilentlyContinue) { throw 'Close RPCS3 before installing.' }

function Assert-PlainPath([string]$Path) {
    $cursor = $Path
    while ($cursor) {
        if (Test-Path -LiteralPath $cursor) {
            if ((Get-Item -LiteralPath $cursor -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) {
                throw "Refusing a linked path: $cursor"
            }
        }
        $parent = Split-Path -Parent $cursor
        if ($parent -eq $cursor) { break }
        $cursor = $parent
    }
}
Assert-PlainPath $gameRoot
Assert-PlainPath $cachePath
Assert-PlainPath $registrationPath
$registrationBefore = [IO.File]::ReadAllText($registrationPath)
$registrationHash = (Get-FileHash -LiteralPath $registrationPath -Algorithm SHA256).Hash
$registeredFolder = Split-Path -Parent $gameRoot
$registrationAfter = Set-TestingRegistrationText $registrationBefore $registeredFolder
$manifest = Get-Content -Raw -LiteralPath (Join-Path $buildRoot 'build_manifest.json') | ConvertFrom-Json
if ($manifest.schema -ne 1 -or !$manifest.ui_regression_checks -or !$manifest.version) {
    throw 'Build is not validated and numbered.'
}
foreach ($entry in $manifest.files.PSObject.Properties) {
    if ([IO.Path]::GetFileName($entry.Name) -ne $entry.Name) { throw 'Unsafe manifest filename.' }
    $source = Join-Path $buildRoot $entry.Name
    if ((Get-Item -LiteralPath $source).Length -ne $entry.Value.bytes -or
        (Get-FileHash -Algorithm SHA256 -LiteralPath $source).Hash -ne $entry.Value.sha256) {
        throw "Build verification failed: $source"
    }
}
# The canonical deployment layout, imported read-only from this repository.
Push-Location $projectRoot
try {
    $layoutText = & python -c "import sys,json;sys.path.insert(0,'tools');from deploy import LAYOUT;print(json.dumps(LAYOUT))"
    if ($LASTEXITCODE -ne 0) { throw 'Cannot read deployment layout.' }
    $layout = $layoutText | ConvertFrom-Json
} finally { Pop-Location }
$targets = @()
foreach ($entry in $layout.PSObject.Properties) {
    if (!$manifest.files.PSObject.Properties[$entry.Name]) { throw "Manifest omits $($entry.Name)" }
    $target = [IO.Path]::GetFullPath((Join-Path (Join-Path $discRoot $entry.Value) $entry.Name))
    if (!$target.StartsWith($gameRoot + '\', [StringComparison]::OrdinalIgnoreCase)) {
        throw "Target outside game directory: $target"
    }
    Assert-PlainPath $target
    if (!(Test-Path -LiteralPath $target -PathType Leaf)) { throw "Missing installed target: $target" }
    $targets += [pscustomobject]@{
        name = $entry.Name; source = (Join-Path $buildRoot $entry.Name); target = $target
        relative = $target.Substring($gameRoot.Length + 1)
        before = (Get-FileHash -Algorithm SHA256 -LiteralPath $target).Hash
        after = $manifest.files.PSObject.Properties[$entry.Name].Value.sha256
    }
}
if (Test-Path -LiteralPath $cachePath) {
    if ((Resolve-Path -LiteralPath $cachePath).Path -ne 'E:\RPCS3\dev_hdd0\game\BLJS10256_DATA') {
        throw 'Unexpected cache target.'
    }
    if (Get-ChildItem -LiteralPath $cachePath -Recurse -Force |
        Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }) {
        throw 'Install cache contains a linked path.'
    }
}
function Save-Hashes {
    $result = @{}
    foreach ($userDir in Get-ChildItem -LiteralPath 'E:\RPCS3\dev_hdd0\home' -Directory) {
        $saves = Join-Path $userDir.FullName 'savedata'
        if (Test-Path -LiteralPath $saves) {
            foreach ($file in Get-ChildItem -LiteralPath $saves -File -Recurse) {
                $result[$file.FullName] = (Get-FileHash -Algorithm SHA256 -LiteralPath $file.FullName).Hash
            }
        }
    }
    return $result
}
$saveBefore = Save-Hashes
# Keep the single-folder receipt consistent with the installed build too.
$metadataNames = @('build_manifest.json','message_coverage.json','folder_audit.json','README.txt')
$metadataBefore = @{}
foreach ($name in $metadataNames) {
    $path = Join-Path $registeredFolder $name
    Assert-PlainPath $path
    $metadataBefore[$name] = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash
}
$folderAudit = Get-Content -LiteralPath (Join-Path $registeredFolder 'folder_audit.json') -Raw | ConvertFrom-Json
if (!$folderAudit.complete_disc_verified -or !$folderAudit.files) { throw 'Missing complete folder audit.' }
Write-Output "Verified build $($manifest.version): $($targets.Count) exact game-file targets; $($saveBefore.Count) save files protected."
Write-Output "Cache refresh target: $cachePath (move to backup, not delete)."
Write-Output "RPCS3 BLJS10256 will use: $registeredFolder (other games unchanged)."
if (!$Write) { Write-Output 'Dry run complete. No installed files changed.'; exit 0 }
if (Get-Process rpcs3 -ErrorAction SilentlyContinue) { throw 'RPCS3 started during preflight; close it.' }
$backupRoot = Join-Path $projectRoot ('work\install_backups\' + $manifest.version + '_' + (Get-Date -Format 'yyyyMMdd_HHmmss'))
Assert-PlainPath $backupRoot
if (Test-Path -LiteralPath $backupRoot) { throw 'Backup destination already exists.' }
New-Item -ItemType Directory -Path $backupRoot | Out-Null
New-Item -ItemType Directory -Path (Join-Path $backupRoot 'metadata') | Out-Null
foreach ($name in $metadataNames) {
    $path = Join-Path $registeredFolder $name
    $backup = Join-Path (Join-Path $backupRoot 'metadata') $name
    Copy-Item -LiteralPath $path -Destination $backup
    if ((Get-FileHash -LiteralPath $backup -Algorithm SHA256).Hash -ne $metadataBefore[$name]) { throw "Metadata backup mismatch: $name" }
}
Copy-Item -LiteralPath $registrationPath -Destination (Join-Path $backupRoot 'games.yml')
if ((Get-FileHash -LiteralPath (Join-Path $backupRoot 'games.yml') -Algorithm SHA256).Hash -ne $registrationHash) {
    throw 'Registration changed during backup; nothing installed.'
}
# Back up every target before changing any installed file.
foreach ($entry in $targets) {
    $backup = Join-Path (Join-Path $backupRoot 'PS3_GAME') $entry.relative
    New-Item -ItemType Directory -Path (Split-Path -Parent $backup) -Force | Out-Null
    Copy-Item -LiteralPath $entry.target -Destination $backup
    if ((Get-FileHash -Algorithm SHA256 -LiteralPath $backup).Hash -ne $entry.before) {
        throw "Backup mismatch: $backup"
    }
}
$cacheMoved = $false
$registrationWritten = $false
try {
    if (Get-Process rpcs3 -ErrorAction SilentlyContinue) { throw 'RPCS3 started during backup; close it.' }
    foreach ($entry in $targets) {
        Copy-Item -LiteralPath $entry.source -Destination $entry.target -Force
        if ((Get-FileHash -Algorithm SHA256 -LiteralPath $entry.target).Hash -ne $entry.after) {
            throw "Installed hash mismatch: $($entry.target)"
        }
    }
    if (Test-Path -LiteralPath $cachePath) {
        # Both absolute targets were validated above; saves live elsewhere.
        Move-Item -LiteralPath $cachePath -Destination (Join-Path $backupRoot 'BLJS10256_DATA')
        $cacheMoved = $true
    }
    if ((Get-FileHash -LiteralPath $registrationPath -Algorithm SHA256).Hash -ne $registrationHash) {
        throw 'Registration changed during installation.'
    }
    $registrationWritten = $true
    [IO.File]::WriteAllText($registrationPath, $registrationAfter, (New-Object Text.UTF8Encoding($false)))
    if ([IO.File]::ReadAllText($registrationPath) -cne $registrationAfter) { throw 'Registration verification failed.' }
    $saveAfter = Save-Hashes
    if ($saveBefore.Count -ne $saveAfter.Count) { throw 'Save-file inventory changed during install.' }
    foreach ($path in $saveBefore.Keys) {
        if ($saveBefore[$path] -ne $saveAfter[$path]) { throw "Save hash changed: $path" }
    }
    $expected = @{}
    foreach ($entry in $targets) { $expected[$entry.target] = $entry }
    foreach ($entry in $folderAudit.files) {
        $path = [IO.Path]::GetFullPath((Join-Path $registeredFolder $entry.relative))
        if (!$path.StartsWith($registeredFolder + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Unsafe folder-audit path.' }
        Assert-PlainPath $path
        if ($expected.ContainsKey($path)) {
            $entry.sha256 = $expected[$path].after
            $entry.source = $expected[$path].source
        }
        if ((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash -ne $entry.sha256) { throw "Complete-disc verification failed: $path" }
    }
    $folderAudit.version = $manifest.version
    $folderAudit.build = $buildRoot
    $folderAudit.registration_changed = $true
    foreach ($name in @('build_manifest.json','message_coverage.json')) {
        $source = Join-Path $buildRoot $name
        $target = Join-Path $registeredFolder $name
        Copy-Item -LiteralPath $source -Destination $target -Force
        if ((Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash -ne (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash) { throw "Metadata copy mismatch: $name" }
    }
    [IO.File]::WriteAllText((Join-Path $registeredFolder 'folder_audit.json'), ($folderAudit | ConvertTo-Json -Depth 5))
    $readme = "Super Robot Wars Z3 - Time Prison`r`nCombined local version $($manifest.version)`r`n`r`nSingle runnable game folder: $registeredFolder`r`nRPCS3 BLJS10256 registration points here; launch this folder, not an older ISO.`r`n`r`nTranslation is partial. See build_manifest.json and message_coverage.json.`r`nAll $($folderAudit.files.Count) disc files were hash-verified, including $($targets.Count) translated outputs.`r`nSaves are unchanged. Older files and cache are backed up in:`r`n$backupRoot`r`n"
    [IO.File]::WriteAllText((Join-Path $registeredFolder 'README.txt'), $readme)
} catch {
    foreach ($name in $metadataNames) {
        Copy-Item -LiteralPath (Join-Path (Join-Path $backupRoot 'metadata') $name) -Destination (Join-Path $registeredFolder $name) -Force
        if ((Get-FileHash -LiteralPath (Join-Path $registeredFolder $name) -Algorithm SHA256).Hash -ne $metadataBefore[$name]) { throw "Metadata rollback failed: $name" }
    }
    if ($registrationWritten) {
        Copy-Item -LiteralPath (Join-Path $backupRoot 'games.yml') -Destination $registrationPath -Force
        if ((Get-FileHash -LiteralPath $registrationPath -Algorithm SHA256).Hash -ne $registrationHash) {
            throw "Registration rollback failed. Backup: $backupRoot"
        }
    }
    foreach ($entry in $targets) {
        Copy-Item -LiteralPath (Join-Path (Join-Path $backupRoot 'PS3_GAME') $entry.relative) -Destination $entry.target -Force
        if ((Get-FileHash -Algorithm SHA256 -LiteralPath $entry.target).Hash -ne $entry.before) {
            throw "Rollback failed: $($entry.target). Backup: $backupRoot"
        }
    }
    if ($cacheMoved -and !(Test-Path -LiteralPath $cachePath)) {
        Move-Item -LiteralPath (Join-Path $backupRoot 'BLJS10256_DATA') -Destination $cachePath
    }
    throw
}
$audit = @{version=$manifest.version; build=$buildRoot; game=$gameRoot; backup=$backupRoot;
           registered_folder=$registeredFolder; registration_verified=$true;
           cache_moved=$cacheMoved; save_files_unchanged=$saveBefore.Count; files=$targets}
[IO.File]::WriteAllText((Join-Path $backupRoot 'install_audit.json'), ($audit | ConvertTo-Json -Depth 5))
Write-Output "Installed $($manifest.version): all $($targets.Count) game hashes match; saves unchanged."
Write-Output "Backup: $backupRoot"
Write-Output 'The game will recreate its install cache on next launch.'

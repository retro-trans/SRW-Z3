$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'testing_registration.ps1')
$other = 'BLJS10299: E:/Projects/SRW Z3 2/work/tengoku/game-ui-0.1.0/'
foreach ($newline in @("`r`n", "`n")) {
    $before = "# registered games${newline}BLJS10256: E:/old.iso${newline}$other${newline}"
    $after = Set-TestingRegistrationText $before 'E:\Projects\SRW Z3\game'
    $expected = "# registered games${newline}BLJS10256: 'E:/Projects/SRW Z3/game/'${newline}$other${newline}"
    if ($after -cne $expected) { throw 'Incorrect replacement or unrelated registration/line ending changed.' }
    if ((Set-TestingRegistrationText $after 'E:\Projects\SRW Z3\game') -cne $after) { throw 'Not idempotent.' }
}
foreach ($invalid in @($other, "BLJS10256: a`nBLJS10256: b")) {
    $rejected = $false
    try { $null = Set-TestingRegistrationText $invalid 'E:\Projects\SRW Z3\game' } catch { $rejected = $true }
    if (!$rejected) { throw 'Missing/duplicate target was accepted.' }
}
foreach ($script in @('prepare_testing_game.ps1', 'install_build.ps1', 'testing_registration.ps1')) {
    $parseErrors = $null
    $tokens = $null
    $null = [Management.Automation.Language.Parser]::ParseFile((Join-Path $PSScriptRoot $script), [ref]$tokens, [ref]$parseErrors)
    if ($parseErrors.Count) { throw ($parseErrors | Out-String) }
}
Write-Output 'PASS: CRLF/LF preservation, other-game preservation, idempotence, missing/duplicate rejection, script syntax.'

# Pure transformation: preserve every other registration and line ending.
function Set-TestingRegistrationText([string]$Text, [string]$Folder) {
    $pattern = '(?m)^BLJS10256:[^\r\n]*'
    if ([regex]::Matches($Text, $pattern).Count -ne 1) {
        throw 'Expected exactly one BLJS10256 game registration.'
    }
    $path = $Folder.Replace('\', '/').TrimEnd('/') + '/'
    if ($path -match "['\r\n]") { throw 'Unsupported registration path.' }
    $replacement = "BLJS10256: '$path'"
    return [regex]::Replace($Text, $pattern, [System.Text.RegularExpressions.MatchEvaluator]{param($match) $replacement})
}

Write-Host "Copying OneCore TTS voices to legacy SAPI registry..."

$source = "HKLM:\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens"
$destination = "HKLM:\SOFTWARE\Microsoft\SPEECH\Voices\Tokens"

Get-ChildItem -Path $source | ForEach-Object {
    ${name} = $_.PSChildName
    $srcPath = $_.PsPath
    $destPath = Join-Path $destination ${name}

    try {
        Write-Host "Copying voice: ${name}"
        Copy-Item -Path $srcPath -Destination $destPath -Recurse -Force
        Write-Host "Successfully copied: ${name}"
    } catch {
        Write-Host "Failed to copy ${name}: ${_}" -ForegroundColor Red
    }
}

Write-Host "`nAll done. Please restart any apps using SAPI (e.g., Python) to see new voices."
Read-Host -Prompt "Press Enter to exit"

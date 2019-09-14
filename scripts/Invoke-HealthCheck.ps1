#
# Invoke-HealthCheck.ps1
#
# Run multiple commands to ensure basic features are working well.
#

$commands = @(
    "--help",
    "",
    "--formats csv,html,json"
)

$sum = 0
foreach ($c in $commands) {
    $command = "`npipenv run python reportmix.py $c"
    Write-Host -ForegroundColor Cyan "$command"
    Invoke-Expression "pipenv run python reportmix.py $c"
    $sum += if (!$? -or $LASTEXITCODE -gt 0) { 1 } else { 0 }
}

if ($sum -gt 0) {
    Write-Host -ForegroundColor Red "$sum commands failed!"
    exit 1
} else {
    Write-Host -ForegroundColor Green "Success!"
}

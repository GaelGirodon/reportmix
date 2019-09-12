#
# Invoke-HealthCheck.ps1
#
# Run multiple commands to ensure basic features are working well.
#

$commands = @(
    "--help",
    "",
    "--format csv",
    "--format html",
    "--format json"
)

$sum = 0
foreach ($c in $commands) {
    $command = "`npipenv run python reportmix.py $c"
    Write-Host -ForegroundColor Cyan "$command"
    Invoke-Expression "pipenv run python reportmix.py $c"
    $sum += if ($?) { 0 } else { 1 }
}

if ($sum -gt 0) {
    Write-Host -ForegroundColor Red "$sum commands failed!"
    exit 1
} else {
    Write-Host -ForegroundColor Green "Success!"
}

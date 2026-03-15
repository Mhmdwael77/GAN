
param(
    [string]$ImageName = "myapp",
    [int]$WaitSeconds = 120
)

function Wait-ForDockerEngine {
    param([int]$TimeoutSeconds = 120)
    $start = Get-Date
    while (-not (Test-Path '\\.\pipe\docker_engine')) {
        if ((Get-Date) - $start -gt (New-TimeSpan -Seconds $TimeoutSeconds)) {
            return $false
        }
        Start-Sleep -Seconds 2
    }
    return $true
}

Write-Host "Checking docker engine..."
if (Test-Path '\\.\pipe\docker_engine') {
    Write-Host "Docker engine pipe found."
} else {
    Write-Host "Docker engine pipe not found. Attempting to start Docker Desktop..."
    $dockerExe = 'C:\Program Files\Docker\Docker\Docker Desktop.exe'
    if (Test-Path $dockerExe) {
        Start-Process -FilePath $dockerExe -WindowStyle Hidden
        Write-Host "Started Docker Desktop (if installed). Waiting up to $WaitSeconds seconds for the engine..."
        if (-not (Wait-ForDockerEngine -TimeoutSeconds $WaitSeconds)) {
            Write-Error "Docker engine did not become available within $WaitSeconds seconds. Start Docker Desktop manually and try again."
            exit 1
        }
        Write-Host "Docker engine is available."
    } else {
        Write-Error "Docker Desktop not found at '$dockerExe'. Install Docker Desktop and try again: https://www.docker.com/get-started"
        exit 1
    }
}

Write-Host "Building Docker image '$ImageName'..."
$build = docker build -t $ImageName .
if ($LASTEXITCODE -ne 0) {
    Write-Error "docker build failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}

Write-Host "Running container from image '$ImageName'..."
docker run --rm -it $ImageName
exit $LASTEXITCODE

param(
    [string]$Message = "",
    [switch]$NoPush,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

function Run-Git {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$GitArgs
    )

    if ($DryRun) {
        Write-Host "[dry-run] git $($GitArgs -join ' ')"
        return
    }

    & git @GitArgs
    if ($LASTEXITCODE -ne 0) {
        throw "Git command failed: git $($GitArgs -join ' ')"
    }
}

try {
    git rev-parse --is-inside-work-tree *> $null
    if ($LASTEXITCODE -ne 0) {
        throw "This folder is not a Git repository."
    }

    $branch = (& git branch --show-current).Trim()
    if ([string]::IsNullOrWhiteSpace($branch)) {
        throw "Cannot detect current Git branch."
    }

    $changes = & git status --porcelain
    if (-not $changes) {
        Write-Host "No changes to sync."
        exit 0
    }

    if ([string]::IsNullOrWhiteSpace($Message)) {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
        $Message = "Sync project changes $timestamp"
    }

    Write-Host "Current branch: $branch"
    Write-Host "Commit message: $Message"
    Write-Host ""
    git status --short
    Write-Host ""

    Run-Git -GitArgs @("add", "-A")

    if (-not $DryRun) {
        git diff --cached --quiet
        if ($LASTEXITCODE -eq 0) {
            Write-Host "No staged changes to commit."
            exit 0
        }
    }

    Run-Git -GitArgs @("commit", "-m", $Message)

    if ($NoPush) {
        Write-Host "Committed locally. Push skipped because -NoPush was used."
        exit 0
    }

    Run-Git -GitArgs @("push", "-u", "origin", $branch)

    if ($DryRun) {
        Write-Host "Dry run complete. No files were changed."
    }
    else {
        Write-Host "Sync complete."
    }
}
catch {
    Write-Error $_
    exit 1
}

<#
.SYNOPSIS
    Imports bookmarks into Microsoft Edge by modifying the Bookmarks JSON file.

.DESCRIPTION
    This script reads an existing Edge bookmarks file, adds new bookmarks, and saves it.
    Works for both Edge Stable and Edge Beta (adjust $edgeProfilePath if needed).

.NOTES
    - Close all Edge windows before running this script.
    - Backup your existing Bookmarks file before making changes.

.SOURCE
	From copilot

#>

# Path to Edge's Default profile Bookmarks file
$edgeProfilePath = "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Bookmarks"

# Path to backup file
$backupPath = "$edgeProfilePath.bak"

# Example bookmarks to add
$newBookmarks = @(
    @{ name = "Outlook Mail"; url = "https://outlook.live.com/mail/0/" },
    @{ name = "Yahoo Mail"; url = "https://mail.yahoo.com/n/inbox/" },
    @{ name = "MSN Mail"; url = "https://outlook.live.com/mail/0/" },
    @{ name = "iCloud Mail"; url = "https://www.icloud.com/mail" },
    @{ name = "Hotmail"; url = "https://outlook.live.com/mail/0/" },
    @{ name = "Google GMail"; url = "https://mail.google.com/mail/u/0/#inbox" }
)

try {
    # Ensure Edge is closed
    Get-Process msedge -ErrorAction SilentlyContinue | Stop-Process -Force

    # Backup existing bookmarks
    if (Test-Path $edgeProfilePath) {
        Copy-Item $edgeProfilePath $backupPath -Force
    } else {
        throw "Edge bookmarks file not found at $edgeProfilePath"
    }

    # Read and parse existing bookmarks JSON
    $bookmarksJson = Get-Content $edgeProfilePath -Raw | ConvertFrom-Json

    # Navigate to the "bookmark_bar" children array
    $bookmarkBar = $bookmarksJson.roots.bookmark_bar.children

    # Add new bookmarks if they don't already exist
    foreach ($bm in $newBookmarks) {
        if (-not ($bookmarkBar | Where-Object { $_.url -eq $bm.url })) {
            $bookmarkBar += [PSCustomObject]@{
                date_added = (Get-Date).ToFileTimeUtc().ToString()
                guid       = [guid]::NewGuid().ToString()
                id         = (Get-Random -Minimum 1000 -Maximum 9999).ToString()
                name       = $bm.name
                type       = "url"
                url        = $bm.url
            }
        }
    }

    # Save updated JSON back to file
    $bookmarksJson.roots.bookmark_bar.children = $bookmarkBar
    $bookmarksJson | ConvertTo-Json -Depth 10 | Set-Content $edgeProfilePath -Encoding UTF8

    Write-Host "Bookmarks imported successfully. Restart Edge to see changes." -ForegroundColor Green
}
catch {
    Write-Error "Error: $_"
}

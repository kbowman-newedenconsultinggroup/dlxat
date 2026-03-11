# --- CONFIGURATION ---
$folderName = "Public Libraries"
$bookmarksToAdd = @(
    @{ name = "Olathe"; url = "https://www.olathelibrary.org/" },
    @{ name = "Leavenworth"; url = "https://leavenworthpubliclibrary.org/" },
    @{ name = "Kansas City KS"; url = "https://kckpl.org" },
    @{ name = "Johnson County"; url = "https://www.jocolibrary.org/" }
)
$profileName = "Default"  # Change to "Profile 1" etc. if needed

# --- CLOSE EDGE ---
Write-Host "Closing Microsoft Edge..."
Get-Process msedge -ErrorAction SilentlyContinue | Stop-Process -Force

# --- PATHS ---
$edgeProfilePath = Join-Path $env:LOCALAPPDATA "Microsoft\Edge\User Data\$profileName"
$bookmarksFile = Join-Path $edgeProfilePath "Bookmarks"

if (-not (Test-Path $bookmarksFile)) {
    Write-Error "Bookmarks file not found at: $bookmarksFile"
    exit 1
}

# --- BACKUP ---
$backupFile = "$bookmarksFile.bak_$(Get-Date -Format 'yyyyMMddHHmmss')"
Copy-Item $bookmarksFile $backupFile -Force
Write-Host "Backup created at $backupFile"

# --- LOAD JSON ---
$json = Get-Content $bookmarksFile -Raw | ConvertFrom-Json

# --- FIND BOOKMARK BAR ---
$bookmarkBar = $json.roots.bookmark_bar

# --- FIND OR CREATE FOLDER ---
$folder = $bookmarkBar.children | Where-Object { $_.type -eq "folder" -and $_.name -eq $folderName }
if (-not $folder) {
    $folder = [PSCustomObject]@{
        type       = "folder"
        name       = $folderName
        children   = @()
        date_added = ([string]([DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds() * 1000))
        id         = ([string](Get-Random -Minimum 100000 -Maximum 999999))
    }
    $bookmarkBar.children += $folder
    Write-Host "Created folder '$folderName'"
}

# --- ADD BOOKMARKS ---
foreach ($bm in $bookmarksToAdd) {
    if (-not ($folder.children | Where-Object { $_.url -eq $bm.url })) {
        $newBookmark = [PSCustomObject]@{
            type       = "url"
            name       = $bm.name
            url        = $bm.url
            date_added = ([string]([DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds() * 1000))
            id         = ([string](Get-Random -Minimum 100000 -Maximum 999999))
        }
        $folder.children += $newBookmark
        Write-Host "Added bookmark '$($bm.name)'"
    } else {
        Write-Host "Bookmark '$($bm.name)' already exists in '$folderName'"
    }
}

# --- SAVE JSON ---
$json | ConvertTo-Json -Depth 10 | Set-Content $bookmarksFile -Encoding UTF8

# --- RESTART EDGE ---
Write-Host "Starting Microsoft Edge..."
Start-Process "msedge.exe"

Write-Host "✅ Bookmarks imported successfully into folder '$folderName'."

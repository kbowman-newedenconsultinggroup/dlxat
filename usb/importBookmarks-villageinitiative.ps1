# --- CONFIGURATION ---
$folderName = "Village Initiative"
$bookmarksToAdd = @(
  @{ name = "The Village Initiative"; url = "https://villageinitiativeinc.com},
  @{ name = "Care Beyond The Boulevard"; url = "https://www.carebeyondtheboulevard.org},
  @{ name = "CDC Correctional Health"; url = "https://www.cdc.gov/correctional-health/reentry/index.html},
  @{ name = "Decarcerate KC"; url = "https://www.decarceratekc.org/about},
  @{ name = "DBT Skills from Experts"; url = "https://www.youtube.com/@DBTRU},
  @{ name = "Great jobs KC"; url = "https://greatjobskc.org/empowering-kansas-citys-workforce-with-education/},
  @{ name = "Heartland Regional Alcohol & Drug Assessment Center"; url = "https://www.hradac.com},
  @{ name = "Johnson County Mental Health"; url = "https://www.jocogov.org/department/mental-health},
  @{ name = "Kansas City Alcoholics Anonymous"; url = "https://kc-aa.org},
  @{ name = "Kansas City Kansas Community College"; url = "https://www.kckcc.edu},
  @{ name = "Kansas Department For Children & Families (Benefits Assistance, Child Support)"; url = "https://www.dcf.ks.gov/Pages/default.aspx},
  @{ name = "Kansas City Narcotics Anonymous"; url = "https://www.kansascityna.org/meetings/},
  @{ name = "Kansas Department of Revenue (Driver’s License, Real ID, and Tax Assistance) "; url = "https://www.ksrevenue.gov/index.html},
  @{ name = "Kansas Housing Resource Corporation"; url = "https://kshousingcorp.org},
  @{ name = "KC Common Good"; url = "https://kccommongood.org},
  @{ name = "Revolve KC (Earn-a-Bike Program)"; url = "https://www.revolvekc.org/earn-a-bike},
  @{ name = "Ride KC (Regional Transit) https://ridekc.org},
  @{ name = "Social Security"; url = "https://www.ssa.gov},
  @{ name = "Trauma Informed Care Implementation Recourse Center"; url = "https://www.traumainformedcare.chcs.org/what-is-trauma-informed-care/},
  @{ name = "Vibrant Health"; url = "https://vibranthealthkc.org},
  @{ name = "VitalChek (ordering birth certificate)"; url = "https://www.vitalchek.com/v/},
  @{ name = "Workforce Partnership"; url = "https://workforcepartnership.com},
  @{ name = "Wyandotte Behavior Health Network"; url = "https://www.wyandotbhn.org}
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

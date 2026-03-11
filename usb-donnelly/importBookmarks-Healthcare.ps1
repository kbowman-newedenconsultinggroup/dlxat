# --- CONFIGURATION ---
$folderName = "Health Provider Portals"
$bookmarksToAdd = @(
    @{ name = "Swope Health"; url = "https://mycw38.eclinicalweb.com/portal4264/jsp/100mp/login_otp.jsp" },
    @{ name = "KC Care Health Center"; url = "https://mycw131.ecwcloud.com/portal18286/jsp/jspnew/selfWebEnable_new.jsp" },
    @{ name = "Samual Rodgers Health Center"; url = "https://pxpportal.nextgen.com/samuelurodgershealthcenter-25051/portal/#/user/login?returnUrl=%2Fdashboard" },
    @{ name = "University Health myUHealth"; url = "https://tmcmed.consumeridp.us-1.healtheintent.com/saml2/sso/login?authenticationRequestId=9344f6db-328e-4b79-b69f-8c248fcf906a" },
    @{ name = "HCA Midwest MyHealthOne"; url = "https://myhealthone.com/mh1/public/mh1/Login/#/login-form" },
    @{ name = "mySaintLuke&#39;s"; url = "https://mysaintlukes.corp.saint-lukes.org/MyChartPRD/Authentication/Login?" },
    @{ name = "MyChildrensMercy"; url = "https://accounts.mychildrensmercy.org/saml2/sso/login?authenticationRequestId=ba931657-da60-4271-9e57-9a70e897993b" },
    @{ name = "University of Kansas Medical"; url = "https://mychart.kansashealthsystem.com/MyChart/Authentication/Login?" },
    @{ name = "ArchWell"; url = "https://mycw149.ecwcloud.com/portal20971/jsp/100mp/login_otp.jsp" },
    @{ name = "Health Partnership Clinic"; url = "https://mycw90.ecwcloud.com/portal12011/jsp/100mp/login_otp.jsp" },
    @{ name = "Hope Family Care"; url = "https://mycw46.eclinicalweb.com/portal5399/jsp/100mp/login_otp.jsp" },
    @{ name = "NKC Health"; url = "https://northkansascityhospital.consumeridp.us-1.healtheintent.com/saml2/sso/login?authenticationRequestId=dbced4d2-b4fe-4b88-8bbe-45d1239da899" },
    @{ name = "Olathe Health"; url = "https://olathehealth.consumeridp.us-1.healtheintent.com/saml2/sso/login?authenticationRequestId=47ac5271-ec96-4a5f-a115-a379cfefe924" },
    @{ name = "St Joseph"; url = "https://mychart.primehealthcare.com/MyChart/Authentication/Login" },
    @{ name = "Veterans Affairs"; url = "https://www.va.gov/sign-in/?application=mhv&to=home&oauth=false" },
    @{ name = "Vibrant Health"; url = "https://mycw31.eclinicalweb.com/portal3287/jsp/100mp/login_otp.jsp" }
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

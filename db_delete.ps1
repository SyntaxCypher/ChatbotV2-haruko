$fileToDelete = "E:\Code-Repo-2\Project Haruko\chat_history.db"

# Check if the file exists
if (Test-Path $fileToDelete) {
    # Delete the file
    Remove-Item $fileToDelete -Force
 Write-Host "" 
 Write-Host ""
    Write-Host "**************************************************"
    Write-Host "Haruko Memory Database has been successfully wiped"
    Write-Host "**************************************************"
 Write-Host ""
 Write-Host ""
} else {
 Write-Host ""
 Write-Host ""
    Write-Host "************************************************"
    Write-Host "Haruko Memory Database has been already be wiped"
    Write-Host "************************************************"
 Write-Host ""
 Write-Host ""
}

exit
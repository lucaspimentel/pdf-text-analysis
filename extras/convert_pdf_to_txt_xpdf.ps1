param (
    [Parameter(Mandatory)]
    [ValidateScript( { Test-Path $_ -PathType 'Container' })]
    [string]$inputDirectory,

    [Parameter(Mandatory)]
    [string]$outputDirectory
)

$ErrorActionPreference = 'Stop'

# Validate that the output directory exists or create it if it doesn't exist
if (-not (Test-Path $outputDirectory -PathType 'Container')) {
    Write-Host "The output directory '$outputDirectory' does not exist. Creating it..."
    New-Item -ItemType Directory -Path $outputDirectory
}

# Convert to absolute paths
$inputDirectory = Resolve-Path $inputDirectory
$outputDirectory = Resolve-Path $outputDirectory

# Validate that the input directory exists
if (-not (Test-Path $inputDirectory)) {
    Write-Host "Error: The input directory '$inputDirectory' does not exist."
    exit 1
}

# Specify the path to pdftotext.exe
$pdftotextPath = "${env:USERPROFILE}\\Downloads\\xpdf-tools-win-4.05\\bin64\\pdftotext.exe"

# Loop through each PDF file in the input directory
Get-ChildItem -Path $inputDirectory -Filter "*.pdf" | ForEach-Object {
    $pdfFile = $_.FullName
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($_.Name)

    # Construct the output .txt file path
    $txtFile = Join-Path $outputDirectory "$baseName.txt"

    # Call pdftotext.exe to convert the PDF to text
    & $pdftotextPath -nopgbrk -raw -enc 'UTF-8' $pdfFile $txtFile

    # Output status
    Write-Host "Converted $pdfFile to $txtFile"
}

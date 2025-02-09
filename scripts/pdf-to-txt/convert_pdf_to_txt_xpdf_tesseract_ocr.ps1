param(
    [Parameter(Mandatory = $true)]
    [string]$PdfPath,
    
    [Parameter(Mandatory = $true)]
    [string]$OutputTxtPath
)

# 1. Create a temporary folder to hold PNG files and intermediate text
$tempFolder = Join-Path $env:TEMP ("OCR_" + [System.IO.Path]::GetRandomFileName())
New-Item -ItemType Directory -Path $tempFolder | Out-Null

try {
    # 2. Convert the PDF to PNG pages (Xpdf’s pdftopng must be in your PATH)
    pdftopng $PdfPath (Join-Path $tempFolder 'page')

    # 3. Run Tesseract OCR on each PNG
    $pngFiles = Get-ChildItem -Path $tempFolder -Filter 'page*.png' | Sort-Object Name
    foreach ($png in $pngFiles) {
        # Output text file will use the PNG's base name
        $outBase = Join-Path $tempFolder $png.BaseName
        tesseract $png.FullName $outBase | Out-Null
    }

    # 4. Concatenate all text files
    $txtFiles = Get-ChildItem -Path $tempFolder -Filter 'page*.txt' | Sort-Object Name
    $txtFiles | ForEach-Object {
        Get-Content $_.FullName
    } | Out-File $OutputTxtPath -Encoding UTF8
}
finally {
    # 5. Clean up temporary folder (comment out if you want to inspect files)
    Remove-Item $tempFolder -Recurse -Force
}

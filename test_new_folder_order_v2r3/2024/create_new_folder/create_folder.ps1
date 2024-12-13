# �������� ��������� ANSI-������ � PowerShell
$Host.UI.RawUI.WindowTitle = "Python Script Runner"
if ($PSVersionTable.PSVersion.Major -ge 7) {
    $PSStyle.OutputRendering = 'ANSI'
} else {
    # ��� ����� ������ ������ PowerShell
    $null = [Console]::BufferWidth
}

# ����� Python � ��������� ������
$pythonPaths = @(
    "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python312\python.exe",
    "C:\Program Files\Python312\python.exe"
)

$pythonExe = $null

# ��������� ������ ����
foreach ($path in $pythonPaths) {
    if (Test-Path $path) {
        $pythonExe = $path
        break
    }
}

if ($pythonExe -eq $null) {
    Write-Host "Python �� ������ � ����������� ������ ���������!" -ForegroundColor Red
    Write-Host "����������, ���������� Python ��� ������� ���������� ����." -ForegroundColor Yellow
    exit 1
}

try {
    Write-Host "������ Python: $pythonExe" -ForegroundColor Green
    Write-Host "������ �������..." -ForegroundColor Green
    
    # ������������� ���������� ��������� ��� Python, ����������� ��� �� � PowerShell
    $env:PYTHONUNBUFFERED = "1"
    $env:FORCE_COLOR = "1"
    
    # ������ Python-�������
    & $pythonExe new_folder_order_v2.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n������ ������� �������� ������" -ForegroundColor Green
    }
    else {
        Write-Host "`n������ ���������� � ������� (���: $LASTEXITCODE)" -ForegroundColor Red
    }
}
catch {
    Write-Host "`n��������� ������ ��� ���������� �������:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}
finally {
    Write-Host "`n������� ����� ������� ��� ������..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}
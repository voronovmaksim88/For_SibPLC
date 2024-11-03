# Включаем поддержку ANSI-цветов в PowerShell
$Host.UI.RawUI.WindowTitle = "Python Script Runner"
if ($PSVersionTable.PSVersion.Major -ge 7) {
    $PSStyle.OutputRendering = 'ANSI'
} else {
    # Для более старых версий PowerShell
    $null = [Console]::BufferWidth
}

# Поиск Python в различных местах
$pythonPaths = @(
    "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python312\python.exe",
    "C:\Program Files\Python312\python.exe"
)

$pythonExe = $null

# Проверяем каждый путь
foreach ($path in $pythonPaths) {
    if (Test-Path $path) {
        $pythonExe = $path
        break
    }
}

if ($pythonExe -eq $null) {
    Write-Host "Python не найден в стандартных местах установки!" -ForegroundColor Red
    Write-Host "Пожалуйста, установите Python или укажите правильный путь." -ForegroundColor Yellow
    exit 1
}

try {
    Write-Host "Найден Python: $pythonExe" -ForegroundColor Green
    Write-Host "Запуск скрипта..." -ForegroundColor Green
    
    # Устанавливаем переменную окружения для Python, указывающую что мы в PowerShell
    $env:PYTHONUNBUFFERED = "1"
    $env:FORCE_COLOR = "1"
    
    # Запуск Python-скрипта
    & $pythonExe new_folder_order_v2.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`nСкрипт успешно завершил работу" -ForegroundColor Green
    }
    else {
        Write-Host "`nСкрипт завершился с ошибкой (код: $LASTEXITCODE)" -ForegroundColor Red
    }
}
catch {
    Write-Host "`nПроизошла ошибка при выполнении скрипта:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}
finally {
    Write-Host "`nНажмите любую клавишу для выхода..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}
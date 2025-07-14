@echo off
chcp 65001 > nul
echo -------------------------------------------
echo LIMPEZA DE PROJETO DJANGO
echo -------------------------------------------
echo Este script irá:
echo - Apagar o banco de dados "db.sqlite3"
echo - Remover todas as pastas "__pycache__"
echo - Excluir arquivos ".pyc"
echo - Apagar a pasta "staticfiles"
echo.

set /p CONFIRMA="Tem certeza que deseja continuar? (s/n): "
if /i not "%CONFIRMA%"=="s" (
    echo ❌ Operação cancelada pelo usuário.
    pause
    exit /b
)

echo.
echo ▶ Removendo banco de dados SQLite...
if exist db.sqlite3 (
    del /f /q db.sqlite3
    echo ✅ Banco de dados "db.sqlite3" removido.
) else (
    echo ⚠️ Banco de dados "db.sqlite3" não encontrado.
)

echo ▶ Removendo arquivos __pycache__ e *.pyc...
for /d /r %%i in (__pycache__) do (
    rd /s /q "%%i"
)
for /r %%f in (*.pyc) do (
    del /f /q "%%f"
)
echo ✅ Caches Python removidos.

echo ▶ Removendo pasta "staticfiles"...
if exist staticfiles (
    rd /s /q staticfiles
    echo ✅ Pasta "staticfiles" removida.
) else (
    echo ⚠️ Pasta "staticfiles" não encontrada.
)

echo.
echo 🧹 Limpeza finalizada com sucesso!
pause

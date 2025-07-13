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
echo - Remover arquivos de migração (exceto __init__.py)
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

echo ▶ Removendo arquivos de migração (exceto __init__.py)...
for /d %%d in (core\migrations alunos\migrations avaliacao\migrations exercicio\migrations treino\migrations organizacao\migrations) do (
    if exist %%d (
        for %%f in (%%d\*.py) do (
            if not "%%~nxf"=="__init__.py" (
                del /f /q "%%f"
                echo Removido: %%f
            )
        )
    )
)
echo ✅ Arquivos de migração removidos.

echo.
echo 🧹 Limpeza finalizada com sucesso!
echo.
echo ▶ Criando novas migrações...
python manage.py makemigrations core alunos avaliacao exercicios treinos organizacao || goto :erro
echo ✅ Novas migrações criadas.

echo.
echo ▶ Aplicando migrações...
python manage.py migrate || goto :erro
echo ✅ Migrações aplicadas.

echo.
echo ▶ Coletando arquivos estáticos...
if not exist staticfiles mkdir staticfiles
python manage.py collectstatic --noinput || goto :erro
echo ✅ Arquivos estáticos coletados.

echo.
echo 🚀 Projeto resetado e pronto para uso!
pause
exit /b

:erro
echo.
echo ❌ Ocorreu um erro durante a execução dos comandos.
pause
exit /b 1
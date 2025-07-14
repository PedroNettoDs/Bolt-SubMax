@echo off
chcp 65001 > nul

echo -------------------------------------------
echo Iniciando as migrações do Django...
echo -------------------------------------------

echo ▶ Etapa 1: Migrando app "Pages"
python manage.py migrate Pages || goto :erro

echo ▶ Etapa 2: Migrando banco de dados padrão
python manage.py migrate || goto :erro

echo ▶ Etapa 3: Criando migrações do app "Pages"
python manage.py makemigrations Pages || goto :erro

echo ▶ Etapa 4: Criando migrações gerais
python manage.py makemigrations || goto :erro

echo ▶ Etapa 5: Coletando arquivos estáticos
if not exist staticfiles mkdir staticfiles
python manage.py collectstatic --noinput || goto :erro

echo.
echo ✅ Todas as operações foram concluídas com sucesso!
pause
exit /b

:erro
echo.
echo ❌ Ocorreu um erro durante a execução dos comandos.
pause
exit /b 1

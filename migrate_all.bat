@echo off
chcp 65001 > nul

echo -------------------------------------------
echo Iniciando as migrações do Django...
echo -------------------------------------------

echo ▶ Etapa 1: Migrando app "core"
python manage.py migrate core || goto :erro

echo ▶ Etapa 2: Migrando app "Alunos"
python manage.py migrate alunos || goto :erro

echo ▶ Etapa 3: Migrando app "Avaliacao"
python manage.py migrate avaliacao || goto :erro

echo ▶ Etapa 3: Migrando app "agendas"
python manage.py migrate agendas || goto :erro

echo ▶ Etapa 4: Migrando app "Exercicios"
python manage.py migrate exercicios || goto :erro

echo ▶ Etapa 5: Migrando app "Treinos"
python manage.py migrate treinos || goto :erro

echo ▶ Etapa 6: Migrando app "Organizacao"
python manage.py migrate organizacao || goto :erro

echo ▶ Etapa 7: Migrando banco de dados padrão
python manage.py migrate || goto :erro

echo ▶ Etapa 8: Criando migrações para todos os apps
python manage.py makemigrations core alunos avaliacao exercicios treinos organizacao || goto :erro

echo ▶ Etapa 9: Coletando arquivos estáticos
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
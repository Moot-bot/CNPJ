#!/bin/bash
# startup.sh

echo "🔄 Rodando migrações..."
python manage.py migrate --noinput

echo "📦 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "🚀 Iniciando Gunicorn..."
exec gunicorn consulta_cnpj.wsgi:application
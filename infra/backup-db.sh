#!/bin/bash

# Configurações
CONTAINER_NAME="saas_locadora_postgres_1"
DB_USER="locadora"
DB_NAME="saas_locadora"
BACKUP_DIR="./backups"
DATE=$(date +"%Y%m%d_%H%M%S")
FILENAME="$BACKUP_DIR/backup_$DATE.sql.gz"

# Cria o diretório se não existir
mkdir -p "$BACKUP_DIR"

# Executa o dump dentro do container e compacta
echo "Iniciando backup do banco de dados..."
docker exec -t $CONTAINER_NAME pg_dump -U $DB_USER $DB_NAME | gzip > $FILENAME

if [ $? -eq 0 ]; then
    echo "Backup finalizado com sucesso: $FILENAME"
else
    echo "Erro ao gerar backup"
    exit 1
fi

# Remove backups com mais de 7 dias para evitar disco cheio
find "$BACKUP_DIR" -type f -name "*.sql.gz" -mtime +7 -exec rm {} \;
echo "Limpeza de backups antigos concluída."

#!/bin/bash
set -e

# Use the psql command to execute the GRANT using variables
psql -v ON_ERROR_STOP=1 --username "$DB_USER" --dbname "$DB_NAME" <<-EOSQL
    GRANT CREATE ON DATABASE "$DB_NAME" TO "$DB_USER";
EOSQL
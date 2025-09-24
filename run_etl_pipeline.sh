#!/usr/bin/env bash
set -euo pipefail

# config  
NETWORK_NAME="etl-net"
PG_CONTAINER="postgres-etl"
PG_VOLUME="pgdata_etl"
PG_IMAGE="postgres:13"   
DB_NAME="etl_data"
DB_USER="postgres"
DB_PASS="damilare"
ETL_IMAGE="etl-image:latest"
RAW_DIR="$(pwd)/raw_files"

# 1) create network (if missing)
if ! docker network ls --format '{{.Name}}' | grep -q "^${NETWORK_NAME}$"; then
  docker network create "${NETWORK_NAME}"
  echo "Created network ${NETWORK_NAME}"
fi

# 2) create named volume (if missing)
if ! docker volume ls --format '{{.Name}}' | grep -q "^${PG_VOLUME}$"; then
  docker volume create "${PG_VOLUME}"
  echo "Created volume ${PG_VOLUME}"
fi

# 3) start Postgres container (detached)
# If a container with that name exists, stop and remove it first (safe for dev)
if docker ps -a --format '{{.Names}}' | grep -q "^${PG_CONTAINER}$"; then
  docker rm -f "${PG_CONTAINER}"
fi

docker run -d \
  --name "${PG_CONTAINER}" \
  --network "${NETWORK_NAME}" \
  -e POSTGRES_DB="${DB_NAME}" \
  -e POSTGRES_USER="${DB_USER}" \
  -e POSTGRES_PASSWORD="${DB_PASS}" \
  -v "${PG_VOLUME}":/var/lib/postgresql/data \
  "${PG_IMAGE}"

echo "Postgres container started (${PG_CONTAINER})"

# 4) Wait until Postgres reports ready
echo "Waiting for Postgres to be ready..."
until docker exec "${PG_CONTAINER}" pg_isready -U "${DB_USER}" >/dev/null 2>&1; do
  printf '.'
  sleep 1
done
echo
echo "Postgres ready."

# 5) Build ETL image
docker build -t "${ETL_IMAGE}" .
echo "Built ETL image ${ETL_IMAGE}"

 
mkdir -p "${RAW_DIR}"

# 6) Run the ETL container 
docker run --rm \
  --name etl-run \
  --network "${NETWORK_NAME}" \
  -e DB_HOST="${PG_CONTAINER}" \
  -e DB_PORT="5432" \
  -e DB_NAME="${DB_NAME}" \
  -e DB_USER="${DB_USER}" \
  -e DB_PASS="${DB_PASS}" \
  -v "${RAW_DIR}":/app/raw_files \
  "${ETL_IMAGE}"

echo "ETL run finished (check Postgres or logs for details)."

 
docker exec -it "${PG_CONTAINER}" psql -U "${DB_USER}" -d "${DB_NAME}" -c "SELECT COUNT(*) FROM SECURE_STARTUPS;"

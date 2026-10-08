#!/bin/sh
# Start one search engine at a time on 127.0.0.1, run engine_bakeoff.py against it, stop it.
# Binaries come from the vendors' public container images (extracted with skopeo and tar, never run as containers):
#   getmeili/meilisearch:v1.54.3, typesense/typesense:30.2, opensearchproject/opensearch:3.9.0
# Usage: ENGINE_ROOT=/path/with/rootfs_meili,rootfs_ts,rootfs_os PY=/path/to/venv/python ./run_engines.sh meilisearch|typesense|opensearch
set -eu
cd "$(dirname "$0")"
ENGINE_ROOT=${ENGINE_ROOT:?set ENGINE_ROOT}
PY=${PY:-python3}
DOCS=${DOCS:-1000000}
WORK=${WORK:-$ENGINE_ROOT/work}
mkdir -p "$WORK"
case "$1" in
meilisearch)
  R=$ENGINE_ROOT/rootfs_meili
  mkdir -p "$WORK/meili"
  "$R/lib/ld-musl-x86_64.so.1" --library-path "$R/lib:$R/usr/lib" "$R/bin/meilisearch" --db-path "$WORK/meili/data" --http-addr 127.0.0.1:7700 \
      --no-analytics --env development --max-indexing-memory 3GiB > "$WORK/meili.log" 2>&1 &
  PID=$!; DATA="$WORK/meili/data"; until curl -s 127.0.0.1:7700/health >/dev/null; do sleep 1; done ;;
typesense)
  mkdir -p "$WORK/ts"
  "$ENGINE_ROOT/rootfs_ts/opt/typesense-server" --data-dir "$WORK/ts" --api-key=bench --api-address 127.0.0.1 --api-port 8108 > "$WORK/ts.log" 2>&1 &
  PID=$!; DATA="$WORK/ts"; until curl -s 127.0.0.1:8108/health | grep -q ok; do sleep 1; done ;;
opensearch)
  # OpenSearch refuses to run as root; the postgres OS user is used on this sandbox. Copy the install to a writable place first.
  OSH="$WORK/os"; [ -d "$OSH" ] || { mkdir -p "$OSH"; cp -a "$ENGINE_ROOT/rootfs_os/usr/share/opensearch/." "$OSH/"; chown -R postgres:postgres "$OSH"; }
  cat > "$OSH/config/opensearch.yml" <<YML
cluster.name: bench
node.name: n1
network.host: 127.0.0.1
http.port: 9200
discovery.type: single-node
plugins.security.disabled: true
node.store.allow_mmap: false
bootstrap.memory_lock: false
YML
  chown postgres:postgres "$OSH/config/opensearch.yml"
  su postgres -s /bin/sh -c "cd $OSH && OPENSEARCH_JAVA_HOME=$OSH/jdk OPENSEARCH_JAVA_OPTS='-Xms3g -Xmx3g' DISABLE_INSTALL_DEMO_CONFIG=true DISABLE_SECURITY_PLUGIN=true ./bin/opensearch" > "$WORK/os.log" 2>&1 &
  until curl -s 127.0.0.1:9200 >/dev/null; do sleep 2; done
  PID=$(pgrep -f "org.opensearch.bootstrap.OpenSearch" | head -1); DATA="$OSH/data" ;;
*) echo "unknown engine"; exit 1 ;;
esac
$PY engine_bakeoff.py --engine "$1" --docs "$DOCS" --pid "$PID" --data-dir "$DATA"
kill "$PID" 2>/dev/null || true
sleep 3

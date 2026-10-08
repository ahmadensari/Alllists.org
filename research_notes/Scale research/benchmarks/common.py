"""Shared helpers for the hot-path benchmarks (note 06). Only touches databases whose name starts with bench_.

Usage from a script:  from common import connect, admin, make_db, drop_db, pctl
Environment: PGPASSWORD / POSTGRES_* as already set in the sandbox (role alllists, localhost:5432).
"""

import os
import statistics
import time

import psycopg

HOST = os.environ.get("POSTGRES_HOST", "localhost")
PORT = int(os.environ.get("POSTGRES_PORT", "5432"))
USER = os.environ.get("POSTGRES_USER", "alllists")
PASSWORD = os.environ.get("POSTGRES_PASSWORD", "alllists")


def _check(name):
    # Safety rail: refuse any database that is not a scratch database.
    if not name.startswith("bench_"):
        raise SystemExit(f"refusing to touch database {name!r}: only bench_* is allowed")


def connect(dbname, autocommit=True, host=None, port=None, **kw):
    _check(dbname)
    return psycopg.connect(
        host=host or HOST, port=port or PORT, user=USER, password=PASSWORD, dbname=dbname, autocommit=autocommit, **kw
    )


def admin(host=None, port=None):
    """Connection to the maintenance database used only to CREATE/DROP bench_ databases."""
    return psycopg.connect(
        host=host or HOST, port=port or PORT, user=USER, password=PASSWORD, dbname="postgres", autocommit=True
    )


def make_db(name, host=None, port=None):
    _check(name)
    with admin(host, port) as c:
        c.execute(f'DROP DATABASE IF EXISTS "{name}" WITH (FORCE)')
        c.execute(f'CREATE DATABASE "{name}"')


def drop_db(name, host=None, port=None):
    _check(name)
    with admin(host, port) as c:
        c.execute(f'DROP DATABASE IF EXISTS "{name}" WITH (FORCE)')


def pctl(values, p):
    if not values:
        return float("nan")
    s = sorted(values)
    return s[min(len(s) - 1, int(round(p / 100 * (len(s) - 1))))]


def summary(label, lat_s, wall_s, n=None):
    n = n if n is not None else len(lat_s)
    return (
        f"{label}: n={n} wall={wall_s:.2f}s rate={n / wall_s:,.0f}/s "
        f"p50={pctl(lat_s, 50) * 1000:.2f}ms p95={pctl(lat_s, 95) * 1000:.2f}ms p99={pctl(lat_s, 99) * 1000:.2f}ms"
    )


class Timer:
    def __enter__(self):
        self.t = time.perf_counter()
        return self

    def __exit__(self, *a):
        self.s = time.perf_counter() - self.t


__all__ = ["connect", "admin", "make_db", "drop_db", "pctl", "summary", "Timer", "statistics"]

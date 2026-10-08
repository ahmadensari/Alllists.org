-- Run once as the database owner (psql). Passwords come from the secret store, never from this file.
--   psql -v app_pw="'...'" -v ro_pw="'...'" -f deploy/db_roles.sql alllists
-- Then, after every deploy that migrates:  python manage.py db_roles --apply   (as the owner)
CREATE ROLE alllists_app LOGIN PASSWORD :app_pw NOSUPERUSER NOCREATEDB NOCREATEROLE;
CREATE ROLE alllists_readonly LOGIN PASSWORD :ro_pw NOSUPERUSER NOCREATEDB NOCREATEROLE;
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT CONNECT ON DATABASE alllists TO alllists_app, alllists_readonly;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS unaccent;

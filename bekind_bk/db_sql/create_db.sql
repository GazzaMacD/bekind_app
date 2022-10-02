CREATE DATABASE name_db;
CREATE USER u_name WITH PASSWORD 'some password';
ALTER ROLE u_name SET client_encoding TO 'utf8';
ALTER ROLE u_name SET default_transaction_isolation TO 'read committed';
ALTER ROLE u_name SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE name_db TO u_name;
ALTER USER u_name WITH CREATEDB;
/* add uuid-ossp module for uuid support */
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
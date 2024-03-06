-- Create the 'hh_db' database (manually check if it exists first)
-- DROP DATABASE IF EXISTS hh_db;
CREATE DATABASE hh2_db;

-- Create the 'hh_dev' user (manually check if it exists first)
CREATE USER hh2_dev WITH PASSWORD 'HolbiTeam2024*';

-- Grant all privileges on the 'hh_db' database to 'hh_dev'
GRANT ALL PRIVILEGES ON DATABASE hh2_db TO hh2_dev;
GRANT ALL PRIVILEGES ON SCHEMA public TO hh2_dev;

-- Connect to the database where you want to apply the following settings
\c hh2_db

-- Grant SELECT on all future tables in the 'public' schema to 'hh_dev'
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO hh2_dev;

-- This command grants SELECT on all existing tables in the 'public' schema to 'hh2_dev'
-- Note: This needs to be executed in the 'hh_db' database context
GRANT SELECT ON ALL TABLES IN SCHEMA public TO hh2_dev;

-- Reminder: To make sure the above commands work as expected,
-- you might need to execute them while connected to the specific database
-- where you want these privileges to apply, especially for the GRANT commands
-- on existing tables and setting default privileges.


-- Create the 'hh_db' database (manually check if it exists first)
-- DROP DATABASE IF EXISTS hh_db;
CREATE DATABASE hh3_db;

-- Create the 'hh_dev' user (manually check if it exists first)
CREATE USER hh3_dev WITH PASSWORD 'HolbiTeam2024*';

-- Grant all privileges on the 'hh_db' database to 'hh_dev'
GRANT ALL PRIVILEGES ON DATABASE hh2_db TO hh3_dev;
GRANT ALL PRIVILEGES ON SCHEMA public TO hh3_dev;

-- Connect to the database where you want to apply the following settings
\c hh2_db

-- Grant SELECT on all future tables in the 'public' schema to 'hh_dev'
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO hh3_dev;

-- This command grants SELECT on all existing tables in the 'public' schema to 'hh3_dev'
-- Note: This needs to be executed in the 'hh_db' database context
GRANT SELECT ON ALL TABLES IN SCHEMA public TO hh3_dev;

-- Reminder: To make sure the above commands work as expected,
-- you might need to execute them while connected to the specific database
-- where you want these privileges to apply, especially for the GRANT commands
-- on existing tables and setting default privileges.

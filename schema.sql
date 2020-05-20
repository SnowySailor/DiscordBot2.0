DO $$
BEGIN
-- Terminate all connections
IF EXISTS (SELECT 1 FROM pg_database WHERE datname = 'WAIFUBOT') THEN
    REVOKE CONNECT ON DATABASE WAIFUBOT FROM public;
    PERFORM pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'WAIFUBOT';
END IF;
END$$ LANGUAGE plpgsql;

-- Drop and recreate database/schema
DROP DATABASE IF EXISTS WAIFUBOT;
CREATE DATABASE WAIFUBOT WITH OWNER = 'root' ENCODING = 'UTF8';
\connect waifubot;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE message (
    id bigint primary key,
    channel_id bigint not null,
    server_id bigint not null,
    data text not null,
    word_count int not null,
    deleted boolean not null default false,
    digested boolean not null default false
);

CREATE UNIQUE INDEX ON message (server_id, channel_id, id);
CREATE UNIQUE INDEX ON message (id, channel_id, server_id);
CREATE UNIQUE INDEX ON message (id, deleted);
CREATE INDEX ON message (server_id, word_count, digested);

CREATE TABLE markov_grouping (
    message_id bigint not null references message(id),
    digested_text text not null,
    original_text text not null,
    is_message_start boolean not null
);
CREATE INDEX ON markov_grouping(message_id, digested_text) INCLUDE (original_text);
CREATE INDEX ON markov_grouping(is_message_start);

CREATE TABLE loaded_channel (
    channel_id bigint not null primary key
);
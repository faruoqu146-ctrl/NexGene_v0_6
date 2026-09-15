-- NexGene initial schema
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(320) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    display_name VARCHAR(120),
    date_of_birth VARCHAR(10),
    sex_at_birth VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS observation_types (
    id SERIAL PRIMARY KEY,
    code VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    unit VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS observations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    observation_type_id INTEGER NOT NULL REFERENCES observation_types(id),
    numeric_value DOUBLE PRECISION,
    text_value TEXT,
    boolean_value BOOLEAN,
    recorded_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_observations_user ON observations(user_id);
CREATE INDEX IF NOT EXISTS idx_observations_recorded ON observations(recorded_at);

-- Seed common observation types
INSERT INTO observation_types (code, name, unit) VALUES
    ('sleep_duration', 'Sleep duration', 'hours'),
    ('sleep_quality', 'Sleep quality', '1-10'),
    ('energy', 'Energy', '1-10'),
    ('mood', 'Mood', '1-10'),
    ('stress', 'Stress', '1-10'),
    ('exercise_minutes', 'Exercise', 'minutes'),
    ('symptoms', 'Symptoms', NULL)
ON CONFLICT (code) DO NOTHING;

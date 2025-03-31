-- Create a table to store page hits
CREATE TABLE IF NOT EXISTS hits (
    id SERIAL PRIMARY KEY,
    count INTEGER NOT NULL
);

-- Initialize the counter
INSERT INTO hits (count) VALUES (0) ON CONFLICT DO NOTHING;


PRAGMA foreign_keys = ON;

-- Insert users
INSERT INTO users (username, hashed_password, caffeine, last_observed) VALUES
('janedoe', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 180, NULL);

-- Insert drinks
INSERT INTO drinks (user_id, title, caffeine, created_at) VALUES
(1, 'Espresso Shot', 90, DATE('now', '-1 day') || ' 00:00:00'),
(1, 'Cold Brew', 150, DATE('now', '-1 day') || ' 00:00:00'),
(1, 'Green Tea', 45, DATE('now', '-1 day') || ' 00:00:00');
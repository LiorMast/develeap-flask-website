-- MySQL Database Dump for Flask Chat Application
-- Create Database
CREATE DATABASE IF NOT EXISTS chatdb;
USE chatdb;

-- Create Messages Table
CREATE TABLE IF NOT EXISTS messages (
    msg_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    room VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    msg TEXT NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=1;
-- Insert Sample Data
INSERT INTO messages (username, room, timestamp, msg) VALUES 
    ('admin', 'general', '2026-02-25 10:00:00', 'Welcome to the general chat room!'),
    ('user1', 'general', '2026-02-25 10:05:30', 'Hello everyone!'),
    ('user2', 'random', '2026-02-25 10:10:15', 'Random thoughts here...'),
    ('admin', 'support', '2026-02-25 10:15:45', 'How can I help you today?');

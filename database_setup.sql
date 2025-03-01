
-- Create the database
CREATE DATABASE IF NOT EXISTS securefile;

-- Use the database
USE securefile;

-- Create users table
CREATE TABLE IF NOT EXISTS userdata (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(12) NOT NULL,
    last_name VARCHAR(12) NOT NULL,
    email_address VARCHAR(50) UNIQUE NOT NULL,
    phone_number VARCHAR(10) UNIQUE NOT NULL,
    password VARCHAR(64) NOT NULL
);

-- Create file storage table
CREATE TABLE IF NOT EXISTS filestorage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    time DATETIME NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES userdata(id)
);

-- Create indexes for better performance
CREATE INDEX idx_email ON userdata(email_address);
CREATE INDEX idx_phone ON userdata(phone_number);
CREATE INDEX idx_user_files ON filestorage(user_id);

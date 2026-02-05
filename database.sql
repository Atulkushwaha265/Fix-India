-- =====================================================
-- NearFix Database Schema
-- All-in-One Local Service Booking System
-- Database: MySQL
-- =====================================================

-- Create Database
CREATE DATABASE IF NOT EXISTS nearfix;
USE nearfix;

-- =====================================================
-- SERVICES TABLE (must be created first)
-- =====================================================
CREATE TABLE services (
    service_id INT AUTO_INCREMENT PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- USERS TABLE
-- =====================================================
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- HELPERS TABLE
-- =====================================================
CREATE TABLE helpers (
    helper_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    service_type_id INT,
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    is_available BOOLEAN DEFAULT TRUE,
    is_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (service_type_id) REFERENCES services(service_id)
);

-- =====================================================
-- SERVICE REQUESTS TABLE (CORE BUSINESS LOGIC)
-- =====================================================
CREATE TABLE service_requests (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    helper_id INT,
    service_type_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    user_latitude DECIMAL(10,8),
    user_longitude DECIMAL(11,8),
    user_address TEXT,

    status ENUM(
        'pending',
        'accepted',
        'in_progress',
        'work_done_by_helper',
        'completed',
        'cancelled'
    ) DEFAULT 'pending',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (helper_id) REFERENCES helpers(helper_id),
    FOREIGN KEY (service_type_id) REFERENCES services(service_id)
);

-- =====================================================
-- PAYMENTS TABLE
-- =====================================================
CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    request_id INT NOT NULL,
    user_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    gateway_payment_id VARCHAR(255),
    status ENUM('pending','success','failed') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (request_id) REFERENCES service_requests(request_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- =====================================================
-- ADMINS TABLE
-- =====================================================
CREATE TABLE admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- DEFAULT DATA
-- =====================================================

-- Insert default services
INSERT INTO services (service_name, description) VALUES
('Plumber', 'Fixing pipes, leaks, drainage issues'),
('Electrician', 'Electrical repairs, wiring, appliance installation'),
('Car Mechanic', 'Car repair and maintenance services'),
('Bike Mechanic', 'Bike repair and maintenance services'),
('AC Repair', 'Air conditioner repair and maintenance'),
('Carpenter', 'Woodwork, furniture repair'),
('Painter', 'Painting services for walls and furniture'),
('Cleaning', 'Home and office cleaning services');

-- Insert default admin (password should be hashed in real app)
INSERT INTO admins (username, email, password, full_name) VALUES
('admin', 'admin@nearfix.com', 'admin123', 'System Administrator');

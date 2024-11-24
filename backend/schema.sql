CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) DEFAULT 'creator', -- Roles: admin, creator, subscriber
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE lists (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    creator_id INT REFERENCES users(id),
    parent_list_id INT REFERENCES lists(id), -- For hierarchical merging
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_public BOOLEAN DEFAULT TRUE
);

CREATE TABLE list_entries (
    id SERIAL PRIMARY KEY,
    list_id INT REFERENCES lists(id),
    entry_name VARCHAR(100) NOT NULL,
    entry_description TEXT,
    contact_info JSONB, -- Stores phone, email, social links
    location VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    list_id INT REFERENCES lists(id),
    amount DECIMAL(10, 2) NOT NULL,
    transaction_type VARCHAR(50), -- e.g., "list_purchase", "subscription"
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE revenue_sharing (
    id SERIAL PRIMARY KEY,
    list_id INT REFERENCES lists(id),
    creator_id INT REFERENCES users(id),
    platform_share DECIMAL(10, 2) NOT NULL,
    creator_share DECIMAL(10, 2) NOT NULL,
    total_earnings DECIMAL(10, 2) NOT NULL,
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE subscriptions (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    subscription_type VARCHAR(50), -- e.g., "individual", "business"
    start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_date TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    action VARCHAR(100),
    target_table VARCHAR(50),
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

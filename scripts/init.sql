CREATE TABLE IF NOT EXISTS audited_invoices (
    id SERIAL PRIMARY KEY,
    vendor_name VARCHAR(255),
    tax_id VARCHAR(50),
    total_amount DECIMAL(12, 2),
    currency VARCHAR(10),
    approval_status VARCHAR(50),
    approver_comments TEXT,
    processed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    raw_response_json JSONB
);

ALTER TABLE audited_invoices
ADD CONSTRAINT check_currency CHECK (currency IS NOT NULL AND currency <> '');

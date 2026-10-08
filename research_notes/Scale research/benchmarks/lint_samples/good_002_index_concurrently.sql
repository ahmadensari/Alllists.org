-- GOOD: one statement per file, no transaction, so CONCURRENTLY is allowed
CREATE INDEX CONCURRENTLY IF NOT EXISTS entries_entry_website_idx ON entries_entry (website);

-- GOOD: expand step. Run with lock_timeout set; index concurrently outside the transaction; constraints NOT VALID then VALIDATE.
SET lock_timeout = '5s';
ALTER TABLE entries_entry ADD COLUMN depth smallint;
ALTER TABLE entries_entry ADD CONSTRAINT entry_ck CHECK (length(name) > 0) NOT VALID;
ALTER TABLE entries_contact ADD CONSTRAINT contact_entry_fk FOREIGN KEY (entry_id) REFERENCES entries_entry (id) NOT VALID;

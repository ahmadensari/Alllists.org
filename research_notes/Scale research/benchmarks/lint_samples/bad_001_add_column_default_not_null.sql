-- BAD: plain index on an existing big table (blocks writes), NOT NULL column added with a default in one step,
-- type change (rewrite), FK without NOT VALID, rename, drop column
BEGIN;
CREATE INDEX entries_entry_website_idx ON entries_entry (website);
ALTER TABLE entries_entry ADD COLUMN depth smallint NOT NULL DEFAULT 0;
ALTER TABLE entries_entry ALTER COLUMN year_established TYPE integer;
ALTER TABLE entries_contact ADD CONSTRAINT contact_entry_fk FOREIGN KEY (entry_id) REFERENCES entries_entry (id);
ALTER TABLE entries_entry ALTER COLUMN name_fold SET NOT NULL;
ALTER TABLE entries_entry RENAME COLUMN website TO site_url;
ALTER TABLE entries_entry DROP COLUMN description;
ALTER TABLE entries_entry ADD CONSTRAINT entry_ck CHECK (length(name) > 0);
ALTER TABLE entries_entry ADD CONSTRAINT entry_uniq UNIQUE (uid, country_code);
COMMIT;

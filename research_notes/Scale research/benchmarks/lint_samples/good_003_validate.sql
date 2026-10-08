-- GOOD: contract step after the backfill is complete
ALTER TABLE entries_entry VALIDATE CONSTRAINT entry_ck;
ALTER TABLE entries_contact VALIDATE CONSTRAINT contact_entry_fk;
ALTER TABLE entries_entry ADD CONSTRAINT depth_nn CHECK (depth IS NOT NULL) NOT VALID;
ALTER TABLE entries_entry VALIDATE CONSTRAINT depth_nn;
ALTER TABLE entries_entry ALTER COLUMN depth SET NOT NULL;
ALTER TABLE entries_entry DROP CONSTRAINT depth_nn;

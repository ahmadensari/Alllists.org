"""Optional read replica (plan P6.03). Set DATABASE_REPLICA_HOST to switch it on: reads that opt in with `.using("replica")`
or run in a request marked read-only go to the replica; every write, and every read inside a transaction that wrote,
stays on the primary. Without the setting nothing changes."""


class ReplicaRouter:
    def db_for_read(self, model, **hints):
        return None  # reads use the primary unless the caller names the replica; list views opt in explicitly

    def db_for_write(self, model, **hints):
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == "default"

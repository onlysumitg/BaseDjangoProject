# https://docs.djangoproject.com/en/3.2/topics/db/multi-db/#database-routers
class DBRouter:
    def db_for_read(self, model, **hints):
        by_table = self.get_db_by_table_name(str(model.__name__))
        if by_table:
            return by_table


        return None

    def db_for_write(self, model, **hints):
        by_table = self.get_db_by_table_name(str(model.__name__))
        if by_table:
            return by_table

        """
        if model._meta.app_label in self.route_app_labels:
            return 'users_db'
        """
        return None


    def allow_migrate(self, db, app_label, model_name=None, **hints):
        is_pci_model = str(model_name).upper().startswith("PCI")
        is_pci_db = str(db).lower() == "pci"
        if is_pci_db and not is_pci_model:
            return False

        if is_pci_model and not is_pci_db:
            return False

        if is_pci_db and is_pci_model:
            return True
         
        return None   


    

    def get_db_by_table_name(self,model_name):
        if str(model_name).upper().startswith("PCI_"):
            return "pci"
        return None
from main import Main


class SharePoint(Main):
    
    def __init__(self, email, password, endpoint, type):
        Main.__init__(self, email, password, endpoint, type)


    def create_team_website_sharepoint(self, title : str, is_public = False):
        conn = self.auth()
        
        try:
            conn.create_team_site(alias = {title}, title = {title}, is_public = is_public)
            print("Création avec succès !!!")
            return True

        except:
            print("Erreur de création !!!")
            return False


    def create_communication_website_sharepoint(self, title : str):
        conn = self.auth()
        
        try:
            conn.create_communication_site(alias = {title}, title = {title})
            print("Création avec succès !!!")
            return True

        except:
            print("Erreur de création !!!")
            return False

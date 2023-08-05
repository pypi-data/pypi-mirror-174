from main import Main


class OneDrive(Main):
    
    def __init__(self, email, password, endpoint, type):
        Main.__init__(self, email, password, endpoint, type)

    
    #SHARE FOLDER
    def share_folder(self, folder_name : str = "", is_edit = False):
        conn = self.auth()
        result = conn.web.create_anonymous_link(conn, url=f"Documents/{folder_name}", is_edit_link = is_edit).execute_query()

        return result.value
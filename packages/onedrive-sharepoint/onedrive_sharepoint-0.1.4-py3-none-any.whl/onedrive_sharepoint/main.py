import os
from datetime import datetime
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
from office365.runtime.client_request_exception import ClientRequestException


root_started = [
    {"type" : "onedrive", "root": "Documents"},
    {"type" : "sharepoint", "root" : "Documents partages"}
]
    

class Main:

    def __init__(self, email : str, password : str, endpoint : str, type : str):
        self.email = email
        self.password = password
        self.endpoint = endpoint
        self.type = type

    
    def __root(self):
        return [item["root"] for item in root_started if item["type"].lower() == self.type.lower()][0]


    # CONNECT USER
    def auth(self):

        return ClientContext(self.endpoint).with_credentials(
            UserCredential(
                user_name = self.email, 
                password = self.password
            )
        )



    # CREATE FOLDER
    def create_folder(self, folder_name):
        if folder_name:
            conn = self.auth()
            root = self.__root()
            conn.web.folders.add(f'{root}/{folder_name}').execute_query()

            return f"Création avec succès de {root}/{folder_name} !!!"

        print("Aucun dossier !!!")
        return False



    # GET ALL FOLDERS FROM ROOT OR ON A FOLDER_NAME
    def get_folders(self, folder_name : str = ""):

        conn = self.auth()
        root = self.__root()

        folders = conn.web.get_folder_by_server_relative_url(f"{root}/{folder_name}").folders
        conn.load(folders).execute_query()

        return folders



    # GET FILES FROM FOLDER
    def get_files(self, folder_name : str = ""):

        conn = self.auth()
        root = self.__root()

        files = conn.web.get_folder_by_server_relative_url(f"{root}/{folder_name}").files
        conn.load(files).execute_query()

        return files

    

    # DOWNLOAD FILE BY URL
    def download_file(self, file_url : str):
        conn = self.auth()
        filename = file_url.split("/")[-1]
        dir_name =  f"./{ datetime.now().strftime('%d-%m-%Y') }-datas"

        try:
            os.mkdir(dir_name)
        except FileExistsError:
            pass

        path_file = os.path.abspath( os.path.join(dir_name, filename) )
        
        with open(path_file, "wb") as local_file:
            file = conn.web.get_file_by_server_relative_url(file_url)
            file.download(local_file)
            conn.execute_query()

        print(f"Fichier { filename } téléchargé avec succès !")


    
    # DOWNLOAD FILES FROM FOLDER
    def download_files_from_folder(self, folder_name : str = ""):
    
        files = self.get_files(folder_name)

        if len(files) > 0:
            [self.download_file(file.serverRelativeUrl) for file in files]
            return True

        else:
            print("Aucun Fichier téléchargé !!! Vérifiez le nom du dossier.")
            return False



    # CHECK FOLDER EXIST    
    def check_exist_folder(self, folder_name):
        conn = self.auth()
        root = self.__root()
    
        try:
            req = conn.web.get_folder_by_server_relative_url(f"{root}/{folder_name}")
            req.get().execute_query()
            return req
        
        except ClientRequestException as e:
            print(e)
            return False



    # UPLOAD FILE 
    def upload_file_on_folder(self, path_file_abs : str = "", folder_name : str = ""):
        req = self.check_exist_folder(folder_name)

        if req:
            file_name = path_file_abs.split('/')[-1]
            
            with open(path_file_abs, 'rb') as content_file:

                file_content = content_file.read()
                req.upload_file(file_name, file_content).execute_query()

            print(f"Le fichier {file_name} chargé avec succès !")

            return True

        return False



    # UPLOAD FILES
    def upload_files_on_folder(self, folder_name_local : str = "", folder_name_online : str = ""):
        req = self.check_exist_folder(folder_name_online)

        if req:
            tab_files = os.listdir(f"{ folder_name_local }")
            [self.upload_file_on_folder(f"{folder_name_local + f}", folder_name_online) for f in tab_files if os.path.isfile(folder_name_local + f)] 
            return True

        else: 
            return False



class OneDrive(Main):
    
    def __init__(self, email, password, endpoint, type):
        Main.__init__(self, email, password, endpoint, type)

    
    #SHARE FOLDER
    def share_folder(self, folder_name : str = "", is_edit = False):
        conn = self.auth()
        result = conn.web.create_anonymous_link(conn, url=f"Documents/{folder_name}", is_edit_link = is_edit).execute_query()

        return result.value






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

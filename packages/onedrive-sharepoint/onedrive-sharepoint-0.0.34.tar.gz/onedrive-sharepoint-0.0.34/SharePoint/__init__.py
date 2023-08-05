import os
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
from office365.runtime.client_request_exception import ClientRequestException


class SharePoint():

    def __init__(self, username, password, sharepoint_website_url):
        self.username = username
        self.password = password
        self.sharepoint_website_url = sharepoint_website_url


    def __auth(self):
        user_credentials = UserCredential(self.username, self.password)
        conn = ClientContext(self.sharepoint_website_url).with_credentials(user_credentials)
        
        return conn


    def create_team_website_sharepoint(self, title : str, is_public = False):
        conn = self.__auth()
        
        try:
            conn.create_team_site(alias = {title}, title = {title}, is_public = is_public)
            print("Création avec succès !!!")
            return True

        except:
            print("Erreur de création !!!")
            return False


    def create_communication_website_sharepoint(self, title : str):
        conn = self.__auth()
        
        try:
            conn.create_communication_site(alias = {title}, title = {title})
            print("Création avec succès !!!")
            return True

        except:
            print("Erreur de création !!!")
            return False



    def get_folders(self, folder_name : str = ""):
        conn = self.__auth()
        list_source = conn.web.get_folder_by_server_relative_url(f"Documents partages/{folder_name}")
        folders = list_source.folders
        conn.load(folders)
        conn.execute_query()

        return folders



    def get_files(self, folder_name : str = ""):
        conn = self.__auth()
        list_source = conn.web.get_folder_by_server_relative_url(f"Documents partages/{folder_name}")
        files = list_source.files
        conn.load(files)
        conn.execute_query()

        return files



    def create_folder(self, new_folder_name : str, location_folder : str = ""):
        conn = self.__auth()
        result = conn.web.folders.add(f'Documents partages/{location_folder}/{new_folder_name}').execute_query()

        if result:

            relative_url = f'Documents partages/{location_folder}/{new_folder_name}'
            
            return relative_url


    
    def download_file(self, file_url : str):
        conn = self.__auth()
        filename = file_url.split("/")[-1]

        with open(f"{filename}", "wb") as local_file:

            file = conn.web.get_file_by_server_relative_url(file_url)
            file.download(local_file)
            conn.execute_query()
        
        print(f"Fichier { filename } téléchargé avec succès !")

        return True



    def download_files_from_folder(self, folder_name : str = ""):

        files = self.get_files(folder_name)

        if len(files) > 0:
            [self.download_file(file.serverRelativeUrl) for file in files]
            return True

        else:
            print("Aucun Fichier téléchargé !!! Vérifiez le nom du dossier.")
            return False



    def upload_file_on_sharepoint(self, path_file_abs : str = "", folder_name_sharepoint : str = ""):
        req = self.check_exist_folder(folder_name_sharepoint)

        if req:
            file_name = path_file_abs.split('/')[-1]
            
            with open(path_file_abs, 'rb') as content_file:

                file_content = content_file.read()
                req.upload_file(file_name, file_content).execute_query()

            print(f"Le fichier {file_name} chargé avec succès !")

            return True

        return False



    def upload_files_on_folder_sharepoint(self, folder_name_local : str = "", folder_name_sharepoint : str = ""):
        req = self.check_exist_folder(folder_name_sharepoint)

        if req:
            tab_files = os.listdir(f"{ folder_name_local }")
            [self.upload_file_on_sharepoint(folder_name_local+f, folder_name_sharepoint) for f in tab_files if os.path.isfile(folder_name_local + f)] 
            return True

        else: 
            return False



    def check_exist_folder(self, folder_name_sharepoint):
        conn = self.__auth()
    
        try:
            req = conn.web.get_folder_by_server_relative_url(f"Documents partages/{folder_name_sharepoint}")
            req.get().execute_query()
            return req
        
        except ClientRequestException as e:
            print(e)
            return False
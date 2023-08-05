# **Automation of some processes on office365**

<br></br>

> #### Require :  **pip install Office365-REST-Python-Client**

<br></br>


### 1.   **Create session user**

<br>

```
from onedrive_sharepoint.main import OneDrive

email = "XXXXXXXXXXXXXXXXXXXXXX"
password = "XXXXXXXXXXXXXXXXXXXXXX"
endpoint = "https://<tenant_name>.sharepoint.com/personal/<username>" (for onedrive)
type = "onedrive"

session = OneDrive(email=email, password=password, endpoint=endpoint, type=type)
```

> type takes the values "onedrive" and "sharepoint"


<br></br>


### 2.   **Get folders**

```
folders = session.get_folders()

for folder in folders:  

    print(folder.name)
```

<br>

#### Folder Properties 

To see all the properties of a file, use the **properties** attribute. 
For example 

``` 
    print(folder.properties) 
```

output

```
{
    'Exists': True,
    'IsWOPIEnabled': False,
    'ItemCount': 0,
    'Name': <folder_name>,
    'ProgID': None,
    'ServerRelativeUrl': '/personal/<tenant>/Documents/<folder_name>',
    'TimeCreated': '2022-10-10T12:58:09Z',
    'TimeLastModified': '2022-10-10T12:58:09Z',
    'UniqueId': '16636378-fd57-4456-9e0f-1331d62f1385',
    'WelcomePage': ''
}
```

<br></br>

### 3.   **Get files**

```
files = session.get_files()

print(*files, seq="\n")
```

<br>

#### **File Properties**

```
{
    'CheckInComment': '',
    'CheckOutType': 2,
    'ContentTag': '{263E029D-372D-476B-9609-1F84D2C9B578},1,1',
    'CustomizedPageStatus': 0,
    'ETag': '"{263E029D-372D-476B-9609-1F84D2C9B578},1"',
    'Exists': True,
    'IrmEnabled': False,
    'Length': '36653',
    'Level': 1,
    'LinkingUri': '<tenant>/Documents/<filename>.csv?d=w263e029d372d476b96091f84d2c9b578',
    'LinkingUrl': '<tenant>/Documents/<filename>.csv?d=w263e029d372d476b96091f84d2c9b578',
    'MajorVersion': 1,
    'MinorVersion': 0,
    'Name': 'KOLDA.csv',
    'ServerRelativeUrl': '/personal/<tenant>/Documents/<filename>.csv',
    'TimeCreated': '2022-10-07T12:32:38Z',
    'TimeLastModified': '2022-10-07T12:32:38Z',
    'Title': None,
    'UIVersion': 512,
    'UIVersionLabel': '1.0',
    'UniqueId': '263e029d-372d-476b-9609-1f84d2c9b578'
}
```


<br></br>

### 4.   **Create folder**

```
session.create_folder(folder_name)
```


<br></br>

### 5.   **Download files from folder**

```
session.download_file(folder_name)
```

<br></br>

### 6.   **Upload files local to [onedriver or sharepoint] folder**

```
session.upload_files_on_folder(path_folder_name_local, folder_name_online)
```
<br>

Upload single file on OneDrive|SharePoint

```
session.upload_file_on_folder(path_file_name_local, folder_name_online)
```

<br></br>

### 7.   **Share folder with Anonymous**

```
session.share_folder(<folder_name>)
```

output

```
Link like this => https://<tenant>.sharepoint.com/:f:/g/personal/<username>/EnhjYxZX_VZEng8TMdYvE4UB78vdTFHSEs3vc5FgqQ1A8Q
```
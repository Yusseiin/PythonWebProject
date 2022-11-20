from tinydb import TinyDB, Query
import pathlib
from hideme import encPwd, decPwd

currentpath = str(pathlib.Path(__file__).parent.resolve())
new_dir_name = 'Resource'
new_dir = pathlib.Path(currentpath, new_dir_name)
new_dir.mkdir(parents=True, exist_ok=True)
new_dir_name = 'db'
new_dir = pathlib.Path(new_dir, new_dir_name)
new_dir.mkdir(parents=True, exist_ok=True)
db = TinyDB(str(new_dir) + '\\db_one.json')

#db.truncate()
#db.insert({'Username': 'Username', 'Name': 'Name', 'Surname': 'Surname', 'Email': 'Email', 'Telephone': 'Telephone','ChatId': 123456})
userid = "184646691"
textReceived = "matteo"
db.update({"Username": textReceived}, Query().ChatId == str(userid))

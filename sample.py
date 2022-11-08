from SwobBackendPublisher import MySQL, Lib

MYSQL_HOST=""
MYSQL_USER=""
MYSQL_PASSWORD=""
MYSQL_DATABASE=""

db = MySQL.connector(
        database=MYSQL_DATABASE, 
        user=MYSQL_USER, 
        password=MYSQL_PASSWORD, 
        host=MYSQL_HOST
    )
    
SBPLib = Lib(db=db)

result = SBPLib.whoami(phone_number="")
result = SBPLib.decrypt(phone_number="", platform_name="")
result = SBPLib.whichplatform(platform_letter="")
result = SBPLib.myplatforms(user_id="")

print(result)

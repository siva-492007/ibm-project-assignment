import ibm_db

DATABASE = "bludb"
HOSTNAME = "19af6446-6171-4641-8aba-9dcff8e1b6ff.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud"
PORT = 30699
UID = "ygg32911"
PWD = "kePH8FKY43ESmASQ"

connection = ibm_db.connect(f"DATABASE={DATABASE};HOSTNAME={HOSTNAME};PORT={PORT};SECURITY=SSL;SSLServerCertificate=DigitCertGlobalRootCA.crt;UID={UID};PWD={PWD}", "", "")
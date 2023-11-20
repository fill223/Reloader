import importlib
from reload import reload_pc
import pymysql.cursors
import configparser
import datetime
import time
import info





#____________________________________________________________________________________
#Connect to SQL

def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config



config_file = "config.ini"
config = read_config(config_file)

# Access the variables from the 'Database' section
host = config.get('MySQL', 'host')
port = config.getint('MySQL', 'port')
user = config.get('MySQL', 'user')
password = config.get('MySQL', 'password')
database = config.get('MySQL', 'database')
iteractions=config.get('MySQL', 'iteractions')
sleep=config.get('MySQL', 'sleep')


#Setting key

key="your_personal_sha_key"

#Decrypt data
from cryptography.fernet import Fernet
f=Fernet(key)
decrypted=f.decrypt(password)


password=decrypted.decode()

connection = pymysql.connect(host=host,
                        user=user,
                        password=password,
                        database=database,
                        charset='utf8',
                        cursorclass=pymysql.cursors.DictCursor)

print("Connected to SQL \n")

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Execution to SQL


for i in range(int(iteractions)):

    # Force reload of info module
    importlib.reload(info)
    (
        username,
        hostname,
        domain_name,
        ip_address,
        system_name,
        node_name,
        release,
        version,
        machine,
        processor,
        uptime,
        status_log_in,
    ) = info.get_pc_info()

    today = datetime.datetime.today()
    dt_now = today.strftime("%Y/%m/%d %H:%M:%S")
    cursor = connection.cursor()

    #Checking if there is already str whith this HostName
    availability_check = "SELECT Ip FROM pc_reloader WHERE HostName=(%s)"
    cursor.execute(availability_check, info.hostname)
    already = str(cursor.fetchone())
    connection.commit()

    if already == "None":
        #Create the string and insert data
        print("There is no line about this pc => adding str in db \n")
        print(str(today))
        creating = ("INSERT INTO pc_reloader (Ip, HostName, UserName, Domain, UpTime, LastUpdate, Logged) VALUES(%s, %s, %s, %s, %s, %s, %s)" )
        cursor.execute(creating, (str(info.ip_address), str(info.hostname), str(info.username), str(info.domain_name), str(info.uptime), str(today), str(info.status_log_in)))
        connection.commit()
    else:
        #Update info in the existing str
        print("There is already line about this pc => updating info in db \n")
        update_info = "UPDATE pc_reloader SET Ip=%s, UserName=%s, Domain=%s, UpTime=%s, LastUpdate=%s, Logged=%s WHERE HostName=(%s)"
        cursor.execute(update_info, (str(info.ip_address), str(info.username), str(info.domain_name), str(info.uptime), str(today), str(info.status_log_in), str(info.hostname)))
        connection.commit()

    print("Checked info about pc in DB, checking reload \n")


    reload_check = "SELECT Reload FROM pc_reloader WHERE HostName=%s"
    cursor.execute(reload_check, info.hostname)
    reload = (cursor.fetchone())
    reload = reload.get('Reload')
    connection.commit()
    print("Reload status is " + reload + "\n")

    if reload == "yes":
        print("Reload line is 'yes', reloading \n")
        logged_clear = 'UPDATE pc_reloader SET Logged="no" WHERE HostName=%s'
        cursor.execute(logged_clear, info.hostname)
        connection.commit()

        reload_clear = 'UPDATE pc_reloader SET Reload="no" WHERE HostName=%s'
        cursor.execute(reload_clear, info.hostname)
        connection.commit()
        reload_pc()

    print("End of loop, coming to sleep")
    time.sleep(int(sleep))

connection.close()




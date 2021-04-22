import sqlite3
from sqlite3 import Error
name="Ajith"
name =name+" "+"Anand"
print(name)
try:
    db_path='../../HostelManagement/db.sqlite3'
    connection = sqlite3.connect(db_path)
    cursor =connection.cursor()
    cursor.execute(f"select sd_id from User_student Where sd_name='{name}'  ")
    result=cursor.fetchone()
    cursor.execute(f"select * from User_attendance Where sd_name='{name}'  AND  date=CURRENT_DATE ")
    at =cursor.fetchone()
    student_id=result[0]
    print(student_id)
    if at is None:
        cursor.execute(f"insert into User_attendance('sd_id','date','status','sd_name','stduent_info_id') values({student_id},CURRENT_DATE ,1,'{name}',{student_id}) ")
        connection.commit()
        print("value inserted")
    else:
        print("already value exists!!")
    cursor.close()
    connection.close()
    print(result)
    print(at)
except Error as e:
    print(e)
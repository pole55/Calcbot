import psycopg2


def add(username):
    con = psycopg2.connect(
        host="ec2-54-211-210-149.compute-1.amazonaws.com", 
        user="dprqhirtaukzyz", 
        password="19503df752de21b6ab036578760b3cb6904035ee0c8aa9f4142d5069ed3a3937", 
        database="d4k65lptppsltt", 
        port="5432"
        )
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users (NAME) VALUES ('{}')".format(username)
        )

    con.commit()  
    con.close()


def read():
    con = psycopg2.connect(
        host="ec2-54-211-210-149.compute-1.amazonaws.com", 
        user="dprqhirtaukzyz", 
        password="19503df752de21b6ab036578760b3cb6904035ee0c8aa9f4142d5069ed3a3937", 
        database="d4k65lptppsltt", 
        port="5432"
        )
    cur = con.cursor()
    cur.execute("SELECT name from users")
  
    rows = cur.fetchall()
    names =[]
    for row in rows:

        print("NAME =", row[0])
        names.append(row[0])
    print(len(names))
    print(len(set(names)))

# https://heroku-data-explorer.herokuapp.com/#/
read()
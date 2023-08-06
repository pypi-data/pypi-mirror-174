
The DBcm.UseDatabase context manager for working with MariaDB and SQLite3.

The 1.x release of this module was based on code created for the second edition 
of Head First Python. See Chapters 7, 8, 9, and 11 of the that book for information
on how this was done.  Release 1 targetted MySQL server.

For the third edition of Head First Python, DBcm moved to release 2 and now targets
MariaDB as its primary back-end database (although it should still work with a MySQL
server if that's what you're running).

The option to use SQLite (v3) is also supported in this release.

Simple example usage:

    from DBcm import UseDatabase, SQLError

    config = { 'host': '127.0.0.1',
               'user': 'myUserid',
               'password': 'myPassword',
               'database': 'myDB' }

    with UseDatabase(config) as cursor:
        try:
            _SQL = "select * from log"
            cursor.execute(_SQL)
            data = cursor.fetchall()
        except SQLError as err:
            print('Your query caused an issue:', str(err))

If a filename (string) is used in place of a dictionary when using 
DBcm.UseDataBase, the data is assumed to reside in a local SQLite file.

Note: It is assumed you have a working version of the MariaDB server installed
on the computer onto which you're installing DBcm.  (If not, you'll get build 
errors due to the absence of the MariaDB client-side C tools).


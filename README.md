# My Knowledge Base

A simple wiki app implemented in Python + Django

### Run

1. Install PostgreSQL
2. Generate SECRET_KEY
3. Create user and database in PostgreSQL
4. Set the SECRET_KEY, DB_NAME, USER, PASSWORD variables in the **[start.sh](start.sh)** file
5. Change script permissions

```bash
$ chmod u+x ./start.sh
```

6. Run script

```bash
$ ./start.sh -<mode> <url>
```

For example:

```bash
$ ./start.sh -dev 127.0.0.1:8000
```

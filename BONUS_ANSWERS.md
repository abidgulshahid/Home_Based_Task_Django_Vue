# Bonus Questions Answers

## 1. What steps would you take to debug a failing REST API call?
Ans: I will check the server side  and client side logging  then will check the requests(Request Methods, Validation(Auth, Headers) and request payload). I will also check review database. Finally, I will do the code review.  



## 2. How would you handle database migrations in a production environment?
Test migrations in staging and dev env.
will create backups and do migrations in low traffic periods
Will use django migrations and will monitor migrations progress
Will have a rollback plan (MainTain db backups, and monitoring in place)


## 3. What's one common security mistake in Django and how would you avoid it?
 Hardcode secret_key in settings.py or commit it to Github

**How to Avoid It:**
Use Env Variables

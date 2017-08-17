# Logs Analysis Project
> Alain Boisvert, Québec, Canada, 2017-08-17 10:37 EDT.

- [Summary](#p0)
- [Instructions for running the program](#p1)
  - [Install and start the Virtual Machine](#p1a)
  - [Load the data to the database](#p1b)
  - [Clone and run the reporting tool](#p1c)
- [Results](#p2)
- [Description of the program's design](#p3)
  - [The `run()` method](#p3a)
  - [The `__execute()` method](#p3b)
  - [The `__write()` method](#p3b)
  - [The `__open_connection()` and `__close_connection()` methods](#p3d)
- [License](#p4)

<a name="p0"></a>
## Summary

Here is my third project for the "Full Stack Web Developer Nanodegree".

The objective of this project is to develop a python code that query a database 
and displays the correct answers to each of the questions in the lab description.

The repository of this project is 
https://github.com/boisalai/logs-analysis-project

The code is written in Python 3 and conforms to [PEP 8 guidelines](https://www.python.org/dev/peps/pep-0008/).

This document assumes you have already set up Python3.

<a name="p1"></a>
## Instructions for running the program

<a name="p1a"></a>
### Install and start the Virtual Machine 
> The instructions to install and start the virtual machine come from Udacity (Full Stack Web Developer Nanodegree, 3. The Backend: Database & Applications, Lesson 2: Elements of SQL, 17. Installing the Virtual Machine)

This project needs a virtual machine (VM) to run an SQL database server. For this project,
we're using tools called [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads) to install and manage the VM. 

Install VirtualBox first. You can download it from 
[virtualbox.org](https://www.virtualbox.org/wiki/Downloads). Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it; Vagrant will do that.

Next step, install Vagrant. Download it from 
[vagrantup.com](https://www.vagrantup.com/downloads.html). 
Install the version for your operating system.  

Now you need to configure the virtual machine and, for this, a configuration file already exists. 

Clone the repository https://github.com/udacity/fullstack-nanodegree-vm. 

Inside the cloned repository, you will find a directory called `/vagrant`. 
From your terminal, change directory to the `/vagrant` directory.
Inside this subdirectory, run the command `$ vagrant up`. 
This will cause Vagrant to download the Linux operating system and install it.

```
$ ls
README.md	vagrant
$ cd vagrant
$ ls
Vagrantfile  catalog  forum  tournament
$ vagrant up
```

Be patient. This may take a few minutes.

When `$ vagrant up` is finished running, you will get your shell prompt back. At this point, you can run `$ vagrant ssh` to log in to your newly installed Linux VM!

In addition to the VM, you have now the PostgreSQL database and support software needed for this project.

Finally, the shared directory is located at `/vagrant`. To access your shared files: `$ cd /vagrant`. You should see something like this.

```
vagrant@vagrant:~$ cd /vagrant
vagrant@vagrant:/vagrant$
```

<a name="p1b"></a>
### Load the data to the database

> These instructions to load the data to the database come from Udacity (Full Stack Web Developer Nanodegree, 3. The Backend: Database & Applications, Project: Logs Analysus Project)

Next, download the data <a target="_blank" href="https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip">here</a>. 
You will need to unzip this file after downloading it. The file inside is called `newsdata.sql`. Put this file into the `/vagrant` directory, which is shared with your VM.

To build the reporting tool, you'll need to load the site's data into your local database. To do this, use the command:

```sql
$ psql -d news -f newsdata.sql
```


Running this command will connect to the `news` database and execute the SQL commands in the downloaded file, creating tables and populating them with data.

<a name="p1c"></a>
### Clone and run the reporting tool 

Now you need the Python code that prints out reports (in plain text) based on the data in the database.

To do this, 
clone the repository https://github.com/boisalai/logs-analysis-project.
Copy the file 'report.py' under vagrant directory created earlier.

Inside this python file, you may need to change the path of the output file if you are working on a different directory.

```python
PATH = "/vagrant/report.txt"
```

Then, run the Python file like this.

```
vagrant@vagrant:/vagrant$ python3 report.py 
```

You should see traces of the execution in the terminal window.
The file `report.txt` is also created containing the results of each question
in the lab description.

<a name="p2"></a>
## Results

The file `report.txt` should contain the following results.

```
Question 1
What are the three most popular articles of all time?
"Candidate is jerk, alleges rival" - 338,647 views
"Bears love berries, alleges bear" - 253,801 views
"Bad things gone, say good people" - 170,098 views

Question 2
Who are the most popular article authors of all time?
"Ursula La Multa" - 507,594 views
"Rudolf von Treppenwitz" - 423,457 views
"Anonymous Contributor" - 170,098 views
"Markoff Chaney" - 84,557 views

Question 3
On which days did more than 1% of requests lead to errors?
July 17, 2016 - 2.3 errors
```

Also, the terminal window should contain the following traces.

```
vagrant@vagrant:/vagrant/project$ python3 report.py 

Connection was created successfully.

Title:
Create a view
Query:
CREATE VIEW article_author_log AS SELECT articles.slug, articles.title, authors.name FROM articles, authors, log WHERE log.path = '/article/' || articles.slug AND articles.author = authors.id
Elapsed time:
0.1658 milliseconds

Title:
Question 1
What are the three most popular articles of all time?
Query:
SELECT slug, title, count(*) as num FROM article_author_log GROUP BY slug, title ORDER BY num DESC LIMIT 3
Result:
"Candidate is jerk, alleges rival" - 338,647 views
"Bears love berries, alleges bear" - 253,801 views
"Bad things gone, say good people" - 170,098 views
Elapsed time:
0.3125 milliseconds

Title:
Question 2
Who are the most popular article authors of all time?
Query:
SELECT name, count(*) as num FROM article_author_log GROUP BY name ORDER BY num DESC
Result:
"Ursula La Multa" - 507,594 views
"Rudolf von Treppenwitz" - 423,457 views
"Anonymous Contributor" - 170,098 views
"Markoff Chaney" - 84,557 views
Elapsed time:
0.2129 milliseconds

Title:
Compute status frequency
Query:
SELECT status, count(*) as num FROM log GROUP BY status
Result:
('404 NOT FOUND', 12908)
('200 OK', 1664827)
Elapsed time:
0.1841 milliseconds

Title:
Create a view
Query:
CREATE VIEW day_status AS SELECT date_trunc('day', time) as day, CASE status WHEN '200 OK' THEN 1 ELSE 0 END AS ok, CASE status WHEN '200 OK' THEN 0 ELSE 1 END AS not_found FROM log
Elapsed time:
0.0707 milliseconds

Title:
Question 3
On which days did more than 1% of requests lead to errors?
Query:
SELECT day, sum(ok), sum(not_found), 100*sum(not_found)/(sum(ok)+sum(not_found))::float AS pct FROM day_status GROUP BY day HAVING sum(not_found)/(sum(ok)+sum(not_found))::float > 0.01
Result:
July 17, 2016 - 2.3 errors
Elapsed time:
0.2742 milliseconds

Connection was closed.
```


<a name="p3"></a>
## Description of the program's design

The Python code starts with the following instructions.

```python
if __name__ == '__main__':
    app = Report()
    app.run()
```

The class `Report` contains two variables and five methods.
- Instance variable `__report`: Output file for the report.
- Instance variable `__conn`: Connection object to a database.
- Method `__open_connection()`: Connect to the PostgreSQL database.
- Method `__close_connection()`: Close database connection.
- Method `__write()`: Write a line to the report.
- Method `__execute()`: Execute query and print the results.
- Method `run()`: Main method that launches all queries.

Note that the instance variables and methods respect this naming rules from PEP 8: 

> Lowercase with words separated by underscores as necessary to improve readability. Use one leading underscore only for non-public methods and instance variables. To avoid name clashes with subclasses, use two leading underscores to invoke Python's name mangling rules.<br>
Source: PEP 8 -- Style Guide for Python Code, [Method Names and Instance Variables](https://www.python.org/dev/peps/pep-0008/#method-names-and-instance-variables)

Indeed, only the `run()` method must be declared public. 
Other instance variables and methods may be declared private.

<a name="p3a"></a>
### The `run()` method

The `run()` method performs a number of tasks in the following order.
- Open a file to write a text report.
- Open a database connection.
- Execute queries by passing instructions to the `__execute()` method.
- Close database connection.
- Close the report file.

To answer questions 1 and 2, this method first creates a view.

```sql
CREATE VIEW article_author_log AS 
SELECT articles.slug, articles.title, authors.name 
FROM articles, authors, log 
WHERE log.path = '/article/' || articles.slug 
AND articles.author = authors.id
```

To create this view, these instructions are passed to the `__execute()` method.

```python
title = "Create a view"
query = ("CREATE VIEW article_author_log AS "
         "SELECT articles.slug, articles.title, authors.name "
         "FROM articles, authors, log "
         "WHERE log.path = '/article/' || articles.slug "
         "AND articles.author = authors.id")
fetch = False
format = None
report = False
self.__execute(title, query, fetch, format, report)
```

The private `__execute()` method and his arguments are explained in detail below.

Similarly, to answer question 3, the `run()` method creates another view.

```sql
CREATE VIEW day_status AS 
SELECT date_trunc('day', time) as day, 
       CASE status WHEN '200 OK' THEN 1 
                   ELSE 0 
       END AS ok, 
       CASE status WHEN '200 OK' THEN 0 
                   ELSE 1 
       END AS not_found 
FROM log
```

This SQL code creates two columns containing 0 or 1 depending on the value of the `status` column. If the `status` column contains `'200 OK'`, then the column `ok` contains 1 and the column `not_found` contains 0. Otherwise, if the `status` column does not contain `'200 OK'`, the column `ok` contains 0 and the column `not_found` contains 1.

After creating these views, the `run()` method performs three queries to answer 
each of three questions of the lab description like this. 

```python
# Question 1
title = ("Question 1\nWhat are the three most popular articles "
         "of all time?")
query = ("SELECT slug, title, count(*) as num "
         "FROM article_author_log "
         "GROUP BY slug, title "
         "ORDER BY num DESC "
         "LIMIT 3")
fetch = True
format = ('"{0}" - {1:,} views', 1, 2)
report = True
self.__execute(title, query, fetch, format, report)


# Question 2
title = ("Question 2\nWho are the most popular article authors "
         "of all time?")
query = ("SELECT name, count(*) as num "
         "FROM article_author_log "
         "GROUP BY name "
         "ORDER BY num DESC")
fetch = True
format = ('"{0}" - {1:,} views', 0, 1)
report = True
self.__execute(title, query, fetch, format, report)


# Question 3
title = ("Question 3\nOn which days did more than 1% of requests "
         "lead to errors?")
query = (
    "SELECT day, sum(ok), sum(not_found), "
    "    100*sum(not_found)/(sum(ok)+sum(not_found))::float AS pct "
    "FROM day_status "
    "GROUP BY day "
    "HAVING sum(not_found)/(sum(ok)+sum(not_found))::float > 0.01")
fetch = True
format = ('{0:%B %d, %Y} - {1:.1f} errors', 0, 3)
report = True
self.__execute(title, query, fetch, format, report)
```


<a name="p3b"></a>
### The `__execute()` method

The `__execute()` method execute query and print the results. This method
takes five arguments.
- title: the title for the report (string).
- query: the SQL query (string).
- fetch: a boolean value indicating whether to fetch or not rows of a query result (boolean).
- format: the format to print result (tuple or None).
- report: a boolean value indicating whether to write or not the result to the report (boolean).

The `format` variable is a tuple containing three values. The first value is a string containing 
literal text or replacement fields delimited by braces `{}`. Two replacement fields are expected
The second and third values of the `format` variable contain an integer indicating 
which value of the `row` tuple to pass to the 
`[str.format()](https://docs.python.org/3/library/stdtypes.html#str.format)` method.


So, to write a report line, this statement is used.

```python
print(format[0].format(row[format[1]], row[format[2]]))
```

After all operations are completed, the `__execute()` method calculates elapsed 
time to perform these operations. 


<a name="p3c"></a>
### The `__write()` method line

This `__write()` method write a line to the report. 
This method is called by The `__execute()` method like this.

```python
if report:
    # Print title to the report.
    self.__write("\n" + title)
```

And like this...

```python
print(format[0].format(row[format[1]], row[format[2]]))
if report:
  self.__write(format[0].format(row[format[1]], row[format[2]]))
```


<a name="p3d"></a>
### The `__open_connection()` and `__close_connection()` methods

The `__open_connection()` method allows to connect to the PostgreSQL database with 
`psycopg2.connect(database=DBNAME)` instruction.

The `__close_connection()` method allows to close the database connection.


<a name="p4"></a>
## License

The contents of this repository are covered under the [MIT License](LICENSE).


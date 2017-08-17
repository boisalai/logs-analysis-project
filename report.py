#!/usr/bin/env python3
#
# Reporting tool that prints out reports (in plain text) based on the
# data in the database.

import psycopg2
import time


DBNAME = "news"
PATH = "/vagrant/report.txt"


class Report():
    # Output file for the report.
    __report = None

    # Connection object to a database.
    __conn = None

    def __open_connection(self):
        """Connect to the PostgreSQL database."""
        try:
            if self.__conn is None:
                # Connect to an existing database.
                self.__conn = psycopg2.connect(database=DBNAME)
                print("\nConnection was created successfully.")
            else:
                print("\nConnection already created.")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Oups!\n" + error)

    def __close_connection(self):
        """Close database connection."""
        if self.__conn is not None:
            self.__conn.close()
            print("\nConnection was closed.")
        else:
            print("\nConnection already closed.")

    def __write(self, line):
        """Write a line to report."""
        self.__report.write(line + "\n")

    def __execute(self, title, query, fetch, format, report):
        """Execute query and print the results.

        Keyword arguments:
        title -- the title for the report (string).
        query -- the query (string).
        fetch -- fetch or not (boolean).
        format -- the format to print result (tuple or None).
        report -- write or not to the report (boolean).
        """

        try:
            # Get current time.
            start = time.process_time()

            # Print title to the terminal.
            print("\nTitle:\n" + title)

            if report:
                # Print title to the report.
                self.__write("\n" + title)

            # Print query to the terminal.
            # Remove multiple whitespaces of the query.
            print("Query:\n" + " ".join(query.split()))

            # Open a cursor to perform database operations.
            cur = self.__conn.cursor()

            # Execute the query.
            # Query the database.
            cur.execute(query)

            # Fetchall only if 'fetch' is True.
            if fetch:
                # Print result.
                print("Result:")

                # Obtain data as Python objects.
                rows = cur.fetchall()
                for row in rows:
                    if isinstance(format, tuple):
                        # Formatted result.
                        print(format[0].format(row[format[1]],
                              row[format[2]]))
                        if report:
                            self.__write(format[0].format(row[format[1]],
                                         row[format[2]]))
                    else:
                        # Result not formatted.
                        print(row)

            # Close cursor.
            cur.close()

            # Calculate and print elapsed time.
            end = time.process_time()
            elapsed = (end-start)*1000
            print("Elapsed time:\n{:.4f} milliseconds".format(elapsed))

        except (Exception, psycopg2.DatabaseError) as error:
            print("Oups!\n" + error)

    def run(self):
        """Main method that launches all queries."""

        # Open a new file in write mode to write the report.
        self.__report = open(PATH, 'w')

        # Open connection to the database.
        self.__open_connection()

        # Create a view to answer questions 1 and 2.
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

        # Question 1.
        # What are the most popular three articles of all time?
        # Which articles have been accessed the most? Present this
        # information as a sorted list with the most popular article
        # at the top.
        # Example:
        # "Princess Shellfish Marries Prince Handsome" — 1201 views
        # "Baltimore Ravens Defeat Rhode Island Shoggoths" — 915 views
        # "Political Scandal Ends In Political Scandal" — 553 views
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

        # Question 2.
        # Who are the most popular article authors of all time?
        # That is, when you sum up all of the articles each author has
        # written, which authors get the most page views? Present this
        # as a sorted list with the most popular author at the top.
        # Example:
        # Ursula La Multa — 2304 views
        # Rudolf von Treppenwitz — 1985 views
        # Markoff Chaney — 1723 views
        # Anonymous Contributor — 1023 views
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

        # Count views by status from 'log' table.
        title = "Compute status frequency"
        query = ("SELECT status, count(*) as num "
                 "FROM log "
                 "GROUP BY status")
        fetch = True
        format = None
        report = False
        self.__execute(title, query, fetch, format, report)

        # Create a view to answer question 3.
        title = "Create a view"
        query = (
            "CREATE VIEW day_status AS "
            "SELECT date_trunc('day', time) as day, "
            "       CASE status WHEN '200 OK' THEN 1 "
            "                   ELSE 0"
            "       END AS ok, "
            "       CASE status WHEN '200 OK' THEN 0 "
            "                   ELSE 1"
            "       END AS not_found "
            "FROM log")
        fetch = False
        format = None
        report = False
        self.__execute(title, query, fetch, format, report)

        # Question 3.
        # On which days did more than 1% of requests lead to errors?
        # The log table includes a column status that indicates the
        # HTTP status code that the news site sent to the user's
        # browser.
        # Example:
        # July 29, 2016 — 2.5% errors
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

        # Close communication with the database.
        self.__close_connection()

        # Close the report.
        self.__report.close()


if __name__ == '__main__':
    app = Report()
    app.run()

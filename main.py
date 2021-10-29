# File: main.py
# Author: Lorè Francesco
#   Program to build a simplified and proof-of-concept software application
#   for managing an electronic table reservation book for a restaurant in the evening of a specific day.
#   The software is composed  of a user interface and business logic part
#   written in Python and an SQL database management system (MySQL) to store the data.

# Python v. 3.9.1
import mysql.connector as ms # mysql-connector-python v. 8.0.23
import pandas as pd # pandas v. 1.2.0


# All functions are inside the main function that starts automatically when we open the file
def main():
    # connection to database mysql
    dbconn = ms.connect(
        host="localhost",
        user="root",
        database="ds_project"
    )

    # creation of cursor
    dbcur = dbconn.cursor(buffered=True)

    # function to execute a query, when there is a 'SELECT' or 'WITH'
    # at beginning of the query return a dataframe otherwise commit the result
    # that can be a DELETE, UPDATE, or INSERT operation
    def queryEx(query, cur=dbcur, con=dbconn):
        cur.execute(query)
        if "SELECT" == query[:6] or "WITH" == query[:4]:
            df = pd.DataFrame(dbcur, columns=cur.column_names)
            return df
        else:
            con.commit()

    # The following function is used to check the command to do by splitting the input getting a list and then check
    # if the first element of the list is in the dictionary-keys, in which for each operation there is the related function
    # the program creates the dictionary "listIns" after having defined all functions
    def Instruction(inp):
        inpList = inp.split()
        if inpList[0] in listIns.keys():
            return listIns.get(inpList[0])(inpList[1:]) # return the fit function from dictionary
                                                        # (the actual parameters is the list of element
                                                        # in inpList except the first that is the command code)
        else:
            return "Error"

    # function to register reservation of a table
    def funR(inp):
        # check if there are only 3 element otherwise returns Error
        if len(inp) == 3:
            # check the validity of phone number (length = 10, and all characters are digit)
            if len(inp[1]) == 10:
                if inp[1].isdigit() is False:
                    return "Error"
            else:
                return "Error"

            # check that the number of guests is a digit
            if inp[0].isdigit() is False:
                return "Error"

            # check if the number of guests is > 6
            # because in this case the restaurant is not able to book a table
            inp[0] = int(inp[0])
            if inp[0] > 6:
                return "Error"

            # check if there is a reservation with the same phone number or the same name, in this case the function returns Error
            query = 'SELECT name ' \
                    'FROM reservation ' \
                    'WHERE name = "{0}" OR phone_number = "{1}"'.format(inp[2], inp[1])
            res = queryEx(query)
            if res.shape[0] > 0:
                return "Error"
            else:
                # the function verifies if there is an available table with the same number of guests, if not
                # the function find a table with a number of seats > guests
                # If there are not available tables it returns Error
                # otherwise it executes 3 query
                occ = False
                for i in range(0, 7 - inp[0]):
                    query = 'SELECT count(dt.ID_table) ' \
                            'FROM dining_table dt ' \
                            'WHERE dt.seats = "{0}" ' \
                            '   AND dt.ID_table not in (' \
                            '       SELECT r.ID_table ' \
                            '       FROM reservation r' \
                            ')'.format(inp[0] + i)
                    res = queryEx(query)
                    if res.values[0, 0] > 0:
                        # 1 query: get the ID_table of selected table
                        query = 'SELECT dt.ID_table ' \
                                'FROM dining_table dt ' \
                                'WHERE dt.seats = "{0}" ' \
                                '   AND dt.ID_table not in (' \
                                '       SELECT r.ID_table ' \
                                '       FROM reservation r' \
                                '   )'.format(inp[0] + i)
                        ID_table = queryEx(query).values[0, 0]
                        # 2 query : get the max value of ID_res inside reservation table,
                        # if there are not bookings set new ID_res = 1
                        # otherwise set new ID_res = max(ID_res) + 1
                        # in this way the function creates an ID different than others
                        query = 'SELECT max(ID_res) ' \
                                'FROM reservation'
                        ID_res = queryEx(query).values[0, 0]
                        if ID_res is None:
                            ID_res = 1
                        else:
                            ID_res = ID_res + 1
                        # 3 query: insert data into reservation table
                        query = 'INSERT INTO reservation values ' \
                                '({0}, {1}, {2}, "{3}", "{4}")'.format(ID_res, ID_table, inp[0], inp[1], inp[2])
                        queryEx(query)
                        occ = True
                        break
                # if occ is false the function don't find an available table, in this case the function returns Error,
                # otherwise it returns a empty string
                if occ is False:
                    return "Error"
                else:
                    return ""
        else:
            return "Error"

    # function to select information about reservation
    def funS(inp):
        # checking if there is 1 argument beyond the code of operation
        if len(inp) == 1:
            # checking if argument is a phone number and then execute a query in which I select the required information
            # otherwise the function makes the same operation checking the name
            if inp[0].isdigit() is True and len(inp[0]) == 10:
                query = 'SELECT ID_table, guest_number, seats, phone_number, name ' \
                        'FROM reservation NATURAL JOIN dining_table ' \
                        'WHERE phone_number = "{0}"'.format(inp[0])

            else:
                query = 'SELECT ID_table, guest_number, seats, phone_number, name ' \
                        'FROM reservation NATURAL JOIN dining_table ' \
                        'WHERE name = "{0}"'.format(inp[0])
            res = queryEx(query)
            # if there is not result the function returns 'No result(s)' otherwise it returns the result
            if res.shape[0] < 1:
                return "No result(s)"
            else:
                return " ".join(map(str, list(res.iloc[0]))) # Here the function transform all element of selected tuple into string and then
                                                             # it uses the join() built-in function to show the desired result
                                                             # (it uses the list() function to convert the series into a lists)

    # The same operation of funS but in this case removing the information of a reservation
    # in base of the phone number or the name,
    # if there is not result or if the number of arguments is > 1, the function returns Error
    def funC(inp):
        if len(inp) == 1:
            if inp[0].isdigit() is True and len(inp[0]) == 10:
                query = 'SELECT ID_res ' \
                        'FROM reservation ' \
                        'WHERE phone_number = "{0}"'.format(inp[0])
                res = queryEx(query)
                if res.shape[0] < 1:
                    return "Error"
                else:
                    query = 'DELETE FROM reservation ' \
                            'WHERE phone_number = "{0}"'.format(inp[0])
                    queryEx(query)
                    return ""
            else:
                query = 'SELECT ID_res ' \
                        'FROM reservation ' \
                        'WHERE name = "{0}"'.format(inp[0])
                res = queryEx(query)
                if res.shape[0] < 1:
                    return "Error"
                else:
                    query = 'DELETE FROM reservation ' \
                            'WHERE name = "{0}"'.format(inp[0])
                    queryEx(query)
                    return ""
        else:
            return "Error"

    # function that returns all information required about reservation
    # if there are not informations it returns "No result(s)"
    def funL(inp):
        if len(inp) == 0:
            query = 'SELECT ID_table, guest_number, seats, phone_number, name ' \
                    'FROM reservation NATURAL JOIN dining_table'
            res = queryEx(query)
            if res.shape[0] < 1:
                return "No result(s)"
            else:
                for i in range(res.shape[0] - 1):                             # Since there are more results I use a loop to print the desired result
                    print(" ".join(map(str, list(res.iloc[i]))))              # the result is as funS() function
                return " ".join(map(str, list(res.iloc[res.shape[0] - 1])))

    # Function to list all the unreserved tables, one per line
    # the length of "inp" must be 0, if not the function returns Error
    def funU(inp):
        if len(inp) == 0:
            query = "SELECT dt.ID_table, dt.seats " \
                    "FROM dining_table dt " \
                    "WHERE dt.ID_table not in (" \
                    "   SELECT ID_table" \
                    "   FROM reservation r" \
                    ")"
            res = queryEx(query)
            if res.shape[0] < 1:
                return "No result(s)" # if there are not results the function returns this string
            else:
                for i in range(res.shape[0] - 1):
                    print(" ".join(map(str, list(res.iloc[i]))))
                return " ".join(map(str, list(res.iloc[res.shape[0] - 1]))) # this is the output of function
        else:
            return "Error"

    # function to output the number of reserved tables counting the number of booking in reservation table
    # If there is an argument the function returns the number of reserved tables under the number of guests
    # checking also if the number of guests is a digit or not
    def funNT(inp):
        if len(inp) == 0: # 0 arguments required
            query = "SELECT count(ID_table) " \
                    "FROM reservation"
            res = queryEx(query)
            return res.values[0, 0]
        elif len(inp) == 1: # 1 argument required
            if inp[0].isdecimal() is True:
                query = "SELECT count(t.ID_table) " \
                        "FROM (" \
                        "   SELECT r.ID_table " \
                        "   FROM reservation r " \
                        "   WHERE r.guest_number = {0}" \
                        ") as t".format(inp[0])

                # after "WHEN" I create a relation in which the number
                # of guests is equal to the argument
                res = queryEx(query)
                return res.values[0, 0]
            else:
                return "Error"
        else:
            return "Error"

    # function to output the number of booked guests overall checking always
    # if there are arguments or not, in the first case the function returns Error
    def funNG(inp):
        if len(inp) == 0:
            query = "SELECT sum(guest_number) " \
                    "FROM reservation"
            res = queryEx(query)
            if res.values[0, 0] is None:
                res.values[0, 0] = 0
            return res.values[0, 0]
        else:
            return "Error"

    # Function to output the number of unreserved seats overall.
    # In this case there are 2 queries and then their execution the function returns the difference between them
    def funNU(inp):
        if len(inp) == 0:
            query = "SELECT sum(seats) " \
                    "FROM dining_table" # getting number of seats
            query1 = "SELECT sum(guest_number)" \
                     "FROM reservation" # getting number of guests
            res = queryEx(query)
            res1 = queryEx(query1)
            if res1.values[0, 0] is None:
                res1.values[0, 0] = 0 # if the result is None the function returns 0 in way that it can be able
                                      # to do the difference between the number of seats and the number of guests 
            return res.values[0, 0] - res1.values[0, 0]
        else:
            return "Error"

    # function to show the information about table(s) with the
    # greatest number of unreserved seats, one per line
    def funGU(inp):
        if len(inp) == 0: # also in this case if there are arguments, the result is Error
            query = "WITH t as (" \
                    "   SELECT ID_table, guest_number, seats, (seats-guest_number) unreserved_seats " \
                    "   FROM reservation NATURAL JOIN dining_table " \
                    ") " \
                    "SELECT t.ID_table, t.guest_number, t.seats " \
                    "FROM t " \
                    "WHERE t.unreserved_seats = ( " \
                    "   SELECT max(t1.unreserved_seats) " \
                    "   FROM t t1 " \
                    ")" # to make this query I need to use "WITH"
            res = queryEx(query)
            if res.shape[0] < 1:
                return "No result(s)" # if there are not results return this string
            else:
                for i in range(res.shape[0] - 1):
                    print(" ".join(map(str, list(res.iloc[i]))))
                return " ".join(map(str, list(res.iloc[res.shape[0] - 1]))) # print the result of query one per line
        else:
            return "Error"

    # function to show the information about table(s) with the
    # greatest number of unreserved seats, one per line.
    # Output similar to funGU function, but the guests cannot be 0.
    # the structure is similar to funGU function, the query is different
    def funGR(inp):
        if len(inp) == 0:
            query = "WITH t as (" \
                    "   SELECT ID_table, guest_number, seats, (seats-guest_number) unreserved_seats " \
                    "   FROM (" \
                    "       SELECT *" \
                    "       FROM reservation" \
                    "       WHERE guest_number <> 0" \
                    "   ) as r NATURAL JOIN dining_table" \
                    ") " \
                    "SELECT t.ID_table, t.guest_number, t.seats " \
                    "FROM t " \
                    "WHERE t.unreserved_seats = ( " \
                    "   SELECT max(t1.unreserved_seats) " \
                    "   FROM t t1 " \
                    ")"
            res = queryEx(query)
            if res.shape[0] < 1:
                return "No result(s)"
            else:
                for i in range(res.shape[0] - 1):
                    print(" ".join(map(str, list(res.iloc[i]))))
                return " ".join(map(str, list(res.iloc[res.shape[0] - 1])))
        else:
            return "Error"

    # all functions are inserted into a dictionary in way that we can select the fit function in base of the code command enter by user
    listIns = {"R": funR, "S": funS, "C": funC, "L": funL, "U": funU,
               "NT": funNT, "NG": funNG, "NU": funNU, "GU": funGU, "GR": funGR}
    
    inp = input("> ")
    while inp != "X": # if the user print "X", he/she close the program
        printRes = Instruction(inp)
        if printRes != "":
            print(printRes)
        inp = input("> ")

    # closing the program, the following are operations to do: COMMIT WORK, CLOSE CURSOR, CLOSE CONNECTION
    dbconn.commit()
    dbcur.close()
    dbconn.close()


if __name__ == '__main__':
    main()

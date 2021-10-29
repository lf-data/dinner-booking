# Dinner Booking CLI

Program to build a simplified and proof-of-concept software application  for managing an electronic table reservation book for a restaurant in the evening of a specific day. The software is composed  of a user interface and business logic part  written in Python and an SQL database management system (MySQL) to store the data.

The following an abstraction of my function and database's table:

![function abstraction](function_abstraction.png)

The dining_table contains 12 tables: 3 tables with 2 seats, 2 tables with 3 seats, 3
tables with 4 seats, 2 tables with 5 seats, 2 tables with 6 seats. The number of seats
overall is 46.
Beyond the errors requested from assignment I added also others situation that can
return back an Error:

- If the number of guests is not a number but a character, the program returns
“Error”.
- If at least one characters inside a phone number are not a number or if the
length of phone number is different to 10, the program returns “Error”.
- If the code command entered by user is not inside a key of dictionary in which
there are all of function, the program returns “Error”.
- If there is not table available when the user would to enter a new booking,
the program returns “Error”.
- If the user would like to delete a booking but this booking not exist, the
program returns “Error”.
- If the user enters more or less than required argument or command, the
program returns “Error”.

The following an example of as the output of CLI appears:
```txt
> R 3 1234567891 Francesco
> R 2 1234567892 Giovanni
> R 1 1234567893 Michele
> R 4 1234567894 Domenico
> R 5 1234567895 Gianluca
> R 6 1234567896 Sofia
> R 2 1234567897 Giulia
> R 2 1234567898 Roberta
> R 2 1234567899 Irene
> R 2 1234567889 Irene
Error
> R 2 12ii56789 Marco
Error
> R 2 12ii567891 Marco
Error
> R f 1234567898 Marco
Error
> R 2 1234567891 Marco
Error
> C Giovanni
> C Marco
Error
> C 1234567895
> C 1234567892
Error
> U
1 2
8 4
9 5
10 5
12 6
> L
4 3 3 1234567891 Francesco
2 1 2 1234567893 Michele
6 4 4 1234567894 Domenico
11 6 6 1234567896 Sofia
3 2 2 1234567897 Giulia
5 2 3 1234567898 Roberta
7 2 4 1234567899 Irene
> NT
7
> GR
7 2 4
> GU
7 2 4
> NT 3
1
> NG
20
> NU
26
> S Francesco
4 3 3 1234567891 Francesco
> S Giovanni
No result(s)
> S 1234567891
4 3 3 1234567891 Francesco
> S 1234567892
No result(s)
> NT R
Error
> C Francesco
> C Michele
> C Domenico
> C Sofia
> C Giulia
> C Roberta
> C Irene
> L
No result(s)
> U
1 2
2 2
3 2
4 3
5 3
6 4
7 4
8 4
9 5
10 5
11 6
12 6
> X
```

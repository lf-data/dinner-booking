create table dining_table (
    ID_table int not null,
    seats int,
    primary key (ID_table)
);

create table reservation (
    ID_res int not null,
    ID_table int not null,
    guest_number int,
    phone_number char(10),
    name varchar(30),
    primary key (ID_res),
    foreign key (ID_table) references dining_table(ID_table)
);

insert into dining_table values (1,2);
insert into dining_table values (2,2);
insert into dining_table values (3,2);
insert into dining_table values (4,3);
insert into dining_table values (5,3);
insert into dining_table values (6,4);
insert into dining_table values (7,4);
insert into dining_table values (8,4);
insert into dining_table values (9,5);
insert into dining_table values (10,5);
insert into dining_table values (11,6);
insert into dining_table values (12,6);
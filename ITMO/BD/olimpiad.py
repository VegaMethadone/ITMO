import sqlite3

connect = sqlite3.connect("creation.db")
cursos  = connect.cursor()


###############################
######### TABLES ##############
###############################

## homesteads
cursos.execute(""" CREATE TABLE IF NOT EXISTS homesteads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    area INTEGER NOT NULL 
    );  
    """)

## owners
cursos.execute(""" CREATE TABLE IF NOT EXISTS owners (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    is_snt_member INTEGER
    );
    """)

## income
cursos.execute("""  CREATE TABLE IF NOT EXISTS income (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    info TEXT NOT NULL,
    price INTEGER NOT NULL
    );
    """)

## expenses
cursos.execute("""  CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    info TEXT NOT NULL,
    price INTEGER NOT NULL
    );
    """)

## average_expenses
cursos.execute("""  CREATE TABLE IF NOT EXISTS average_expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_id INTEGER NOT NULL,
    amount INTEGER NOT NULL,
    planned_money_amount INTEGER NOT NULL
    );
    """)

## periods
cursos.execute("""  CREATE TABLE IF NOT EXISTS periods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    startdate NUMERIC NOT NULL,
    enddate NUMERIC NOT NULL
    );
    """)

## ownership
cursos.execute("""  CREATE TABLE IF NOT EXISTS ownership  (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    homestead_id INTEGER NOT NULL,
    owner_id INTEGER NOT NULL,
    owning_startdate NUMERIC NOT NULL,
    owning_enddate NUMERIC,
    owning_type TEXT NOT NULL
    );
    """)

## actual_expenses
cursos.execute("""  CREATE TABLE IF NOT EXISTS actual_expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_id INTEGER NOT NULL,
    from_homestead_id INTEGER NOT NULL,
    amount INTEGER NOT NULL,
    period NUMERIC NOT NULL
    );
    """)

## income_trans
cursos.execute("""  CREATE TABLE IF NOT EXISTS income_trans (
    id INTEGER PRIMARY KEY  AUTOINCREMENT,
    income_id INTEGER NOT NULL,
    from_homestead_id INTEGER NOT NULL,
    amount INTEGER NOT NULL,
    transaction_date NUMERIC NOT NULL,
    amount_of_money INTEGER NOT NULL
    );
    """)

connect.commit()

###############################
########## DATA ###############
###############################

## homesteads
cursos.execute("""  INSERT INTO  homesteads (`id`, `area`)
    VALUES
    (1, 630),
    (2, 600),
    (3, 601),
    (4, 607),
    (5, 600),
    (6, 600),
    (7, 620),
    (8, 600),
    (9, 1200),
    (10, 650);
    """)

## owners (`id`, `name`, `is_snt_member`)
cursos.execute(""" INSERT INTO  owners (`id`, `name`, `is_snt_member`)
    VALUES
    (1, 'Иванов Павел Владиславович', 0),
    (2, 'Полнарев Михаил Федорович', 1),
    (3, 'Федоров Иван Сергеевич', 1),
    (4, 'Ронина Любовь Олеговна', 0),
    (5, 'Беляева София Васильевна', 1),
    (6, 'Саломахина София Артемовна', 1),
    (7, 'Солнцева Элла Алексеевна', 1),
    (8, 'Грудинин Владимир Викторович', 1);
     """)

## income
cursos.execute("""  INSERT INTO  income (`id`, `name`, `info`, `price`)
    VALUES
    (1, 'Членский взнос', 'Платится только членами СНТ', 100),
    (2, 'Целевой взнос', 'Платится со всех участков вне зависимости от членства в СНТ', 120);
     """)

 ## expenses 
cursos.execute(""" INSERT INTO  expenses (`id`, `name`, `info`, `price`)
    VALUES
    (1, 'Вывоз мусора', 'Заказ мусорной машины', 10),
    (2, 'Электричество', 'за 1 единицу', 1),
    (3, 'Ремонт дорог', 'за 1 участок', 100),
    (4, 'Заказ песка', '1 машина песка + доставка до участка', 50);
    """)

## average_expenses 
cursos.execute(""" INSERT INTO  average_expenses (`id`, `expense_id`, `amount`, `planned_money_amount`)
    VALUES
    (1, 1, 100, 1000),
    (2, 2, 100, 1000),
    (3, 3, 12, 1200),
    (4, 4, 2, 100);
    """)

## periods 
cursos.execute("""  INSERT INTO  periods (`id`, `startdate`, `enddate`)
    VALUES
    (1, '2021-01-01', '2021-01-31'),
    (2, '2021-02-01', '2021-02-28'),
    (3, '2021-03-01', '2021-03-31'),
    (4, '2021-04-01', '2021-04-30'),
    (5, '2021-05-01', '2021-05-31'),
    (6, '2021-06-01', '2021-06-30'),
    (7, '2021-07-01', '2021-07-31'),
    (8, '2021-08-01', '2021-08-31'),
    (9, '2021-09-01', '2021-09-30'),
    (10, '2021-10-01', '2021-10-31'),
    (11, '2021-11-01', '2021-11-30'),
    (12, '2021-12-01', '2021-12-31');
    """)

## ownership 
cursos.execute("""  INSERT INTO  ownership (`id`, `homestead_id`, `owner_id`, `owning_startdate`, `owning_enddate`, `owning_type`)
    VALUES
    (1, '1', '2', '2021-05-05', null, 'Покупка'),
    (2, '2', '3', '2021-08-04', null, 'Аренда'),
    (3, '3', '3', '2021-07-21', null, 'Наследник'),
    (4, '4', '4', '2021-07-14', null, 'Наследник'),
    (5, '5', '6', '2021-05-07', null, 'Покупка'),
    (6, '6', '5', '2021-05-02', null, 'Аренда'),
    (7, '7', '8', '2021-05-12', null, 'Наследник'),
    (8, '8', '1', '2021-04-13', null, 'Аренда'),
    (9, '9', '8', '2021-12-17', null, 'Покупка'),
    (10, '10', '7', '2021-01-02', '2021-01-30', 'Покупка');
    """)

## actual_expenses 
cursos.execute("""   INSERT INTO  actual_expenses ('id',`expense_id`, `from_homestead_id`, `amount`, `period`)
    VALUES
    (1, 1, 2, 2, 1),
    (2, 2, 1, 1, 2),
    (3, 3, 3, 4, 2),
    (4, 4, 4, 2, 4),
    (5, 2, 5, 3, 6),
    (6, 3, 6, 1, 7),
    (7, 1, 7, 1, 3),
    (8, 4, 8, 1, 8),
    (9, 2, 9, 2, 9),
    (10, 2, 10, 2, 10),
    (11, 3, 1, 1, 11),
    (12, 2, 2, 3, 12),
    (13, 2, 3, 2, 1),
    (14, 3, 4, 3, 3),
    (15, 1, 5, 10, 2),
    (16, 4, 6, 3, 4),
    (17, 4, 7, 2, 5),
    (18, 4, 8, 2, 6),
    (19, 1, 9, 20, 7),
    (20, 1, 10, 50, 8),
    (21, 4, 1, 4, 9),
    (22, 3, 2, 4, 10),
    (23, 4, 3, 4, 11),
    (24, 4, 4, 2, 12),
    (25, 2, 5, 100, 1),
    (26, 2, 6, 100, 3),
    (27, 1, 7, 200, 2),
    (28, 3, 8, 2, 4),
    (29, 3, 9, 3, 5),
    (30, 1, 10, 233, 6),
    (31, 2, 1, 2, 7),
    (32, 4, 2, 4, 8),
    (33, 4, 3, 4, 9),
    (34, 4, 4, 5, 10),
    (35, 1, 5, 60, 11),
    (36, 4, 6, 2, 12),
    (37, 2, 7, 20, 1),
    (38, 3, 8, 2, 3),
    (39, 3, 9, 1, 2),
    (40, 3, 1, 1, 4),
    (41, 4, 10, 2, 5),
    (42, 1, 2, 33, 6),
    (43, 2, 3, 2, 7),
    (44, 4, 4, 3, 8),
    (45, 1, 5, 24, 9),
    (46, 4, 6, 4, 10),
    (47, 4, 7, 4, 11),
    (48, 3, 8, 2, 12);
    """)

## income_trans     
cursos.execute("""  INSERT INTO  income_trans ('id',`income_id`, `from_homestead_id`, `amount`, `transaction_date`, `amount_of_money`)
    VALUES
    (1, 2, 1, 10, '2021-01-30', 100),
    (2, 1, 1, 20, '2021-01-16', 100),
    (3, 1, 1, 30, '2021-02-12', 100),
    (4, 1, 2, 40, '2021-04-03', 100),
    (5, 2, 1, 50, '2021-03-07', 100),
    (6, 1, 1, 60,  '2021-06-02', 100),
    (7, 2, 1, 70, '2021-07-31', 100),
    (8, 2, 1, 80,  '2021-05-04', 100),
    (9, 2, 1, 90, '2021-01-20', 100),
    (10, 2, 1, 100, '2021-01-21', 100);
    """)

connect.commit()


for row in cursos.execute(""" SELECT  expenses.name as 'Статья расходов',  price as 'Сумма'  FROM actual_expenses  JOIN expenses  ON expenses.id = actual_expenses.expense_id  JOIN periods ON periods.id = actual_expenses.period  WHERE startdate = '2021-03-01' AND enddate = '2021-03-31'  GROUP BY expense_id; """ ):
    print(*row)


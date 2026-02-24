-- SQL : Structured query Lang
-- Note SQL is case insensitive language ->> It is always recommanded to us to use upper case character for keywords.
-- 5 types : 
	-- 1. DDL (Data Definition Language)
		-- We create database/ table structure. 
        -- To make changes in database or table we use DDL
			-- commands
				-- 1. CREATE >> To create database and tables
                -- 2. ALTER  >> To make changes in the database and tables
                -- 3. TRUNCATE >> To delete the entire table data
--              -- 4. DROP >> To delete the entire table/ database
    -- 2. DML (Data Manipulation Language)
		-- We use DML to insert, update, delete the data inside a table.
    -- 3. DQL (Data Query Language)
		-- We use DQL to read the data from the table.
    -- 4. DCL (Data Control Language)
		-- We use DCL to restrict the access of a table for various operations by a user.
    -- 5. TCL (Transaction Control Language)
		-- We use this to control the flow of SQL. 
# How Exactly we store data into the database.
	# Database
		-- |
        -- |___Tables
        --      |___ Data
        
-- When we are creating a table we have to follow certain rules : 
	-- 1. The table name must be unqiue
    -- 2. The table should contain the columns (guide data)

-- Create a database --> we use DDL commands
-- Syntax : 
	-- CREATE DATABASE databasename;

CREATE DATABASE PFSJFS2025_12_03;

-- To Select a database to work with in MYSQL -- USE keyword
-- syntax : 
	-- USE databasename;
    
USE pfsjfs2025_12_03; 

-- To create a table we use CREATE keyword 
-- syntax : 
	-- CREATE TABLE tableName(colName dataType(size), ....);
-- Datatypes : 
	-- 1. String >> char/ varchar
		-- a. char : It will dedicate the memory for the given size wether we use it or not.
        -- b. varchar : it will allocate memory for the data which we gave not based on size. 
	-- 2. Number >> int/ bigint
    -- 3. Decimal >> decimal(value, decimalPlaces)
    -- 4. Boolean >> true or false
    -- 5. Datetime 
    -- 6. BLOB >> stores multimedia data. 
-- RULES : 
	-- 1. Every table must satify the normalisation. 
		-- 1NF : 
			-- Every cell must hold one value. --> atomticity
		-- 2NF : 
			-- 1NF satisfy
            -- there shouldn't be a partial dependency.
            
            -- ( A + B )  C
		-- 3NF : 
			-- 2NF satisfy
            -- There shouldn't be any transitive dependency. --> Non key attribute -- non key attribute
		-- 3.5 NF : 
			-- 3NF satisfy
            -- There shouldn't have functional dependency --> super key
		-- 4NF : 
			-- 3.5 NF
            -- There shouldn't be a multi value dependency.
		
            
    -- 2. Every table must and should have the key constraints. 
		--  apply conditions on the cols
        -- 1. primary key : It is used to find a record. (Not null + unqiue). In a table we can have only one col as primary key
        -- 2. NOT NULL : It is used to make a column to not accept null values. 
        -- 3. Unqiue : It tells the cols that should not accept the duplicate values
        -- 4. Foreign key : The pk of another table which acts as a reference in the table is called as foreign key. 
        -- 5. compsite key : combination of multiple cols to identify a record. 
        -- 6. Default : It will provide a default value to a col. 
        -- 7. Check  : It will check the value before inserting into the table.

-- Creating users table
CREATE TABLE users(
	user_id INT PRIMARY KEy,
    user_name VARCHAR(100) NOT NULL,
    user_email VARCHAR(100) NOT NULL UNIQUE,
    user_phone BIGINT NOT NULL UNIQUE
);

-- To update the table columns or name or data type of a column we use ALTER query
-- Syntax : 
	-- ALTER TABLE tableName MODIFY colName dataType...;

-- Limit the userphone col characters to 10
ALTER TABLE users MODIFY user_phone VARCHAR(10);

-- To add new columns in existing table we use ALTER with ADD 
-- syntax ;
	-- ALTER TABLE tableName ADD COLUMN colName DataType contraints;

-- Add user_city to the users table
ALTER TABLE users ADD COLUMN user_city int;

-- To delete a column from the table we use ALTER with DROP
-- Syntax : 
	-- ALTER TABLE tableName DROP COLUMN colName;

-- Remove user_city column from the table users
-- write your query here
ALTER TABLE users DROP COLUMN user_city;

-- To rename a col name we use ALTER with RENAME COLUMN
-- syntax : 
	-- ALTER TABLE tableName RENAME COLUMN oldCOlName TO newColName;
ALTER TABLE users RENAME COLUMN usercity TO user_city;

-- Inorder delete the table or database we use the drop query
-- syntax to delete table ; 
	-- DROP TABLE tableName;
-- Syntax to delete database;
	-- DROP DATABASE databaseName;

-- To insert data into the table we have to use DML command INSERT.
-- syntax to insert data into the table
	-- INSERT INTO tableName VALUES(value,....);
    
-- Truncate : 
	-- Truncate is used to delete the data from the data. 
    -- syntax : 
    -- TRUNCATE TABLE tablename;
    TRUNCATE table users;
-- DROP : 
	-- Delete the entire table.
    -- syntax : 
		-- DROP TABLE tableName;
	DROP TABLE users;
    
INSERT INTO users VALUES (1, "Adam", "adam@email.com", "8887987634");

-- If we want to insert multi values at a time all we have to do is to divide the values as a seperate set. 
-- syntax : 
	-- INSERT INTO tableName VALUES (value1,...), (value1),...;
INSERT INTO users 
VALUES
(2, "Bob", "bob@gmail.com", "9987654321"), 
(3, "Chris", "chris@gmail.com", "9984454321"), 
(4, "Eddie", "eddie@gmail.com", "9669954321");

-- If we want to insert a certain column values then we have to use the column name specifically and those values
-- syntax : 
	-- INSERT INTO tableName(colName1, colName2,...) VALUES(...);
INSERT INTO users(user_id, user_name, user_email) VALUES (5, "Franky", "franky@email.com");

-- INSERT INTO users VALUES (6, "Georg", "georg@email.com");

-- Update a record --> UPDATE commond.
-- If I want to update all the records 
	-- syntax :
		-- UPDATE tableName SET colName = value;
UPDATE users SET user_city = '1';

-- If we want to update a specific record

-- build a condition in order to target a specific record. 
-- To build a condition we need to use the comparsion operators.
-- >, <, =, <>, >=, <=
-- Clause : 
	-- Helps us to guide for what to do. 
    -- 1. Where : 
		-- It helps us to build a condition. 
			-- syntax : 
				-- DML query WHERE condition;
-- update the phonenumber for user who is having id 5 with value 8876738383
UPDATE users SET user_phone = "8876738383" WHERE user_id = 5;

-- To see the table data we use DQL -- SELECT command
-- syntax : 
	-- SELECT * FROM tableName;
SELECT * FROM users;

-- To see a specific record from the table we have to use condition for that 
-- syntax : 
	-- SELECT * FROM tableName WHERE cond;

-- Find the user data who is have email of bob@gmail.com 
SELECT * FROM users WHERE user_email = 'bob@gmail.com';

-- operators : 
-- comparison operators
-- arthe operators
-- in, between
-- logical operators -- and, or , not

--  Find the users who are having id of 1,4,3
SELECT * FROM users WHERE user_id = 1 OR user_id = 3 OR user_id = 4;


-- DELETE : Is used to delete a record from the table. 
-- Syntax : 
	-- DELETE FROM tablename WHERE condition;
    



use world;

SHOW TABLES;


-- DQL 
-- SELECT 
-- syntax : 
-- SELECT colName,... FROM tableName WHERE condition;

SELECT * FROM country;

-- Like : Used find the data based upon the pattern matching. 
-- % -- match n no.of characters
-- _ -- match 1 character

-- Find the countries, which are starting there name with n (n%)
SELECT name FROM country WHERE name LIKE 'n%';

-- Find the countries which are having population starts with 1 and the third with 3 and ends with 5
SELECT name,population FROM country WHERE population LIKE '1_3%';

-- Find the countries, which are starting there name with n and ending with d 
SELECT name FROM country WHERE name LIKE 'n%d';

-- Find the countries which doesn't belongs to Europe, Asia, Africa
SELECT name FROM country WHERE continent NOT IN ('Europe', 'Asia', 'Africa');

-- Find the name of the countries which having population of 78000, 293000, 120000,22720000, 154000, 22244000, 22455500, 6000
SELECT name FROM country WHERE population IN (78000, 293000, 120000,22720000, 154000, 22244000, 22455500, 6000);

-- Find the name of the contries which are in asia and got the independence in year between 1930 to 1965
SELECT name, indepYear  from country WHERE continent = 'Asia' AND indepYear >= 1930 AND indepYear <= 1965;

SELECT name from country WHERE continent = 'Asia' AND indepYear BETWEEN 1930 AND 1965;

-- Find the Name of the contries which is in ASIA

SELECT name FROM country WHERE continent = 'Asia';

-- Find the country name which is having population of greater than 78000. 
SELECT Name, population FROM country WHERE population >= 78000;


-- ORDER BY : used to sort out the data in a table while displaying the records. 
-- syntax : 
	-- SELECT * FROM tableName ORDER BY colName; (ascending order 1,2,3,4...)
    -- SELECT * FROM tableName ORDER BY colName DESC; (descening order)

-- Display the country names based upon the population in ascending order    
SELECT name, continent, population FROM country ORDER BY population;

-- LIMIT : It limits the no.of records to be displayed. 
-- syntax : 
	-- SELECT * FROM tableName LIMIT no.of records OFFSET start (n + 1);

SELECT * FROM country LIMIT 5 OFFSET 5;

-- Find the country which is having highest population. 
SELECT * FROM country ORDER BY population DESC LIMIT 1;

-- Find the country which is having the second highest population.
SELECT * FROM country ORDER BY population DESC LIMIT 1 OFFSET 1;

-- Aggregate Functions : 
-- Built in function which are used to perform certain operations.
-- MIN -- min value in a column
-- MAX -- max value in a column
-- AVG -- avg value of a column
-- SUM -- add all the values inside col and provide the result
-- COUNT -- total values present in the column.
-- syntax : 
	-- SELECT aggFun(colName) FROM tableName;

-- Find the entire population in this world. 
SELECT SUM(population) FROM country;

-- Find the total no of countries present in the country table. 
SELECT COUNT(name) no_of_countries FROM country;
SELECT COUNT(name) no_of_countries FROM country;




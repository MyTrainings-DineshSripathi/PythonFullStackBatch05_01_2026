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

-- To rename a col name we use ALTER with RENAME COLUMN
-- syntax : 
	-- ALTER TABLE tableName RENAME COLUMN oldCOlName TO newColName;
ALTER TABLE users RENAME COLUMN usercity TO user_city;


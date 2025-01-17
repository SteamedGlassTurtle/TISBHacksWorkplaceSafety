-- Create the 'employees' table
CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Insert 10 records into the 'employees' table
INSERT INTO employees (id, name) VALUES
(1, 'John Doe'),
(2, 'Jane Smith'),
(3, 'Alice Johnson'),
(4, 'Robert Brown'),
(5, 'Emily Davis'),
(6, 'Michael Wilson'),
(7, 'Sarah Miller'),
(8, 'David Martinez'),
(9, 'Laura Garcia'),
(10, 'James Anderson');

-- Verify the inserted data
SELECT * FROM employees;

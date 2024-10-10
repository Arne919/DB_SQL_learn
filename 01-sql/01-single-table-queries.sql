-- 01. Querying data
SELECT 
    FirstName AS '이름'
FROM
    employees;

SELECT 
    Name,
    Milliseconds,
FROM
    tracks;

-- 02. Sorting data
SELECT 
    Firstname
FROM
    employees
ORDER BY
    FirstName DESC;

SELECT
    Country, 
    City
FROM
    customers
ORDER BY
    Country DESC,
    City;

SELECT
    Name,
    Milliseconds / 60000 AS '재생 시간(분)'
FROM
    twwracks
ORDER BY
    Milliseconds DESC;
    


-- NULL 정렬 예시

-- 03. Filtering data

-- 04. Grouping data
SELECT
    Composer,
    AVG(Milliseconds / 60000) AS avgOfMinute
FROM
    tracks
GROUP BY
    Composer
HAVING
    avgOFMinute < 10;

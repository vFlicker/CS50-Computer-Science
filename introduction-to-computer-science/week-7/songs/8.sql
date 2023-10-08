/* SQL query that lists the names of the songs that feature other artists. */
SELECT
  songs.name
FROM
  songs
WHERE
  name LIKE "%feat%";
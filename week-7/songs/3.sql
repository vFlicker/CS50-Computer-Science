/* SQL query to list the names of the top 5 longest songs, in descending order of length. */
SELECT
  songs.name
FROM
  songs
ORDER BY
  songs.duration_ms DESC
LIMIT
  5;
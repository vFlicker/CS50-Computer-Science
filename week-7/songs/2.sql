/* SQL query to list the names of all songs in increasing order of tempo. */
SELECT
  songs.name
FROM
  songs
ORDER BY
  songs.tempo;
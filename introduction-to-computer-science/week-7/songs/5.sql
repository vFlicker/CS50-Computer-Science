/* SQL query that returns the average energy of all the songs. */
SELECT
  AVG(songs.energy) AS average_energy
FROM
  songs;
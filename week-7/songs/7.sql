/* SQL query that returns the average energy of songs that are by Drake. */
SELECT
  AVG(songs.energy) AS average_energy
FROM
  songs
  JOIN artists ON songs.artist_id = artists.id
WHERE
  artists.name = "Drake";
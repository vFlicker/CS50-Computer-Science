/* SQL query that lists the names of any songs that have danceability, energy, and valence greater than 0.75. */
SELECT
  songs.name
FROM
  songs
WHERE
  songs.danceability > 0.75
  AND songs.energy > 0.75
  AND songs.valence > 0.75;
/* SQL query to determine the number of movies with an IMDb rating of 10.0. */
SELECT
  COUNT(*) AS number_of_movies
FROM
  ratings
WHERE
  ratings.rating = 10.0;
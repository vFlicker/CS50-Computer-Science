/* SQL query to list the names of all people who have directed a movie that received a rating of at least 9.0. */
SELECT
  people.name
FROM
  directors
  JOIN people ON directors.person_id = people.id
  JOIN ratings ON directors.movie_id = ratings.movie_id
WHERE
  ratings.rating >= 9.0;
/*  SQL query to list the names of all people who starred in Toy Story. */
SELECT
  people.name
FROM
  stars
  JOIN movies ON stars.movie_id = movies.id
  JOIN people ON stars.person_id = people.id
WHERE
  movies.title = "Toy Story";
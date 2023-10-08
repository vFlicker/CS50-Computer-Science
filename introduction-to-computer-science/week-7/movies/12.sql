/* SQL query to list the titles of all movies in which both Bradley Cooper and Jennifer Lawrence starred. */
SELECT DISTINCT
  movies.title
FROM
  stars
  JOIN movies ON stars.movie_id = movies.id
  JOIN people ON stars.person_id = people.id
WHERE
  people.name IN ("Bradley Cooper", "Jennifer Lawrence")
GROUP BY
  movies.title
HAVING
  COUNT(people.name) = 2;
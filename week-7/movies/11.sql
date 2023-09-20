/* SQL query to list the titles of the five highest rated movies (in order) that Chadwick Boseman starred in, starting with the highest rated. */
SELECT
  movies.title
FROM
  stars
  JOIN movies ON stars.movie_id = movies.id
  JOIN people ON stars.person_id = people.id
  JOIN ratings ON stars.movie_id = ratings.movie_id
WHERE
  people.name = "Chadwick Boseman"
ORDER BY
  ratings.rating DESC
LIMIT
  5;
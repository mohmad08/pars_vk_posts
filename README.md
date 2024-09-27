<h2>SQL запросы для выводов:</h2>

<h3>1. Влияние времени суток на количество лайков</h3>

SELECT 
    EXTRACT(HOUR FROM date) AS hour_of_day, 
    AVG(likes) AS avg_likes
FROM 
    filter
GROUP BY 
    EXTRACT(HOUR FROM date)
ORDER BY 
    hour_of_day;

<h3>2. Влияние дня недели на количество лайков</h3>
   SELECT 
    EXTRACT(DOW FROM date) AS day_of_week, 
    AVG(likes) AS avg_likes
FROM 
    filter
GROUP BY 
    EXTRACT(DOW FROM date)
ORDER BY 
    day_of_week;

<h3> 3. Влияние промежутка между постами на количество лайков </h3>
   WITH ranked_posts AS (
    SELECT 
        date,
        likes,
        LAG(date) OVER (ORDER BY date) AS prev_post_datetime
    FROM 
        filter
)
SELECT 
    date,
    likes,
    EXTRACT(EPOCH FROM (date - prev_post_datetime)) / 3600 AS hours_since_last_post
FROM 
    ranked_posts
WHERE 
    prev_post_datetime IS NOT NULL;


<p> В вайле main.py находится сам парсер для страницы ВК.</p>
<p> В файле filter.csv находятся данные о постах(дата поста и количество лайков).</p>
<p> Cсылка на страницу,  которая была спарсена в файл filter.csv: "https://vk.com/python_of".</p>
<p> Далее представлены SQL запросы.</p>


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
<h1>Расчет промежутков между постами (разница во времени между текущей и предыдущей публикацией):</h1>

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
    
<h1>Группировка по промежуткам между публикациями:</h1>

WITH ranked_posts AS (
    SELECT 
        post_id,
        post_datetime,
        likes_count,
        LAG(post_datetime) OVER (ORDER BY post_datetime) AS prev_post_datetime
    FROM 
        posts
)
SELECT 
    CASE 
        WHEN EXTRACT(EPOCH FROM (date - prev_post_datetime)) / 3600 < 1 THEN '<1 hour'
        WHEN EXTRACT(EPOCH FROM (date - prev_post_datetime)) / 3600 BETWEEN 1 AND 3 THEN '1-3 hours'
        WHEN EXTRACT(EPOCH FROM (date - prev_post_datetime)) / 3600 BETWEEN 3 AND 6 THEN '3-6 hours'
        WHEN EXTRACT(EPOCH FROM (date - prev_post_datetime)) / 3600 BETWEEN 6 AND 12 THEN '6-12 hours'
        ELSE '>12 hours'
    END AS post_interval,
    AVG(likes) AS avg_likes
FROM 
    ranked_posts
WHERE 
    prev_post_datetime IS NOT NULL
GROUP BY 
    post_interval
ORDER BY 
    post_interval;


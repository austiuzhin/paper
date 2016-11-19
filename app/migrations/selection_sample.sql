SELECT *
FROM (
    SELECT obj_type
        ,COUNT(*) AS cnt
    FROM estate_items
    GROUP BY obj_type
    ) t
ORDER BY t.cnt DESC 
LIMIT 10;
FILM_BY_ID = """
    SELECT
    fw.id, fw.title, fw.description, fw.rating, fw.type,
    ARRAY_AGG(DISTINCT g.name) AS genres_names,
    ARRAY_AGG(DISTINCT p.full_name) FILTER
    (WHERE pfw.role = 'actor') AS actors_names,
    ARRAY_AGG(DISTINCT p.full_name)
    FILTER (WHERE pfw.role = 'director') AS directors_names,
    ARRAY_AGG(DISTINCT p.full_name)
    FILTER (WHERE pfw.role = 'writer') AS writers_names,
    ARRAY_AGG(
        DISTINCT
        g.id || ' : '
        || g.name || ' : '
        || COALESCE(g.description, 'EMPTY')
    ) AS genres,
    ARRAY_AGG(DISTINCT p.id || ' : ' || p.full_name)
    FILTER (WHERE pfw.role = 'director') AS directors,
    ARRAY_AGG(DISTINCT p.id || ' : ' || p.full_name)
    FILTER (WHERE pfw.role = 'actor') AS actors,
    ARRAY_AGG(DISTINCT p.id || ' : ' || p.full_name)
    FILTER (WHERE pfw.role = 'writer') AS writers
    FROM film_work as fw
    LEFT JOIN person_film_work as pfw ON pfw.film_work_id = fw.id
    LEFT JOIN person as p ON p.id = pfw.person_id
    LEFT JOIN genre_film_work as gfw ON gfw.film_work_id = fw.id
    LEFT JOIN genre g ON g.id = gfw.genre_id
    WHERE fw.id IN %s
    GROUP BY fw.id
"""

GENRE_BY_ID = """
    SELECT *
    FROM genre
    WHERE id IN %s
"""

PERSON_BY_ID = """
    SELECT
        p.id, p.full_name,
        ARRAY_AGG(DISTINCT fwp.role) AS role,
        ARRAY_AGG(
            DISTINCT CAST(fwp.film_work_id AS VARCHAR)
        ) AS film_ids,
        ARRAY_AGG(CAST(fwp.film_work_id AS VARCHAR))
        FILTER (WHERE fwp.role = 'actor') AS actor,
        ARRAY_AGG(CAST(fwp.film_work_id AS VARCHAR))
        FILTER (WHERE fwp.role = 'director') AS director,
        ARRAY_AGG(CAST(fwp.film_work_id AS VARCHAR))
        FILTER (WHERE fwp.role = 'writer') AS writer
    FROM
        person AS p
    LEFT JOIN person_film_work AS fwp ON p.id = fwp.person_id
    WHERE p.id IN %s
    GROUP BY  p.id, p.full_name
"""

STARTED_TIME = """
    SELECT modified
    FROM {table}
    ORDER BY modified
"""

UPDATE_IDS = """
    SELECT id
    FROM {table}
    WHERE modified > %s
    ORDER BY modified
    LIMIT %s
"""

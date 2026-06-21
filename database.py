

from sqlalchemy import create_engine, text

def Database_management(engine):

    with engine.begin() as conn:
        conn.execute(
            text("""
                 
                CREATE TABLE IF NOT EXISTS public.complaint_types (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS public.work_centers (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS public.suburbs (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS public.wards (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS public.sub_councils (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL
                );


                CREATE TABLE IF NOT EXISTS public.service_requests (
                    id BIGSERIAL PRIMARY KEY,
                    object_id BIGINT NOT NULL,
                    notification_number BIGINT NOT NULL,
                    notification_type TEXT,
                    complaint_type_id INT NOT NULL REFERENCES public.complaint_types(id),
                    work_center_id INT NOT NULL REFERENCES public.work_centers(id),
                    suburb_id INT NOT NULL REFERENCES public.suburbs(id),
                    ward_id INT NOT NULL REFERENCES public.wards(id),
                    sub_council_id INT NOT NULL REFERENCES public.sub_councils(id),
                    coordinate_1 DOUBLE PRECISION,
                    coordinate_2 DOUBLE PRECISION,
                    created_on_date TIMESTAMPTZ,
                    changed_on TIMESTAMPTZ,
                    completed_date TIMESTAMPTZ,
                    notifications_created INT DEFAULT 1,
                    status TEXT GENERATED ALWAYS AS (
                        CASE 
                            WHEN completed_date IS NOT NULL THEN 'Closed'
                            ELSE 'Open'
                        END
                    ) STORED
                );
                """
            )
        )
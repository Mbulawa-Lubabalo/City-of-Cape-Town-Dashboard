

from sqlalchemy import insert, text
from data_pipeline.transform import Clean_Data

def Database_management(engine):

    with engine.begin() as conn:
        conn.execute(
            text("""
                CREATE TABLE IF NOT EXISTS public.complaint_types (
                    id SERIAL PRIMARY KEY,
                    complaint_type TEXT UNIQUE NOT NULL
                );

                CREATE TABLE IF NOT EXISTS public.work_centers (
                    id SERIAL PRIMARY KEY,
                    work_center TEXT UNIQUE NOT NULL
                );
                 
                CREATE TABLE IF NOT EXISTS public.sub_councils (
                    id SERIAL PRIMARY KEY,
                    sub_council TEXT NOT NULL,
                    code TEXT UNIQUE NOT NULL
                );
                 
                CREATE TABLE IF NOT EXISTS public.wards (
                    id SERIAL PRIMARY KEY,
                    code TEXT UNIQUE NOT NULL,
                    sub_council_id INT NOT NULL,
                    CONSTRAINT fk_ward_sub_council
                        FOREIGN KEY (sub_council_id)
                        REFERENCES public.sub_councils(id)
                );

                CREATE TABLE IF NOT EXISTS public.suburbs (
                    id SERIAL PRIMARY KEY,
                    suburb TEXT UNIQUE NOT NULL,
                    ward_id INT NOT NULL,
                    CONSTRAINT fk_suburb_ward
                        FOREIGN KEY (ward_id)
                        REFERENCES public.wards(id)
                );
                CREATE TABLE IF NOT EXISTS public.suburb (
                    id SERIAL PRIMARY KEY,
                    suburb TEXT UNIQUE NOT NULL,
                    total_complaints INT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS public.service_requests (
                    id BIGSERIAL PRIMARY KEY,

                    object_id BIGINT NOT NULL,
                    notification BIGINT UNIQUE NOT NULL,
                    notification_type TEXT,

                    complaint_type_id INT NOT NULL,
                    work_center_id INT NOT NULL,
                    suburb_id INT NOT NULL,

                    coordinate_1 DOUBLE PRECISION,
                    coordinate_2 DOUBLE PRECISION,

                    created_on_date DATE,
                    changed_on DATE,
                    completed_date DATE,

                    notifications_created INT DEFAULT 1,

                    status TEXT GENERATED ALWAYS AS (
                        CASE
                            WHEN completed_date IS NOT NULL
                                AND completed_date <> '1970-01-01'
                            THEN 'Closed'
                            ELSE 'Open'
                        END
                    ) STORED,

                    CONSTRAINT fk_service_complaint_type
                        FOREIGN KEY (complaint_type_id)
                        REFERENCES public.complaint_types(id),

                    CONSTRAINT fk_service_work_center
                        FOREIGN KEY (work_center_id)
                        REFERENCES public.work_centers(id),

                    CONSTRAINT fk_service_suburb
                        FOREIGN KEY (suburb_id)
                        REFERENCES public.suburbs(id)
                );

                """
            )
        )

# def Insert_data(engine, df):
#     complaint_types_unique = df["complaint_type"].unique()

#     with engine.begin() as conn:
#         for val in complaint_types_unique:
#             conn.execute(
#                 insert(complaint_types).values(name=val).on_conflict_do_nothing()
#             )


def Insert_data(engine, df):
    # records = df.to_dict(orient="records")

    UPSERT_SQL = [
        # 1. lookups
        text("""
            INSERT INTO public.complaint_types (complaint_type)
            VALUES (:complaint_type)
            ON CONFLICT (complaint_type) DO NOTHING;
        """),
        text("""
            INSERT INTO public.work_centers (work_center)
            VALUES (:work_center)
            ON CONFLICT (work_center) DO NOTHING;
        """),
        text("""
            INSERT INTO public.sub_councils (sub_council, code)
            VALUES (:sub_council, :code)
            ON CONFLICT (code) DO NOTHING;
        """),
        text("""
            INSERT INTO public.wards (code, sub_council_id)
            SELECT :ward, sc.id
            FROM public.sub_councils sc
            WHERE sc.code = :code
            ON CONFLICT (code) DO NOTHING;
        """),
        text("""
            INSERT INTO public.suburbs (suburb, ward_id)
            SELECT :suburb, w.id
            FROM public.wards w
            WHERE w.code = :ward
            ON CONFLICT (suburb) DO NOTHING;
        """),
        # 2. fact row
        text("""
            INSERT INTO public.service_requests (
                object_id, notification, notification_type,
                complaint_type_id, work_center_id, suburb_id,
                coordinate_1, coordinate_2,
                created_on_date, changed_on, completed_date,
                notifications_created
            )
            SELECT
                :object_id, :notification, :notification_type,
                ct.id, wc.id, s.id,
                :coordinate_1, :coordinate_2,
                :created_on_date,
                :changed_on,
                CASE WHEN :completed_date IS NULL THEN NULL
                    ELSE :completed_date END,
                :notifications_created
            FROM public.complaint_types ct
            JOIN public.work_centers   wc ON wc.work_center   = :work_center
            JOIN public.suburbs        s  ON s.suburb         = :suburb
            WHERE ct.complaint_type = :complaint_type
            ON CONFLICT (notification) DO UPDATE SET
                changed_on     = EXCLUDED.changed_on,
                completed_date = EXCLUDED.completed_date;
        """),
    ]


    records = df.to_dict(orient="records")
    with engine.begin() as conn:
        for row in records:
            for stmt in UPSERT_SQL:
                conn.execute(stmt, row)
        # # complaint_types
        # conn.execute(insert(ComplaintTypes), records_for_complaint_types)

        # # work_centers
        # conn.execute(insert(WorkCenters), records_for_work_centers)

        # # suburbs
        # conn.execute(insert(Suburbs), records_for_suburbs)

        # # wards
        # conn.execute(insert(Wards), records_for_wards)

        # # sub_councils
        # conn.execute(insert(SubCouncils), records_for_sub_councils)

def vw_service_requests(engine):

    sql = text("""CREATE OR REPLACE VIEW public.vw_service_requests AS
    SELECT
        sr.id,
        sr.object_id,
        sr.notification,
        ct.complaint_type,
        wc.work_center,
        s.suburb,
        w.code AS ward,
        sc.sub_council,
        sr.created_on_date,
        sr.completed_date,
        sr.status
    FROM service_requests sr
    JOIN complaint_types ct
        ON sr.complaint_type_id = ct.id
    JOIN work_centers wc
        ON sr.work_center_id = wc.id
    JOIN suburbs s
        ON sr.suburb_id = s.id
    JOIN wards w
        ON s.ward_id = w.id
    JOIN sub_councils sc
        ON w.sub_council_id = sc.id;
               """)
    
    with engine.begin() as conn:
        conn.execute(sql)


def queries(engine):
    sql = [
        text("""
        CREATE OR REPLACE VIEW public.vw_suburbs AS
        SELECT
            s.suburb,
            COUNT(sr.id) AS total_complaints
        FROM public.vw_service_requests sr
        JOIN public.suburbs s
            ON sr.suburb = s.suburb
        GROUP BY s.suburb
        ORDER BY total_complaints DESC
        LIMIT 8;
               """),
        text(
        """
        CREATE OR REPLACE VIEW public.vw_complaints_per_month AS
        SELECT
            DATE_TRUNC('day', created_on_date) AS day,
            COUNT(id) AS total_complaints
        FROM public.vw_service_requests
        WHERE EXTRACT(MONTH FROM created_on_date) = 4
        GROUP BY day
        ORDER BY day;
        """
        ),
        text("""
        CREATE OR REPLACE VIEW public.vw_april_kpi AS
        SELECT
            COUNT(id) 
                FILTER (WHERE EXTRACT(MONTH FROM created_on_date) = 4) 
            AS april_total_complaints,
            SUM(CASE WHEN status = 'Closed' THEN 1 ELSE 0 END) 
                FILTER (WHERE EXTRACT(MONTH FROM created_on_date) = 4) 
            AS completed_complaints,
            SUM(CASE WHEN status = 'Open' THEN 1 ELSE 0 END) 
                FILTER (WHERE EXTRACT(MONTH FROM created_on_date) = 4) 
            AS open_complaints,
            ROUND(AVG(completed_date - created_on_date) 
                FILTER (WHERE completed_date IS NOT NULL AND completed_date <> DATE '1970-01-01'))
            AS avg_resolution_days

        FROM public.vw_service_requests;
    """)

    ]
    
    # with engine.connect() as conn:
    #     result = conn.execute(sql)
    #     print(result.fetchall())
    with engine.begin() as conn:
        # for row in records:
        for stmt in sql:
            conn.execute(stmt)
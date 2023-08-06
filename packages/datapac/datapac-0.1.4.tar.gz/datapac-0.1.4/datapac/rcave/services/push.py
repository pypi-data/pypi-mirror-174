from datapac.config import Environment
from datapac.package.package import Package
from datapac.rcave.sources.postgres import client as pg_client
from datapac.rcave.sources.s3 import client as s3_client


def push(env: Environment, pkg: Package):
    pg_artefacts = [a for a in pkg.artefacts if a.source == "postgres"]
    s3_artefacts = [a for a in pkg.artefacts if a.source == "s3"]

    with (
        pg_client.connect(env.sources.postgres) as pg_conn,
        s3_client.connect(env.sources.s3) as s3_conn,
    ):
        for artefact in pg_artefacts:
            print(f"[source:postgres] pushing {artefact.table} artefact")
            pg_client.insert(pg_conn, artefact.table, artefact.data)

        for artefact in s3_artefacts:
            print(f"[source:s3] pushing {artefact} artefact")
            s3_client.upload(s3_conn, artefact.bucket, artefact.key, artefact.tmp_path)

        pg_conn.commit()
        # s3_conn.commit()

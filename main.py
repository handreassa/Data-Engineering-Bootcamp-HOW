import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://root:root@localhost/test_db')

sql = '''select * from vw_artist;'''

df_artist = pd.read_sql_query(sql, engine)

df_song = pd.read_sql_query('select * from vw_song;',engine)

sql = '''
insert into tb_artist (
select
	t1."date",
	t1."rank",
	t1.artist,
	t1.song
from public."Billboard" t1
where t1.artist like 'Nirvana'
order by 1, 2,3 );
'''

engine.execute(sql)
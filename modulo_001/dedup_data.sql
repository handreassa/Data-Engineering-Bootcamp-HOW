with cte_dedup_artist as (
select 
t1."date",
t1."rank",
t1.artist,
row_number() over (partition by artist order by artist,"date") as "dedup"
from public."Billboard" t1
order by t1.artist, t1."date"
)
select 
t1."date",
t1."rank",
t1.artist artist from cte_dedup_artist as t1
where dedup = 1;


-- Criação de tabela:
create table tb_web_site as ( with cte_dedup_artist as (
select
	t1."date",
	t1."rank",
	t1.artist,
	row_number() over (partition by artist
order by
	artist,
	"date") as "dedup"
from
	public."Billboard" t1
order by
	t1.artist,
	t1."date" )
select
	t1."date",
	t1."rank",
	t1.artist artist
from
	cte_dedup_artist as t1
where
	dedup = 1 );


select * from tb_web_site;


create table tb_artist as (
select
	t1."date",
	t1."rank",
	t1.artist,
	t1.song
from public."Billboard" t1
where t1.artist like 'AC/DC'
order by 1, 2,3 
);

select * from tb_artist;


create view vw_artist as (
with cte_dedup_artist as (
select
	t1."date",
	t1."rank",
	t1.artist,
	row_number() over (partition by artist
order by
	artist,
	"date") as "dedup"
from
	public.tb_artist t1
order by
	t1.artist,
	t1."date" )
select
	t1."date",
	t1."rank",
	t1.artist artist
from
	cte_dedup_artist as t1
where
	dedup = 1 
);

select * from vw_artist;


insert into tb_artist (
select
	t1."date",
	t1."rank",
	t1.artist,
	t1.song
from public."Billboard" t1
where t1.artist like 'Elvis%'
order by 1, 2,3 );







create view vw_song as (
with cte_dedup_artist as (
select
	t1."date",
	t1."rank",
	t1.artist,
	t1.song,
	row_number() over (partition by artist, song order by artist, song, "date") as "dedup"
from
	public.tb_artist t1
order by
	t1.artist,
	t1.song,
	t1."date" )
select
	t1."date",
	t1."rank",
	t1.artist ,
	t1.song
from
	cte_dedup_artist as t1
where
	dedup = 1 
);

select * from vw_song;



insert into tb_artist (
select
	t1."date",
	t1."rank",
	t1.artist,
	t1.song
from public."Billboard" t1
where t1.artist like 'Adele%'
order by 1, 2,3 );

select * from vw_artist;
select * from vw_song;
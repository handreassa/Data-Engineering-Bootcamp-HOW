CREATE TABLE public."Billboard1" (
 "date" date NULL,
 "rank" int4 NULL,
 song varchar(300) NULL,
 artist varchar(300) NULL,
 "last-week" float8 NULL,
 "peak-rank" int4 NULL,
 "weeks-on-board" int4 NULL
);

--Dados carregados a partir de:
--https://www.kaggle.com/dhruvildave/billboard-the-hot-100-songs

select
	TBB."date",
	TBB."rank",
	TBB.song,
	TBB.artist,
	TBB."last-week",
	TBB."peak-rank",
	TBB."weeks-on-board"
from
	"Billboard" as TBB
limit 10;

--Data mais recente de informação
select max("date") from "Billboard" b

--Data mais antiga de informação
select min("date") from "Billboard" b

--Dados da semana mais recente na tabela
select
	TBB."date",
	TBB."rank",
	TBB.song,
	TBB.artist,
	TBB."last-week",
	TBB."peak-rank",
	TBB."weeks-on-board"
from
	"Billboard" as TBB
where
	TBB."date" = (
	select
		max("date")
	from
		"Billboard" b);
-- Filtrar total de músicas do Chuck Berry	
select
	b.artist,
	b.song,
	count(1) as total
from
	"Billboard" b
where
	b.artist like any (array['%Chuck%Berry%',
	'%Frankie Vaughan%'])
group by
	1,
	2
order by
	total desc;



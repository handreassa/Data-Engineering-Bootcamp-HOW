select
distinct
	TBB.artist,
	TBB.song
from
	"Billboard" as TBB
order by 1, 2
;

select
	TBB.artist,
	count(1) as total
from
	"Billboard" as TBB
group by
	1
order by
	2 desc ;


select
	TBB.song,
	count(1) as total
from
	"Billboard" as TBB
group by
	1
order by
	2 desc ;


select
	distinct t1.artist,
	t1.song,
	t2.total as total_artist,
	t3.total as total_song
from
	"Billboard" as t1
left join (
	select
		TBB.artist,
		count(1) as total
	from
		"Billboard" as TBB
	group by
		1 ) as t2 on
	t1.artist = t2.artist
left join (
	select
		TBB.song,
		count(1) as total
	from
		"Billboard" as TBB
	group by
		1) as t3 on
	t1.song = t3.song
order by
	1,
	2;

-- Fazendo o uso de CTEs

with cte_artist as (select
		TBB.artist,
		count(1) as total
	from
		"Billboard" as TBB
	group by
		1),
cte_song as (	select
		TBB.song,
		count(1) as total
	from
		"Billboard" as TBB
	group by
		1)
select
	distinct t1.artist,
	t1.song,
	t2.total as total_artist,
	t3.total as total_song
from
	"Billboard" as t1
left join cte_artist as t2 on
	t1.artist = t2.artist
left join cte_song as t3 on
	t1.song = t3.song
order by
	1,
	2;


------------------------------------------------------------------------

-- Window function

with cte_billboard as (
select
	distinct t1.artist,
	t1.song,
	row_number() over(
	order by artist,
	song) as "row_number",
	row_number() over(partition by artist
order by
	artist,
	song) as "row_number_artist"
from
	public."Billboard" t1
order by
	1,
	2)
select
	*
from
	cte_billboard
where
	"row_number_artist" = 1


--rank
with cte_billboard as (
select
	distinct t1.artist,
	t1.song
from
	public."Billboard" t1
order by
	1,
	2)
select
	*, row_number() over(order by artist, song) as "row_number",
	row_number() over(partition by artist order by 	artist,	song) as "row_number_artist",
	rank() over (partition by artist order by artist, song) as "rank",
	lag(song,1) over (partition by artist order by artist, song) as "lag_song",
	lead(song,1) over (partition by artist order by artist, song) as "lead_song",
	first_value(song) over (partition by artist order by artist, song) as "first_song",
	last_value(song) over (partition by artist order by artist, song range between unbounded preceding and unbounded following) as "last_song"
from
	cte_billboard

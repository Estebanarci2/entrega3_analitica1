/* Integrantes: FABER ESTEBAN ARCILA GALVIS, ANA MARÍA OSPINA ARREDONDO, ALEJANDRO VALENCIA OCHOA */

/*Para correr correctamente los códigos se debe considerar crear las tablas como:
nba_stats, nba_combine y nba_birth, y reemplazar los '***' con la dirección del proyecto para cada vez que se cite un dataset 

/* 1. ¿Cuál es la edad promedio de los jugadores para cada cantidad de temporadas jugadas?*/
SELECT t1.col_Yrs, AVG(t2.Age) AS edad_promedio FROM `***.nba_birth` t1
INNER JOIN  `***.nba_stats` t2 on t1.col_Player = t2.Player 
GROUP BY t1.col_Yrs;

/* 2. ¿Cuántos años tienen los jugadores que llevan entre 14 y 16 años jugando?*/ 
SELECT t1.col_Player, t1.col_Yrs FROM `***.nba_birth` t1
INNER JOIN `***.nba_stats` t2 on t1.col_Player = t2.Player
WHERE t1.col_Yrs between 14 and 16;

/* 3. ¿Cuántos jugadores han jugado en la posición C?*/
SELECT * FROM `***.nba_stats`;
select count(1) as JugadoresPosiconC
from `***.nba_stats` 
where Pos = 'C';

/* 4. ¿Cuántos jugadores hay por posición jugada?*/
select Pos, count(1) from `***.nba_stats`
where Pos is not null
group by Pos;

/* 5. ¿Qué jugador tiene más de 100 goles de campo?*/
SELECT * FROM `***.nba_stats` WHERE FG> 100;

/* 6. ¿Cuáles son los 10 jugadores más altos ?*/
select Player, sum(Height__No_Shoes_) as altura_sin_tennis from `***.nba_combine`
group by Player
having altura_sin_tennis >= 81.25
order by altura_sin_tennis desc;

/* 7. ¿Cuáles son los estados que más jugadores tiene?*/
SELECT col_State, COUNT(col_City) AS cantidad FROM `***.nba_birth`
GROUP BY col_State
ORDER BY cantidad DESC;

/* 8. ¿Cuál es el peso promedio de los jugadores nacidos en cada ciudad? */
SELECT t1.col_City, AVG(t2.Weight) AS peso_promedio FROM `***.nba_birth` t1
INNER JOIN `***.nba_combine` t2 on t1.col_Player = t2.Player
GROUP BY t1.col_City
ORDER BY t1.col_City DESC;

/* 9. ¿Cuántos jugadores nacieron en cada año? */
WITH Birth AS(
  SELECT RIGHT(col_Date, 4) AS Year, col_Yrs FROM `***.nba_birth` 
  WHERE col_Date IS NOT null AND col_Date not in ('Date')
)
SELECT Year, COUNT(1) AS Cantidad FROM Birth 
GROUP BY Year
ORDER BY Cantidad DESC;

/* 10. ¿Qué jugadores que pesan más de 200 libras tienen un promedio de más de 2.5 faltas personales?*/
select t1.Player as Jugador, t2.Weight as Peso, AVG(t1.PF) as Faltas, 
from `***.nba_stats` t1 
join `***.nba_combine` t2 
on t1.Player = t2.Player
where t2.Weight >= 200 and t1.PF >= 2.5
group by Player, Weight, PF;

/* 11. ¿Cuales jugadores con la primera letra “A” en el nombre han jugado más partidos?*/
SELECT Player,G  FROM `***.nba_stats` 
WHERE LEFT(Player,1) = 'A'
ORDER BY G DESC;

/* 12. ¿Cuántos jugadores pertenecen al equipo de NYK y quién es el que más partidos tiene?*/
select Tm, Player, sum(G) as partidos from `***.nba_stats`
where Tm = "NYK"
group by Tm, Player
order by sum(G) desc;

/* 13. ¿Cuál es el peso promedio de los jugadores según su edad?*/
SELECT t1.Age, AVG(t2.Weight) AS peso_promedio FROM `***.nba_stats` t1
INNER JOIN `***.nba_combine` t2 ON t1.Player = t2.Player
GROUP BY t1.Age
ORDER BY peso_promedio DESC;

/* 14. ¿Cuál es el promedio de puntos anotados por cada posición? Ordenarlos de menor a mayor*/
select Pos, avg(PTS) as puntos_prom from `***.nba_stats`
where Pos is not null
group by Pos
order by puntos_prom asc;

/* 15. ¿Cuál fue la altura promedio con y sin zapatos en el draft del 2012 de los primeros 15 draft picks?*/
select Draft_pick,avg(Height__No_Shoes_) as alt_prom_Descalzo, avg(Height__With_Shoes_) as alt_prom_Zapatos
from `***.nba_combine`
where draft_pick <= 15
group by Draft_pick
order by Draft_pick asc;

/* 16. ¿Cuál es el peso y grasa corporal promedio de los primeros 5 draft_pick 2012?*/
select Draft_pick, avg(Weight) as Peso, avg(Body_Fat) as grasa_corporal
from `***.nba_combine`
where Draft_pick <= 5
group by Draft_pick
order by Draft_pick asc;

/* 17. ¿Qué jugadores actuales hicieron parte del draft del 2012?*/
select t1.Player, t2.Player from `***.nba_stats` t1 
join `***.nba:combine` t2 
on t1.Player = t2.Player
group by t1.Player, t2.Player;

/* 18. ¿Cuál es el jugador con el mejor promedio de anotaciones, y a qué equipo pertenecía en ese momento?*/
select Player as jugador, Tm as Equipo, avg(PTS) as puntos from `***.nba_stats`
where Player in ("Luka Dončić") 
group by Player, Tm
order by puntos desc;

/* 19. ¿Cuáles son los 3 equipos que más puntos han anotado en promedio, y cuántos jugadores le han aportado anotaciones?*/
select Tm as Equipo, avg(PTS) as prom_puntos, count(1) as jugadores_anotadores from `***.nba_stats`
where Tm in ("GSW", "NOP", "PHO") 
group by tm
order by prom_puntos desc;

/* 20. ¿Cuál es el promedio ACTUAL de anotaciones de 3 puntos que tienen los jugadores del Drift del 2012?*/
select t1.Player, _3P, count(distinct(_3P)) as puntos_D3 from `***.nba_stats` t1 
join `***.nba_combine` t2 
on t1.Player = t2.Player
group by t1.Player, _3P
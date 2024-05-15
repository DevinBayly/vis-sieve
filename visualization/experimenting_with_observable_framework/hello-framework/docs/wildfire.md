---
sql:
    treeStatus: ./data/FTM_trees.csv
---
# Tree stuff and SQL


```sql
DESCRIBE treeStatus
```

```sql
SELECT genus,yr0status,AVG(Times_burned)  from treeStatus
group by genus, yr0status
```

```sql id=plotdata display
select 
 YrFireName, 
 '1' as year, 
 if (yr1status ='1','alive','dead') as status
from treeStatus
union all 
select 
 YrFireName, 
 '2' as year, 
 if (yr1status ='1','alive','dead') as status
from treeStatus
union all 
select 
 YrFireName, 
 '3' as year, 
 if (yr3status ='1','alive','dead') as status
from treeStatus
union all 
select 
 YrFireName, 
 '4' as year, 
 if (yr1status ='4','alive','dead') as status
from treeStatus
union all 
select 
 YrFireName, 
 '5' as year, 
 if (yr1status ='5','alive','dead') as status
from treeStatus
union all 
select 
 YrFireName, 
 '6' as year, 
 if (yr1status ='6','alive','dead') as status
from treeStatus
union all 
select 
 YrFireName, 
 '7' as year, 
 if (yr1status ='7','alive','dead') as status
from treeStatus
union all 
select 
 YrFireName, 
 '8' as year, 
 if (yr1status ='8','alive','dead') as status
from treeStatus
union all 
select 
 YrFireName, 
 '9' as year, 
 if (yr1status ='9','alive','dead') as status
from treeStatus
union all 
select 
 YrFireName, 
 '10' as year, 
 if (yr1status ='10','alive','dead') as status
from treeStatus
```

```sql
SELECT 
case
when yr1status ='1' then 'alive'
else 'dead'
end
as status
from treeStatus
```

```js
Plot.plot({
    marks:[
        Plot.barY(
            plotdata,
            Plot.groupX({y:"count"},{x:"year",fill:"status",fx:"YrFireName"})
        )
    ]
})
```
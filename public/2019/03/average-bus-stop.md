title: The average bus stop
description: Where is the average bus stop in the UK?
date: 2019-03-08

# The average bus stop

The excellent [diamond geezer](https://diamondgeezer.blogspot.com/) recently calculated [London's most average bus stop, geographically speaking](https://diamondgeezer.blogspot.com/2019/03/londons-most-geographically-average.html) using data from [a FoI response from TfL](https://tfl.gov.uk/corporate/transparency/freedom-of-information/foi-request-detail?referenceId=FOI-1633-1819).

But TfL aren't the only people who list all the bus stops. There's also [National Public Transport Access Nodes (NaPTAN)](https://data.gov.uk/dataset/ff93ffc1-6656-47d8-9155-85ea0b8f2251/national-public-transport-access-nodes-naptan), a UK-wide list of all transit stops.

## Where's the average bus stop for the whole UK?

I run [buildmorebuslanes.com](https://buildmorebuslanes.com/) ([code](https://github.com/h2g2bob/traveline-data)),
so I happen to have this information in a database table:

```
travelinedata=> with
by_lat as (
        select latitude, longitude, name, rank() over (order by latitude) from naptan
),
by_lon as (
        select latitude, longitude, name, rank() over (order by longitude) from naptan
)
select 'lat', latitude as value, name, latitude, longitude
        from by_lat
        where rank = (select count(*) from naptan)::int/2
union
select 'lon', longitude as value, name, latitude, longitude
        from by_lon
        where rank = (select count(*) from naptan)::int/2
order by 1;

 ?column? |  value   |          name           | latitude | longitude 
----------+----------+-------------------------+----------+-----------
 lat      |   52.606 | Lancaster School        |   52.606 |  -1.12355
 lat      |   52.606 | Moat House Lane East    |   52.606 |  -2.06927
 lon      | -1.76065 | Somerset Road Broadgate |  53.6405 |  -1.76065
(3 rows)
```

The location of this is [a field near Bangley Lane, Lichfield](https://www.openstreetmap.org/search?query=52.606%2C-1.76065#map=17/52.60600/-1.76065).

Using these co-ordinates, the nearest bus stop is:

```
travelinedata=> select * from naptan order by abs(-1.76065 - longitude) + abs(52.606 - latitude) asc limit 3;
 atcocode_id |   code   |        name         | latitude | longitude 
-------------+----------+---------------------+----------+-----------
      221103 |          | Gainsborough Avenue |  52.6136 |  -1.74121
      223852 | stagmtdt | Gainsborough Drive  |  52.6136 |  -1.74113
      221102 |          | Gainsborough Drive  |  52.6146 |   -1.7402
(3 rows)
```

It looks like Gainsborough Avenue doesn't really exist, so this is the nearest one really [Gainsborough Drive, Mile Oak](https://www.openstreetmap.org/node/533882982)

## So, um, about that choice of co-ordinate axes...?

We took the median lattitude and median longitude. But there's no good reason for that: we could have picked any other (orthogonal) axes.

What if we rotated our axes by 45° (`τ/8`)? Would that affect our result?

Let's define some rotated axes:

- `slantitude = sin(τ/8)*latitude + cos(τ/8)*longitude = (latitude + longitude) / sqrt(2)`
- `songitude = sin(-τ/8)*latitude + cos(-τ/8)*longitude = (latitude - longitude) / sqrt(2)`

The `sqrt(2)` scaling factors don't matter, so let's do some queries:

```
travelinedata=> with
naptan_transformed as (
        select
                latitude + longitude as slantitude,
                latitude - longitude as songitude,
                name
        from naptan
),
by_slant as (
        select slantitude, songitude, name, rank() over (order by slantitude) from naptan_transformed
),
by_song as (
        select slantitude, songitude, name, rank() over (order by songitude) from naptan_transformed
)
select 'slant', slantitude  as value, name, slantitude, songitude
        from by_slant
        where rank = (select count(*) from naptan_transformed)::int/2
union
select 'song', songitude as value, name, slantitude, songitude
        from by_song
        where rank = (select count(*) from naptan_transformed)::int/2
order by 1;
 ?column? |  value  |      name       | slantitude | songitude 
----------+---------+-----------------+------------+-----------
 slant    | 51.2967 | Belsize Road    |    51.2967 |   52.2001
 song     | 54.5401 | Masons Cottages |    51.9507 |   54.5401
(2 rows)

travelinedata=> with
naptan_transformed as (
        select
                latitude + longitude as slantitude,
                latitude - longitude as songitude,
                *
        from naptan
)
select * from naptan_transformed order by abs(51.2967 - slantitude) + abs(54.5401 - songitude) asc limit 5;
 slantitude | songitude | atcocode_id |   code   |     name      | latitude | longitude 
------------+-----------+-------------+----------+---------------+----------+-----------
    51.2914 |   54.5385 |       43790 | dbsadpjp | Trusley Manor |   52.915 |  -1.62355
    51.2974 |   54.5629 |       43776 | dbsgtadw | Osleston Hall |  52.9301 |  -1.63273
    51.2968 |   54.5149 |       43754 | dbsgwpdt | Main Street   |  52.9059 |  -1.60905
    51.3239 |   54.5395 |       46166 | dbsgdatd | Black Cow     |  52.9317 |  -1.60779
     51.313 |   54.5655 |       47772 | dbsdtjdg | Church        |  52.9393 |  -1.62627
(5 rows)
```

Ignoring bus stops which aren't in use (I think?), the closest one is [Long Lane village church](https://www.openstreetmap.org/search?query=52.9393,-1.62627#map=19/52.93930/-1.62627) in Derbyshire.

This is about 50km away - about the diamater of the M25! Wowzers!

## A tale of two villages

Long Lane village has one bus per day (below the threshold for the [default map view](https://buildmorebuslanes.com/#DE65BE)).

Meanwhile, in Mile Oak, Lichfield, there are [4 buses an hour going by, traveling at over 27mph](https://buildmorebuslanes.com/#B783EA).
That's a _very_ good service for a small village. 

That service is the [Arriva Midlands service 110](https://www.arrivabus.co.uk/midlands/services/110---sapphire---tamworth-to-birmingham/?direction=outbound),
going Tamworth to Birmingham.

The [network service map](https://www.arrivabus.co.uk/globalassets/documents/multi-journey-saver-tickets/midlands/tamworth-and-lichfield-network-map-jan-2019-web.pdf)
suggests this is for commuters in Sutton Coldfield going to Tamworth. Mile Oak just happens to be on the road between them.

The difference between 1 bus a day or 50 buses a day? It really pays to ["be on the way"](https://humantransit.org/2009/04/be-on-the-way.html), as Jarett Walker would put it.

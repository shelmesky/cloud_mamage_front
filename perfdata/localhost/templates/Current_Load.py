#coding: utf-8
#!/usr/bin/python

# Current_Load in 4 hours
hours4="""
-n DEFAULT:9:'/home/max/.fonts/MSYH.TTF' \
--font-render-mode normal \
--graph-render-mode normal \
--slope-mode \
-t "CPU负载   4小时之前的数据" \
-v "CPU负载" \
-w 650 -h 120 \
--start  now-4h \
-x MINUTE:5:HOUR:1:HOUR:1:0:'%H:%M' \
DEF:value1={{ rrd_file }}:1:AVERAGE \
DEF:value2={{ rrd_file }}:2:AVERAGE \
DEF:value3={{ rrd_file }}:3:AVERAGE \
COMMENT:"\\n" \
COMMENT:"\\t\\t\\t当前值\\t\\t平均值\\t\\t最大值\\t\\t最小值\\n" \
COMMENT:"\\n" \
AREA:value1#00ff00:"5分钟负载" \
GPRINT:value1:LAST:%13.2lf \
GPRINT:value1:AVERAGE:%13.2lf \
GPRINT:value1:MAX:%13.2lf \
GPRINT:value1:MIN:%13.2lf \
COMMENT:"\\n" \
LINE2:value2#ff0000:"10分钟负载" \
GPRINT:value2:LAST:%13.2lf \
GPRINT:value2:AVERAGE:%13.2lf \
GPRINT:value2:MAX:%13.2lf \
GPRINT:value2:MIN:%13.2lf \
COMMENT:"\\n" \
LINE2:value3#000fff:"15分钟负载" \
GPRINT:value3:LAST:%13.2lf \
GPRINT:value3:AVERAGE:%13.2lf \
GPRINT:value3:MAX:%13.2lf \
GPRINT:value3:MIN:%13.2lf \
COMMENT:"\\n" \
COMMENT:"最后更新时间 \:$(date '+%Y-%m-%d %H\:%M')\\n" \
COMMENT:"\\n" \
COMMENT:"\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t嘉值云计算"  \
"""

hours25 = """
-n DEFAULT:9:'/home/max/.fonts/MSYH.TTF' \
--font-render-mode normal \
--graph-render-mode normal \
--slope-mode \
-t "CPU负载   25小时之前的数据" \
-v "CPU负载" \
-w 650 -h 120 \
--start  now-25h \
-x MINUTE:15:HOUR:1:HOUR:1:0:'%H' \
DEF:value1={{ rrd_file }}:1:AVERAGE \
DEF:value2={{ rrd_file }}:2:AVERAGE \
DEF:value3={{ rrd_file }}:3:AVERAGE \
COMMENT:"\\n" \
COMMENT:"\\t\\t\\t当前值\\t\\t平均值\\t\\t最大值\\t\\t最小值\\n" \
COMMENT:"\\n" \
AREA:value1#00ff00:"5分钟负载" \
GPRINT:value1:LAST:%13.2lf \
GPRINT:value1:AVERAGE:%13.2lf \
GPRINT:value1:MAX:%13.2lf \
GPRINT:value1:MIN:%13.2lf \
COMMENT:"\\n" \
LINE2:value2#ff0000:"10分钟负载" \
GPRINT:value2:LAST:%13.2lf \
GPRINT:value2:AVERAGE:%13.2lf \
GPRINT:value2:MAX:%13.2lf \
GPRINT:value2:MIN:%13.2lf \
COMMENT:"\\n" \
LINE2:value3#000fff:"15分钟负载" \
GPRINT:value3:LAST:%13.2lf \
GPRINT:value3:AVERAGE:%13.2lf \
GPRINT:value3:MAX:%13.2lf \
GPRINT:value3:MIN:%13.2lf \
COMMENT:"\\n" \
COMMENT:"最后更新时间 \:$(date '+%Y-%m-%d %H\:%M')\\n" \
COMMENT:"\\n" \
COMMENT:"\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t嘉值云计算"  \
"""

week1 = """
-n DEFAULT:9:'/home/max/.fonts/MSYH.TTF' \
--font-render-mode normal \
--graph-render-mode normal \
--slope-mode \
-t "CPU负载   1星期之前的数据" \
-v "CPU负载" \
-w 650 -h 120 \
--start  now-1week \
-x HOUR:2:HOUR:24:HOUR:24:0:'%A' \
DEF:value1={{ rrd_file }}:1:AVERAGE \
DEF:value2={{ rrd_file }}:2:AVERAGE \
DEF:value3={{ rrd_file }}:3:AVERAGE \
COMMENT:"\\n" \
COMMENT:"\\t\\t\\t当前值\\t\\t平均值\\t\\t最大值\\t\\t最小值\\n" \
COMMENT:"\\n" \
AREA:value1#00ff00:"5分钟负载" \
GPRINT:value1:LAST:%13.2lf \
GPRINT:value1:AVERAGE:%13.2lf \
GPRINT:value1:MAX:%13.2lf \
GPRINT:value1:MIN:%13.2lf \
COMMENT:"\\n" \
LINE2:value2#ff0000:"10分钟负载" \
GPRINT:value2:LAST:%13.2lf \
GPRINT:value2:AVERAGE:%13.2lf \
GPRINT:value2:MAX:%13.2lf \
GPRINT:value2:MIN:%13.2lf \
COMMENT:"\\n" \
LINE2:value3#000fff:"15分钟负载" \
GPRINT:value3:LAST:%13.2lf \
GPRINT:value3:AVERAGE:%13.2lf \
GPRINT:value3:MAX:%13.2lf \
GPRINT:value3:MIN:%13.2lf \
COMMENT:"\\n" \
COMMENT:"最后更新时间 \:$(date '+%Y-%m-%d %H\:%M')\\n" \
COMMENT:"\\n" \
COMMENT:"\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t嘉值云计算"  \
"""

month1 = """
-n DEFAULT:9:'/home/max/.fonts/MSYH.TTF' \
--font-render-mode normal \
--graph-render-mode normal \
--slope-mode \
-t "CPU负载   1个月之前的数据" \
-v "CPU负载" \
-w 650 -h 120 \
--start  now-1month \
-x HOUR:6:HOUR:24:HOUR:24:0:'%d' \
DEF:value1={{ rrd_file }}:1:AVERAGE \
DEF:value2={{ rrd_file }}:2:AVERAGE \
DEF:value3={{ rrd_file }}:3:AVERAGE \
COMMENT:"\\n" \
COMMENT:"\\t\\t\\t当前值\\t\\t平均值\\t\\t最大值\\t\\t最小值\\n" \
COMMENT:"\\n" \
AREA:value1#00ff00:"5分钟负载" \
GPRINT:value1:LAST:%13.2lf \
GPRINT:value1:AVERAGE:%13.2lf \
GPRINT:value1:MAX:%13.2lf \
GPRINT:value1:MIN:%13.2lf \
COMMENT:"\\n" \
LINE2:value2#ff0000:"10分钟负载" \
GPRINT:value2:LAST:%13.2lf \
GPRINT:value2:AVERAGE:%13.2lf \
GPRINT:value2:MAX:%13.2lf \
GPRINT:value2:MIN:%13.2lf \
COMMENT:"\\n" \
LINE2:value3#000fff:"15分钟负载" \
GPRINT:value3:LAST:%13.2lf \
GPRINT:value3:AVERAGE:%13.2lf \
GPRINT:value3:MAX:%13.2lf \
GPRINT:value3:MIN:%13.2lf \
COMMENT:"\\n" \
COMMENT:"最后更新时间 \:$(date '+%Y-%m-%d %H\:%M')\\n" \
COMMENT:"\\n" \
COMMENT:"\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t嘉值云计算"  \
"""

year1 = """
-n DEFAULT:9:'/home/max/.fonts/MSYH.TTF' \
--font-render-mode normal \
--graph-render-mode normal \
--slope-mode \
-t "CPU负载   1年之前的数据" \
-v "CPU负载" \
-w 650 -h 120 \
--start  now-1year \
-x MONTH:1:MONTH:1:MONTH:1:0:'%B' \
DEF:value1={{ rrd_file }}:1:AVERAGE \
DEF:value2={{ rrd_file }}:2:AVERAGE \
DEF:value3={{ rrd_file }}:3:AVERAGE \
COMMENT:"\\n" \
COMMENT:"\\t\\t\\t当前值\\t\\t平均值\\t\\t最大值\\t\\t最小值\\n" \
COMMENT:"\\n" \
AREA:value1#00ff00:"5分钟负载" \
GPRINT:value1:LAST:%13.2lf \
GPRINT:value1:AVERAGE:%13.2lf \
GPRINT:value1:MAX:%13.2lf \
GPRINT:value1:MIN:%13.2lf \
COMMENT:"\\n" \
LINE2:value2#ff0000:"10分钟负载" \
GPRINT:value2:LAST:%13.2lf \
GPRINT:value2:AVERAGE:%13.2lf \
GPRINT:value2:MAX:%13.2lf \
GPRINT:value2:MIN:%13.2lf \
COMMENT:"\\n" \
LINE2:value3#000fff:"15分钟负载" \
GPRINT:value3:LAST:%13.2lf \
GPRINT:value3:AVERAGE:%13.2lf \
GPRINT:value3:MAX:%13.2lf \
GPRINT:value3:MIN:%13.2lf \
COMMENT:"\\n" \
COMMENT:"最后更新时间 \:$(date '+%Y-%m-%d %H\:%M')\\n" \
COMMENT:"\\n" \
COMMENT:"\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t嘉值云计算"  \
"""
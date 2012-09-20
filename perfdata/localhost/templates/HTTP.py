#coding:utf-8
#!/usr/bin/python


# _HOST_ in 4 hours
hours4="""
--font-render-mode normal \
--graph-render-mode normal \
--slope-mode \
-n DEFAULT:9:'/home/max/.fonts/MSYH.TTF' \
-t "HTTP响应时间   4小时之前的数据" \
-v "响应时间" \
-w 650 -h 120 \
--start  now-4h \
-x MINUTE:5:HOUR:1:HOUR:1:0:'%H:%M' \
DEF:value1={{ rrd_file }}:1:AVERAGE \
COMMENT:"\\n" \
COMMENT:"\\t\\t\\t当前值\\t\\t\\t平均值\\t\\t最大值\\t\\t最小值\\n" \
COMMENT:"\\n" \
AREA:value1#00ff00:"HTTP响应时间" \
GPRINT:value1:LAST:%13.2lf%s \
GPRINT:value1:AVERAGE:%13.2lf%s \
GPRINT:value1:MAX:%13.2lf%s \
GPRINT:value1:MIN:%13.2lf%s \
COMMENT:"\\n" \
COMMENT:"m\: 毫秒 / u\:微秒\\n" \
COMMENT:"最后更新时间 \:$(date '+%Y-%m-%d %H\:%M')\\n" \
COMMENT:"\\n" \
COMMENT:"\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t嘉值云计算" \
"""


# _HOST_ in 25 hours
hours25="""
--font-render-mode normal \
--graph-render-mode normal \
--slope-mode \
-n DEFAULT:9:'/home/max/.fonts/MSYH.TTF' \
-t "HTTP响应时间   25小时之前的数据" \
-v "响应时间" \
-w 650 -h 120 \
--start  now-25h \
-x MINUTE:15:HOUR:1:HOUR:1:0:'%H' \
DEF:value1={{ rrd_file }}:1:AVERAGE \
COMMENT:"\\n" \
COMMENT:"\\t\\t\\t当前值\\t\\t\\t平均值\\t\\t最大值\\t\\t最小值\\n" \
COMMENT:"\\n" \
AREA:value1#00ff00:"HTTP响应时间" \
GPRINT:value1:LAST:%13.2lf%s \
GPRINT:value1:AVERAGE:%13.2lf%s \
GPRINT:value1:MAX:%13.2lf%s \
GPRINT:value1:MIN:%13.2lf%s \
COMMENT:"\\n" \
COMMENT:"m\: 毫秒 / u\:微秒\\n" \
COMMENT:"最后更新时间 \:$(date '+%Y-%m-%d %H\:%M')\\n" \
COMMENT:"\\n" \
COMMENT:"\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t嘉值云计算" \
"""


# _HOST_ in 1 week
week1="""
--font-render-mode normal \
--graph-render-mode normal \
--slope-mode \
-n DEFAULT:9:'/home/max/.fonts/MSYH.TTF' \
-t "HTTP响应时间   1星期之前的数据" \
-v "响应时间" \
-w 650 -h 120 \
--start  now-1week \
-x HOUR:2:HOUR:24:HOUR:24:0:'%A' \
DEF:value1={{ rrd_file }}:1:AVERAGE \
COMMENT:"\\n" \
COMMENT:"\\t\\t\\t当前值\\t\\t\\t平均值\\t\\t最大值\\t\\t最小值\\n" \
COMMENT:"\\n" \
AREA:value1#00ff00:"HTTP响应时间" \
GPRINT:value1:LAST:%13.2lf%s \
GPRINT:value1:AVERAGE:%13.2lf%s \
GPRINT:value1:MAX:%13.2lf%s \
GPRINT:value1:MIN:%13.2lf%s \
COMMENT:"\\n" \
COMMENT:"m\: 毫秒 / u\:微秒\\n" \
COMMENT:"最后更新时间 \:$(date '+%Y-%m-%d %H\:%M')\\n" \
COMMENT:"\\n" \
COMMENT:"\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t嘉值云计算" \
"""


# _HOST_ in 1 month
month1="""
--font-render-mode normal \
--graph-render-mode normal \
--slope-mode \
-n DEFAULT:9:'/home/max/.fonts/MSYH.TTF' \
-t "HTTP响应时间   1个月之前的数据" \
-v "响应时间" \
-w 650 -h 120 \
--start  now-1month \
-x HOUR:6:HOUR:24:HOUR:24:0:'%d' \
DEF:value1={{ rrd_file }}:1:AVERAGE \
COMMENT:"\\n" \
COMMENT:"\\t\\t\\t当前值\\t\\t\\t平均值\\t\\t最大值\\t\\t最小值\\n" \
COMMENT:"\\n" \
AREA:value1#00ff00:"HTTP响应时间" \
GPRINT:value1:LAST:%13.2lf%s \
GPRINT:value1:AVERAGE:%13.2lf%s \
GPRINT:value1:MAX:%13.2lf%s \
GPRINT:value1:MIN:%13.2lf%s \
COMMENT:"\\n" \
COMMENT:"m\: 毫秒 / u\:微秒\\n" \
COMMENT:"最后更新时间 \:$(date '+%Y-%m-%d %H\:%M')\\n" \
COMMENT:"\\n" \
COMMENT:"\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t嘉值云计算" \
"""


# _HOST_ in 1 year
year1="""
--font-render-mode normal \
--graph-render-mode normal \
--slope-mode \
-n DEFAULT:9:'/home/max/.fonts/MSYH.TTF' \
-t "HTTP响应时间   1年之前的数据" \
-v "响应时间" \
-w 650 -h 120 \
--start  now-1year \
-x MONTH:1:MONTH:1:MONTH:1:0:'%B' \
DEF:value1={{ rrd_file }}:1:AVERAGE \
COMMENT:"\\n" \
COMMENT:"\\t\\t\\t当前值\\t\\t\\t平均值\\t\\t最大值\\t\\t最小值\\n" \
COMMENT:"\\n" \
AREA:value1#00ff00:"HTTP响应时间" \
GPRINT:value1:LAST:%13.2lf%s \
GPRINT:value1:AVERAGE:%13.2lf%s \
GPRINT:value1:MAX:%13.2lf%s \
GPRINT:value1:MIN:%13.2lf%s \
COMMENT:"\\n" \
COMMENT:"m\: 毫秒 / u\:微秒\\n" \
COMMENT:"最后更新时间 \:$(date '+%Y-%m-%d %H\:%M')\\n" \
COMMENT:"\\n" \
COMMENT:"\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t嘉值云计算" \
"""



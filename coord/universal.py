# -*- coding: UTF-8 -*-

from math import *

# http://www.geomidpoint.com/destination/calculation.html
# https://www.movable-type.co.uk/scripts/latlong-vincenty.html


# 投影坐标（可能为高斯-吕克投影）转化为WGS-84坐标
def gauss2wgs(x, y):
    # Given the distance s in meters,
    # the semi-major axis 'a' in meters,
    # the semi-minor axis 'b' in meters
    # and the polar flattening 'flat'.
    s = sqrt(x * x + y * y)
    a = 6378137.0  # 赤道半径Re
    b = 6356752.314245  # 极半径Rp
    flat = a / (a - b)  # 298.257223563;

    lat1 = 31.235517  # 上海市原点坐标
    lon1 = 121.467149
    # Convert the starting point latitude 'lat1' (in the range -90 to 90) to radians.
    lat1 = lat1 * pi/180.0
    # Convert the starting point longitude 'lon1' (in the range -180 to 180) to radians.
    lon1 = lon1 * pi/180.0
    # Convert the bearing 'brg' (in the range 0 to 360) to radians.
    # brg = asin(x/s)-pi/4;
    # brg = brg * pi/180;

    # sb=sin(brg);
    # cb=cos(brg);
    # 对初始航向角做了近似，近似为原点到目标点的航向角
    sb=x/s
    cb=y/s
    f = 1.0/flat
    tu1=(1.0-f)*tan(lat1)
    cu1=1.0/sqrt((1.0+tu1*tu1))
    su1=tu1*cu1
    s2=atan2(tu1, cb)
    sa = cu1*sb
    csa=1.0-sa*sa
    us=csa*(a*a - b*b)/(b*b)
    A=1.0+us/16384.0*(4096.0+us*(-768.0+us*(320.0-175.0*us)))
    B = us/1024.0*(256.0+us*(-128.0+us*(74.0-47.0*us)))
    s1=s/(b*A)
    s1p = 2.0*pi

    cs1m = cos(2.0 * s2 + s1)
    ss1 = sin(s1)
    cs1 = cos(s1)
    while abs(s1-s1p) > 1e-12:
        cs1m=cos(2.0*s2+s1)
        ss1=sin(s1)
        cs1=cos(s1)
        ds1=B*ss1*(cs1m+B/4.0*(cs1*(-1.0+2.0*cs1m*cs1m)- B/6.0*cs1m*(-3.0+4.0*ss1*ss1)*(-3.0+4.0*cs1m*cs1m)))
        s1p=s1
        s1=s/(b*A)+ds1

    t=su1*ss1-cu1*cs1*cb
    lat2=atan2(su1*cs1+cu1*ss1*cb, (1.0-f)*sqrt(sa*sa + t*t))
    l2=atan2(ss1*sb, cu1*cs1-su1*ss1*cb)
    c=f/16.0*csa*(4.0+f*(4.0-3.0*csa))
    l=l2-(1.0-c)*f*sa* (s1+c*ss1*(cs1m+c*cs1*(-1.0+2.0*cs1m*cs1m)))
    # d=atan2(sa, -t)
    # finalBrg=d+2.0*pi
    # backBrg=d+pi
    lon2 = lon1+l

    lat2 = lat2 * 180.0/pi -0.0001
    lon2 = lon2 * 180.0/pi -0.00001
    # finalBrg = finalBrg * 180.0/pi
    # backBrg = backBrg * 180.0/pi

    return lat2, lon2
    
    
# 经纬度转Web墨卡托
def ll2mc(lat, lng):
    x = lng *20037508.3427892/180
    y = log(tan((90+lat)*pi/360))/(pi/180)
    y = y *20037508.3427892/180

    return x, y


# Web墨卡托转经纬度
def mc2ll(x, y):
    lng = x/20037508.3427892*180
    lat = y/20037508.3427892*180
    lat = 180/pi*(2*atan(exp(lat*pi/180))-pi/2)
    
    return lat, lng
    


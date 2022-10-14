
area = [0,0 , 500,500]
x1,y1,x2,y2 = 15,15, 50, 50

xc,yc = x1 + x2 // 2, y1 + y2 //2


if xc in range(area[0], area[2]) and yc in range(area[1], area[3]):
    print('inside')
else:
    print('nope')

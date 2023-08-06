ery('select * from fb')
    c = csv.writer(open('dbdump01.csv', 'w'))
    for x in result:
        c.writerow(x)

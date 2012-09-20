
Groups = (
    ('100','Admin'),
    ('90','Operator'),
    ('80','Normal')
)

G = lambda key: [int(i[0]) for i in Groups if i[1] == str(key)][0]

#Json= JavaScript Object Notation
#Es un lenjuage intermediario para comunicar apis entre si, asi como el fornt end y el backend

#concepto importante Clave-Valor/ por cada clave hay una valor asociado <Calve : Valor>  <Nombre:Fabi,x,y>
# cada {Claves:valores} nosostros conetenmos un Objeto POO
#Json y mini base de datos
Json_ejemplo=[#lista de Json
    {#Json individual
        'nombre':'Chris',
        'Apellido':'Ronaldo',
        'Edad': 36,
        'Equipos':['Sport Club',
                'Manchester united',
                'Real madrid',
                'Juventus'] #array de valores (lista)
    },#ojo a la coma heeeeee
    
    {#Json individual
        'nombre':'Leo',
        'Apellido':'Messi',
        'Edad': 36,
        'Equipos':['Sport Club',
                'Manchester united',
                'Real madrid',
                'Juventus'] #array de valores (lista)
    },
    {#Json individual
        'nombre':'Fabi',
        'Apellido':'Messi',
        'Edad': 36,
        'Equipos':['Sport Club',
                'Manchester united',
                'Real madrid',
                'Juventus']
    }
]

dicd=Json_ejemplo[0]
for x in dicd:
    if x =='Equipos':
        print(dicd[x])
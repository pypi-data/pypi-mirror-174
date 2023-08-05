
# Aún este modulo de Len'py esta un poco vacio, tengo pensado agregar más cosas que solo estás que ves aqui.

import platform

windows = False
mac = False
linux = False

if platform.system() == "Windows":
	
	windows = True

elif platform.mac_ver()[0]:
	
	mac = True

elif platform.system() == "Linux":
	
	linux = True
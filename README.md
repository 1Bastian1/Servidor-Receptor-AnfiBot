OBS
---
Se puede rescartar el video y el csv desde el servidor, se pueden ingresar datos al csv, pero NO PUDE TERMINAR EL ELIMINAR EL ULTIMO REGISTRO DEL CSV LOCAL QUE EN EL EL CSV DEL SERVIDOR SERIA UNO QUE NO NECESARIAMENTE DEBE ESTAR AL FINAL.

                                                       
BOT ANALISIS FSICO

 FUNCIONAMIENTO
 --------------
 Cumple la funcion de capturar la materialidad de los productos desmenusando cada parte del mismo.
 Una vez obtenido todos los datos del producto y cada una de sus parte, toda la informacion es almacenada
 en un Dataframe el cual sera almacenado en un CSV. Para que, finalmente se convertido en una hoja de 
 calculo de forma rapida y sencilla

 TECNICO
 --------
 Se crea un cuestionario con ciertos input que se van pidiendo para generar un CSV con toda la informacion.
 A medida que se avanza por las vestanas se rellenan ciertos arreglos con la informacion que le corrsponde a cada uno.
 Luego cada arreglo es juntado en uno solo para formar un dataframe y transformarlo en un CSV.
 Algunas ventanas hacen uso de la camara en el puerto 2 para la web cam, las cuales se van liberando a medida que
 se va moviendo de una ventana a otra

 OBS
 -------
 Cada arreglo es vaciado cuando se abra una ventan. Dependiendo de que ventana se abra es el arreglo que vaciara.
 Esto con el objetivo de poder llevar un mejor control de la informaci'on cuando hay muchos productos con muchas partes.
 Por otro lado la camara el usada en distintas partes de codigo por lo que es necesario liberarla a medida que cambio
 de ventana.

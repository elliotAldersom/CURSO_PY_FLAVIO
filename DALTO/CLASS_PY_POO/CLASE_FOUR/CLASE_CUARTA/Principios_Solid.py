""" 
Principio Solid:
- Primero hay que saber identificar algo:
¿Nuestro programa o proyecto es un software que se va a 
seguir manteniendo, o solo es algo por relajo y sencillo?

- Si queremos que dude debemos de buscar hacer un buen software,
podemos hacer crecer el code y sea más económico.
Además debemos de aplicar un montón de principios, para que cumplan
con las coss necesarios que debe de cumplir:

Debe Cumplir:
1) Mantenibilidad: El software debe ser fácil de mantener y modificar
en el tiempo, esto significa que el code debe de estar bien organizado,
debe de tener una estructura clara y seguir buenas prácticas, si corregimos 
una parte del software, debe de ser fácil y sin afectar a otras partes del code.

2) Reusabilidad: Es decir, poder reusar código, el software debe de estar diseñado
de tal forma que todos los componentes sean reutilisables, como los módulos, clases,
funciones, métodos, todos deben de ser independientes y ser capaces de ser usados
en otros proyectos sin necesidad de agregar cosas nuevas.

3) Legibilidad: Es decir, el code debe de ser fácil y claro de entender para 
cualquier desarrollador que quiera leerlo, podemos usar nombre de variables que 
tengan un significado o sea que sean intuitivos, comentar cuanto sea necesario,
seguir convenciones de estilo y estructurar todo correctamente.

4) Extensibilidd: Es decir, el software debe de permitir la capacidad de 
extenderse sin necesidad de afectar su funcionamiento, es decir, sin afectar
al código que ya existe.


- Principios SOLID:
1) SRP (Principio de Responsabilidad Única) / (Single Responsability Principie)

2) OCP (Principio de Abierto/ Cerrado) / 

3) LSP (Principio de Sustitución del Liskov):

4) ISP (Principio de Segregación de Interfaz):

5) DIP (Principio de Inversión de Dependencias):

AHORA VAMOS A EXPLICARLOS...
"""

#  SRP (Principio de Responsabilidad Única) /  (Single Responsability Principie)
""" 
- Este principio establece algo muy básico:
" Una Clase tiene que tener una y solo una razón para cambiar."

    - Esto signfica que cada clase tiene que tener una única responsabilidad o tarea,
    miremos a las clases como personas que cada una tiene su tarea, si alguien hace marketing
    que haga solo eso, si uno programa que solo haga eso, lo mismo es con las clases, cada uno
    en su única responsabilidad, y si nos damos cuenta que esa clase debe de hacer más cosas, 
    separamos esa clase según las tareas que deben de hacerse y cada una cumple una funcionalidad
    diferente, porque ayuda a evitar sobrecarga, es mejor mantenible y legible, algo importante,
    esa clase o cada clase, puede hacer su tarea sin depender de otras clases.

"""
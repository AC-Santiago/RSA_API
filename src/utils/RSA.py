import secrets
import numpy as np

from manage_json import ManageJson


class RSA:
    def __init__(self):
        """
        Inicializa la clase CifradoDecifrado.

        Parámetros:
        - p (int): Número primo.
        - q (int): Número primo.
        - n (int): n = p*q.
        - phi (int): phi = (p-1)*(q-1).
        - e (int): Clave pública.
        - d (int): Clave privada.
        - longitud_mensaje (int): Longitud del mensaje.
        - mensaje_cifrado (str): Mensaje cifrado.
        - resultado_cifrado (list): Lista de resultados intermedios de cifrado.
        - resultado_cifrado_final (str): Resultado final cifrado.
        - resultado_descifrado (list): Lista de resultados intermedios de descifrado.
        - rules (np.array): Array de reglas.
        """
        self.p = int()
        self.q = int()
        self.n = int()
        self.phi = int()
        self.e = int()
        self.d = int()

        self.longitud_mensaje = int()
        self.mensaje_cifrado = str()

        self.resultado_cifrado = list()
        self.resultado_cifrado_final = str()
        self.resultado_descifrado = list()

        self.rules = np.array([], dtype=int)
        self.rules_Final = list()

    def generar_bases(self) -> tuple:
        """
        Genera los valores de las bases necesarios para el cifrado y descifrado.

        Returns:
            tuple: Una tupla que contiene los valores de p, q, n y phi.
        """
        path = r"src\json\Numeros_primos.json"
        numeros_primos_dict = ManageJson(path).read_json()
        numeros_primos_list = list(numeros_primos_dict["Numeros_primos"])
        while self.q == self.p:
            self.p = secrets.choice(numeros_primos_list)
            self.q = secrets.choice(numeros_primos_list)
        else:
            self.n = self.p * self.q
            self.phi = (self.p - 1) * (self.q - 1)
        return self.p, self.q, self.n, self.phi

    def _lista_maximo_comun_divisor(self, phi: int) -> list:
        """
        Genera una lista de los números menores que phi que son coprimos con phi.

        Args:
            phi (int): El número phi.

        Returns:
            list: Una lista de números coprimos con phi.

        Examples:
            >>> _lista_maximo_comun_divisor(5)
            [4, 3, 2]
            >>> _lista_maximo_comun_divisor(10)
            [9, 8, 7, 6, 4, 3, 2]
            >>> _lista_maximo_comun_divisor(15)
            [14, 13, 11, 7, 6, 4, 3, 2]
        """
        lista = list()
        for i in range(phi, 2, -1):
            if self._mcd(phi, i) == 1:
                lista.append(i)
                if len(lista) == 100:
                    break
        return lista

    def _mcd(self, a: int, b: int) -> int:
        """
        Calcula el máximo común divisor (MCD) de dos números enteros utilizando el algoritmo de Euclides.

        Args:
            a (int): El primer número entero.
            b (int): El segundo número entero.

        Returns:
            int: El máximo común divisor de los dos números enteros.
        """
        if b == 0:
            return a
        else:
            return self._mcd(b, a % b)

    def generar_claves(self) -> tuple:
        """
        Genera una clave pública y una clave privada para el cifrado y descifrado de datos.

        Returns:
            tuple: Una tupla que contiene la clave pública y la clave privada.

        Examples: El retorno del ejemplo solo es para mostrar el formato de la tupla.
            >>> generar_clave()
            ([n, e], [n, d])
        """
        self.e = int(secrets.choice(self._lista_maximo_comun_divisor(self.phi)))
        for i in range(1, self.phi):
            operacion_d1 = 1 + (i * self.phi)
            operacion_d2 = operacion_d1 / self.e
            if operacion_d2.is_integer():
                self.d = int(operacion_d2)
                if self.d != self.e:
                    break
        return [self.n, self.e], [self.n, self.d]

    def _create_rule(self) -> str:
        """
        Crea una regla de cifrado basada en las reglas existentes y el resultado cifrado actual. Usado para el cifrado RSA.

        Returns:
            str: El resultado cifrado final.
        """
        contador = 1
        for i in range(len(self.rules) - 1):
            if self.rules[i] == self.rules[i + 1]:
                contador += 1
            else:
                self.rules_Final.append(
                    int(
                        str(len(str(contador)))
                        + str(contador)
                        + str(len(str(self.rules[i])))
                        + str(self.rules[i])
                    )
                )
                contador = 1
        self.rules_Final.append(
            int(
                str(len(str(contador)))
                + str(contador)
                + str(len(str(self.rules[-1])))
                + str(self.rules[-1])
            )
        )
        element = str(self.rules_Final[0]) + str(self.resultado_cifrado[0])
        self.resultado_cifrado[0] = int(element)

        component_A = int(0)
        component_B = int(0)
        if len(self.rules_Final) == 1:
            component_A = int(str(self.rules_Final[0])[0:1])
            component_B += int(str(self.rules_Final[0])[1 : component_A + 1])
            self.resultado_cifrado_final = "".join(
                str(e) for e in self.resultado_cifrado
            )
            return self.resultado_cifrado_final
        else:
            for i in range(1, len(self.rules_Final)):
                component_A = int(str(self.rules_Final[i - 1])[0:1])
                component_B += int(str(self.rules_Final[i - 1])[1 : component_A + 1])
                element = str(self.rules_Final[i]) + str(
                    self.resultado_cifrado[component_B]
                )
                self.resultado_cifrado[component_B] = int(element)
                self.resultado_cifrado_final = "".join(
                    str(e) for e in self.resultado_cifrado
                )

            return self.resultado_cifrado_final

    def cifrar(self, mensaje: str, Llave_publica: list) -> str:
        """
        Cifra un mensaje utilizando una llave pública (generada con la misama clase).

        Args:
            mensaje (str): El mensaje a cifrar.
            Llave_publica (list): La llave pública utilizada para el cifrado.

        Returns:
            str: El mensaje cifrado.

        Example:
            >>> cifrar("Hola", [10778707, 10771595])
            '111810021898121777995727891755111810706556'
        """
        self.longitud_mensaje = len(mensaje)
        self.mensaje_cifrado = str(mensaje)
        self.n = Llave_publica[0]
        self.e = Llave_publica[1]

        operacion = int()
        rule = int()
        for letra in self.mensaje_cifrado:
            dato = int(ord(letra))
            operacion = self._exponenciacion_rapida(dato, self.e, self.n)
            self.resultado_cifrado.append(operacion)
            rule = len(str(operacion))
            self.rules = np.append(self.rules, rule)
        return self._create_rule()

    def _create_rule(self) -> str:
        """
        Crea una regla de cifrado basada en las reglas existentes y el resultado cifrado actual. Usado para el cifrado RSA.

        Returns:
            str: El resultado cifrado final.
        """
        contador = 1
        for i in range(len(self.rules) - 1):
            if self.rules[i] == self.rules[i + 1]:
                contador += 1
            else:
                self.rules_Final.append(
                    int(
                        str(len(str(contador)))
                        + str(contador)
                        + str(len(str(self.rules[i])))
                        + str(self.rules[i])
                    )
                )
                contador = 1
        self.rules_Final.append(
            int(
                str(len(str(contador)))
                + str(contador)
                + str(len(str(self.rules[-1])))
                + str(self.rules[-1])
            )
        )
        element = str(self.rules_Final[0]) + str(self.resultado_cifrado[0])
        self.resultado_cifrado[0] = int(element)

        component_A = int(0)
        component_B = int(0)
        if len(self.rules_Final) == 1:
            component_A = int(str(self.rules_Final[0])[0:1])
            component_B += int(str(self.rules_Final[0])[1 : component_A + 1])
            self.resultado_cifrado_final = "".join(
                str(e) for e in self.resultado_cifrado
            )
            return self.resultado_cifrado_final
        else:
            for i in range(1, len(self.rules_Final)):
                component_A = int(str(self.rules_Final[i - 1])[0:1])
                component_B += int(str(self.rules_Final[i - 1])[1 : component_A + 1])
                element = str(self.rules_Final[i]) + str(
                    self.resultado_cifrado[component_B]
                )
                self.resultado_cifrado[component_B] = int(element)
                self.resultado_cifrado_final = "".join(
                    str(e) for e in self.resultado_cifrado
                )

            return self.resultado_cifrado_final

    def descifrar(self, mensaje_cifrado: str, Llave_privada: list) -> str:
        """
        Descifra un mensaje cifrado utilizando una llave privada (generada por la misma clase).

        Args:
            mensaje_cifrado (str): El mensaje cifrado a descifrar.
            Llave_privada (list): La llave privada utilizada para descifrar el mensaje.

        Returns:
            str: El mensaje descifrado.

        Examples:
            >>> descifrar('111714252071116619134111723048281116989148', [3357967, 356143])
            'Hola'
        """
        self.lista_cifrado = self._organizar_mensajeC(mensaje_cifrado)
        rango = len(self.lista_cifrado)
        self.n = Llave_privada[0]
        self.d = Llave_privada[1]
        for i in range(rango):
            letra_cifrado = int(self.lista_cifrado[i])
            operacion = self._exponenciacion_rapida(letra_cifrado, self.d, self.n)
            self.resultado_descifrado.append(chr(operacion))
        mesanje_descifrado = "".join(self.resultado_descifrado)
        return mesanje_descifrado

    def _organizar_mensajeC(self, mensaje_cifrado: str) -> list:
        """
        Esta función recibe un mensaje cifrado (cifrado por la funcion cifrar) y lo organiza en una lista siguiendo las instrucciones dadas por los componentes A, B, C y D.

        Componentes:
            A: Cantidad de digitos que tiene el componente B.
            B: Cantidad de veces que se repite el componente C.
            C: Cantidad de digitos que tiene el componente D.
            D: Cantidad de digitos que tiene el elemento referido a la lista.

        Args:
            mensaje_cifrado (str): El mensaje cifrado a organizar.

        Returns:
            list: La lista organizada del mensaje cifrado.

        Examples:
            >>> _organizar_mensajeC('14174985296336765013929454340577')
            [4985296, 3367650, 1392945, 4340577]
        """
        cifrado = []

        component_A = int(mensaje_cifrado[0])
        component_B = int(mensaje_cifrado[1 : 1 + component_A])
        component_C = int(mensaje_cifrado[1 + component_A])
        component_D = int(
            mensaje_cifrado[2 + component_A : 2 + component_A + component_C]
        )

        indice = 2 + component_A + component_C
        cifrado.append(int(mensaje_cifrado[indice : indice + component_D]))
        indice += component_D

        repeat = 1
        while indice < len(mensaje_cifrado):
            if repeat == component_B:
                component_A = int(mensaje_cifrado[indice])
                component_B = int(
                    mensaje_cifrado[indice + 1 : indice + 1 + component_A]
                )
                component_C = int(mensaje_cifrado[indice + 1 + component_A])
                component_D = int(
                    mensaje_cifrado[
                        indice
                        + 2
                        + component_A : indice
                        + 2
                        + component_A
                        + component_C
                    ]
                )
                indice += 2 + component_A + component_C
                repeat = 0
            cifrado.append(int(mensaje_cifrado[indice : indice + component_D]))
            indice += component_D
            repeat += 1

        return cifrado

    def _exponenciacion_rapida(self, base: int, exponente: int, modulo: int) -> int:
        """
        Realiza la exponenciación rápida de un número dado aplicandole el modulo especificado.

        Args:
            base (int): El número base.
            exponente (int): El exponente al que se desea elevar la base.
            modulo (int): El módulo utilizado para calcular el resultado.

        Returns:
            int: El resultado de la exponenciación rápida.

        Examples:
            >>> _exponenciacion_rapida(2, 3, 5)
            3
            >>> _exponenciacion_rapida(2, 3, 7)
            1
            >>> _exponenciacion_rapida(2, 3, 9)
            8
        """
        resultado = 1
        while exponente > 0:
            if exponente % 2 == 1:
                resultado = (resultado * base) % modulo
            exponente = exponente // 2
            base = (base * base) % modulo
        return resultado

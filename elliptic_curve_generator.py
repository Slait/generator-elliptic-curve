import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

def mod_inverse(a, m):
    """Вычисляет модульное обратное число: a^(-1) mod m"""
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

class EllipticCurve:
    """
    Класс для работы с эллиптической кривой вида y^2 = x^3 + ax + b mod p
    """
    def __init__(self, a, b, p, g):
        self.a = a
        self.b = b
        self.p = p  # модуль для публичных ключей
        self.g = g  # генераторная точка G(x,y)
        
        # Проверка, что точка G лежит на кривой
        x, y = g
        if (y**2 % p) != ((x**3 + a*x + b) % p):
            raise ValueError("Точка G не лежит на эллиптической кривой")
    
    def add_points(self, P, Q):
        """Сложение двух точек на эллиптической кривой"""
        if P is None:
            return Q
        if Q is None:
            return P
        
        x1, y1 = P
        x2, y2 = Q
        
        # Если P = Q, используем формулу для удвоения точки
        if x1 == x2 and y1 == y2:
            # Формула для тангенса в точке P
            numerator = (3 * x1**2 + self.a) % self.p
            denominator = (2 * y1) % self.p
            m = (numerator * mod_inverse(denominator, self.p)) % self.p
        # Если P ≠ Q, используем формулу для сложения разных точек
        elif x1 != x2:
            numerator = (y2 - y1) % self.p
            denominator = (x2 - x1) % self.p
            m = (numerator * mod_inverse(denominator, self.p)) % self.p
        # Если P + Q = O (бесконечно удаленная точка)
        else:
            return None
        
        # Вычисление координат результирующей точки
        x3 = (m**2 - x1 - x2) % self.p
        y3 = (m * (x1 - x3) - y1) % self.p
        
        return (x3, y3)
    
    def scalar_multiply(self, k, P):
        """Умножение точки P на скаляр k"""
        result = None
        addend = P
        
        while k:
            if k & 1:
                result = self.add_points(result, addend)
            addend = self.add_points(addend, addend)
            k >>= 1
            
        return result
    
    def generate_all_points(self, private_key_modulus):
        """
        Генерирует все точки для приватных ключей от 1 до private_key_modulus
        и записывает их в файл
        """
        points = []
        with open("point.txt", "w") as f:
            for private_key in tqdm(range(1, private_key_modulus + 1), desc="Генерация точек"):
                point = self.scalar_multiply(private_key, self.g)
                if point:
                    points.append(point)
                    f.write(f"{private_key}, {point[0]}, {point[1]}\n")
        
        return points
    
    def plot_points(self, points):
        """Построение графика точек эллиптической кривой"""
        plt.figure(figsize=(20, 20), dpi=100)
        
        x_values = [p[0] for p in points]
        y_values = [p[1] for p in points]
        
        plt.scatter(x_values, y_values, s=5, alpha=0.8)
        plt.title("Точки эллиптической кривой")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.xlim(0, self.p)
        plt.ylim(0, self.p)
        plt.grid(True)
        plt.savefig("elliptic_curve_points.png", dpi=100)
        plt.close()

def main():
    # Параметры для демонстрации (можно изменить)
    a = int(input("Введите параметр a кривой y^2 = x^3 + ax + b. Пример 0: "))
    b = int(input("Введите параметр b кривой y^2 = x^3 + ax + b. Пример 7: "))
    p = int(input("Введите модуль для публичных ключей (p). Пример 67: "))
    
    gx = int(input("Введите x-координату точки G. Пример 2: "))
    gy = int(input("Введите y-координату точки G. Пример 22: "))
    g = (gx, gy)
    
    private_key_modulus = int(input("Введите модуль для приватных ключей. Пример 79: "))
    
    try:
        curve = EllipticCurve(a, b, p, g)
        print(f"Параметры эллиптической кривой: y^2 = x^3 + {a}x + {b} mod {p}")
        print(f"Генераторная точка G: ({g[0]}, {g[1]})")
        print(f"Модуль для приватных ключей: {private_key_modulus}")
        
        print("Генерация точек и запись в файл point.txt...")
        points = curve.generate_all_points(private_key_modulus)
        
        print(f"Сгенерировано {len(points)} точек")
        print("Построение графика точек...")
        curve.plot_points(points)
        print("График сохранен в файл elliptic_curve_points.png")
        
    except ValueError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main() 
def main():
    jar = Jar(20)
    print(f"Jar capacity: {jar.capacity}")
    print(f"Current cookies in jar: {jar.size}")
    print(f"Cookies: {str(jar)}")

    jar.deposit(5)
    print(f"Current cookies in jar: {jar.size}")
    print(f"Cookies: {str(jar)}")

    jar.withdraw(2)
    print(f"Current cookies in jar: {jar.size}")
    print(f"Cookies: {str(jar)}")


class Jar:
    def __init__(self, capacity=12):
        if capacity < 1:
            raise ValueError("Capacity must be greater then 0.")

        self._capacity = capacity
        self._size = 0

    def __str__(self):
        return "🍪" * self._size

    def deposit(self, n):
        if self._size + n > self.capacity:
            raise ValueError("Adding cookies would exceed the jar's capacity.")

        self._size += n

    def withdraw(self, n):
        if n > self._size:
            raise ValueError("Not enough cookies in the jar to withdraw.")

        self._size -= n

    @property
    def capacity(self):
        return self._capacity

    @property
    def size(self):
        return self._size


main()

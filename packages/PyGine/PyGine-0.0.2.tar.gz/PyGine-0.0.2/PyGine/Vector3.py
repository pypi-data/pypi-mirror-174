class Vector3 :
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    def __mul__(self, other):
        return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)
    def __truediv__(self, other):
        return Vector3(self.x / other.x, self.y / other.y, self.z / other.z)
import math
class Vector:
    'Represents a 2D vector.'
    def __init__(self, x = 0, y = 0):
        self.x = float(x)
        self.y = float(y)

    def __eq__(self, v):
        epsilon = 0.005
        return (math.fabs(self.x - v.x) < epsilon and
                math.fabs(self.y - v.y) < epsilon)

    def __add__(self, val):
        return Vector( self[0] + val[0], self[1] + val[1] )
    
    def __sub__(self,val):
        return Vector( self[0] - val[0], self[1] - val[1] )
    
    def __iadd__(self, val):
        self.x = val[0] + self.x
        self.y = val[1] + self.y
        return self
        
    def __isub__(self, val):
        self.x = self.x - val[0]
        self.y = self.y - val[1]
        return self
    
    def __truediv__(self, val):
        return Vector( self[0] / val, self[1] / val )

    def __floordiv__(self, val):
        return Vector( self[0] // val, self[1] // val)
    
    def __mul__(self, val):
        return Vector( self[0] * val, self[1] * val )
    
    def __idiv__(self, val):
        self[0] = self[0] / val
        self[1] = self[1] / val
        return self
        
    def __imul__(self, val):
        self[0] = self[0] * val
        self[1] = self[1] * val
        return self

    def __getitem__(self, key):
        if( key == 0):
            return self.x
        elif( key == 1):
            return self.y
        else:
            raise Exception("Invalid key to Vector")
        
    def __setitem__(self, key, value):
        if( key == 0):
            self.x = value
        elif( key == 1):
            self.y = value
        else:
            raise Exception("Invalid key to Vector")
        
    def __str__(self):
        return "(" + str(round(self.x, 1)) + "," + str(round(self.y, 1)) + ")"
        
    def DistanceSqrd( point1, point2 ):
        'Returns the distance between two points squared. Marginally faster than Distance()'
        return ( (point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)
    def Distance( point1, point2 ):
        'Returns the distance between two points'
        return math.sqrt( Vector.DistanceSqrd(point1,point2) )
    def LengthSqrd( vec ):
        'Returns the length of a vector sqaured. Faster than Length(), but only marginally'
        return vec[0]**2 + vec[1]**2
    def Length( vec ):
        'Returns the length of a vector'
        return math.sqrt( Vector.LengthSqrd(vec) )
    def Normalize( vec ):
        'Returns a new vector that has the same direction as vec, but has a length of one.'
        if( vec[0] == 0. and vec[1] == 0. ):
            return Vector(0.,0.)
        return vec / Vector.Length(vec)
    def Dot( a,b ):
        'Computes the dot product of a and b'
        return a[0]*b[0] + a[1]*b[1]
    def ProjectOnto( w,v ):
        'Projects w onto v.'
        return v * Vector.Dot(w,v) / Vector.LengthSqrd(v)

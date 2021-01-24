from numbers import Number


class Bar:    
    def __init__(self, o: Number, h: Number, l: Number, c: Number):
        #Validation
        if h < l : raise ValueError(f'High price must be greater than low price:\n High:{h} > Low:{l}')
        if (o > h or o < l): raise ValueError(f'Open price must be between High and Low:\n High:{h} => Open:{o} >= Low:{l}')
        if (c > h or c < l): raise ValueError(f'Close price must be between High and Low:\n High:{h} => Close:{c} >= Low:{l}')
            
        self._open = o
        self._high = h
        self._low = l
        self._close = c
    
    #Bar range: High - Low
    @property
    def range(self) -> Number:
        return  self._high - self._low
    
    #Bar mean price
    @property
    def mean(self) -> Number:
        return round((self._high + self._low) / 2, 2)
    
    def __repr__(self):
        return "Bar(o={}, h={}, l={}, c={})".format(self._open, self._high, self._low, self._close)
    
    def __str__(self):
        return "{{Open:{}, High:{}, Low:{}, Close:{}}}".format(self._open, self._high, self._low, self._close)
    
    
    def __add__(self, other : 'Bar') -> 'Bar':
        if not isinstance(other, type(self)):
            raise TypeError(f"Other variable must be type {type(self)}, not {type(other)}")
        
        high = max(self._high, other._high)
        low = min(self._low, other._low)
        
        return type(self)(self._open, high, low, other._close)
 

    def __le__(self, other : 'Bar') -> 'Bar':
        if not isinstance(other, type(self)):
            raise TypeError(f"Other variable must be type {type(self)}, not {type(other)}")
        
        return self.range <= other.range
    
    
    def __lt__(self, other : 'Bar') -> 'Bar':
        if not isinstance(other, type(self)):
            raise TypeError(f"Other variable must be type {type(self)}, not {type(other)}")
        
        return self.range < other.range
    
    
    
    def __ge__(self, other : 'Bar') -> 'Bar':
        if not isinstance(other, type(self)):
            raise TypeError(f"Other variable must be type {type(self)}, not {type(other)}")
        
        return self.range >= other.range
    
    
    def __gt__(self, other : 'Bar') -> 'Bar':
        if not isinstance(other, type(self)):
            raise TypeError(f"Other variable must be type {type(self)}, not {type(other)}")
        
        return self.range > other.range

    
    def __eq__(self, other : 'Bar') -> 'Bar':
        if not isinstance(other, type(self)):
            raise TypeError(f"Other variable must be type {type(self)}, not {type(other)}")
        
        return self.range == other.range
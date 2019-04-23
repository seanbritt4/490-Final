import random

class Tile():
    resources = 999
    def __init__(self):
        self.tile_type = 'tile'
        
    def find_color(self):
#        print self.tile_type
        pass

        
class Ground_Tile(Tile):
    def __init__(self):
        self.tile_type = 'ground'
        self.resources = round(random.uniform(0.0, 0.99))

        
class Occ_Tile(Ground_Tile):
    def __init__(self):
        self.tile_type = 'occupied'
        self.resources = round(random.uniform(0.0, 0.99), 2)
        self.pop = round(random.uniform(0.33, 0.66), 2)
        self.consumption_rate = round(random.uniform(0.25, 0.75), 2)
        self.growth_rate = round(random.uniform(0.25, 0.75), 2)
    
    def print_occ(self):
        print self.tile_type
        print self.resources
        print self.pop
        print self.consumption_rate
        print self.growth_rate
        
# may want to save this for later...       
#class Water_Tile(Tile):
#    def __init__(self):
#        self.tile_type = 'water'
#        self.color = (0,0,225)
#        
        
def main():
    test = Ground_Tile()
    print test.tile_type
    print test.resources
    test.find_color()
    
    test1= Tile()
    print test1.tile_type
    print test1.resources
    test1.find_color()
    
    test2 = Occ_Tile()
    test2.print_occ()
    test2.find_color()
    
#    test3 = Water_Tile()
#    print test3.tile_type
#    print test3.res
#    test3.find_color()
    
    print
    
    
if __name__ == "__main__":
    main()
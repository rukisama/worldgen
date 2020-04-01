import tcod as libtcod
import numpy

max_elevation = 255.0
water_cutoff = int(round(max_elevation * 0.25))
plain_cutoff = int(round(max_elevation * 0.50))
mountain_cutoff = int(round(max_elevation * 0.85))
print("Water cutoff: ", water_cutoff)
print("Plain Cutoff: ", plain_cutoff)
print("Mountain cutoff: ", mountain_cutoff)


class WorldMap:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.elevation_map = None
        self.temperature_map = None
        self.rainfall_map = None
        self.drainage_map = None
        self.fg_color = None
        self.bg_color = None
        self.glyph = None

        self.local_map = LocalMap(self.width, self.height)  # TODO: This is totally a placeholder
        self.local_map.make_local_map('bullshit')
        # super().__init__(w, h)

    def generate_map(self, noise_zoom, noise_octaves):

        elevation = libtcod.heightmap_new(self.width, self.height)
        hm1 = libtcod.heightmap_new(self.width, self.height)
        hm2 = libtcod.heightmap_new(self.width, self.height)

        rainfall = libtcod.heightmap_new(self.width, self.height)

        fg_color = numpy.ndarray((self.width, self.height, 3))
        glyphs = numpy.ndarray((self.width, self.height, 2))
        chance = numpy.random.randint(2, size=(self.width, self.height))

        # Temperature also varies randomly by 0 to -4 degrees, makes the icecap transition look better
        temp_rand_variation = numpy.random.randint(-4, 0, size=(self.width, self.height))

        # Zero out all of the heightmap arrays (need to do this because of a bug with libtcod, should be fixed soon)
        elevation[:] = 0
        hm1[:] = 0
        hm2[:] = 0
        rainfall[:] = 0

        # Temperature and rainfall vary with latitude, from -10C at the poles to 30C at the equator for temp
        temp_variation = numpy.sin(numpy.linspace(0, numpy.pi, num=100)) * 40 - 10
        rainfall_variation = numpy.sin(numpy.linspace(0, numpy.pi, num=100))
        # Broadcast 1D temp_variation to 2D temperature map
        temperature = numpy.ones((100, 100)) * temp_variation
        temperature = temperature.transpose()

        noise = libtcod.noise_new(2)
        libtcod.heightmap_add_fbm(hm1, noise, noise_zoom, noise_zoom, 0.0, 0.0, noise_octaves, 0.0, 1.0)
        libtcod.heightmap_add_fbm(hm2, noise, noise_zoom * 2, noise_zoom * 2, 0.0, 0.0, noise_octaves, 0.0, 1.0)
        libtcod.heightmap_add_fbm(rainfall, noise, noise_zoom * 4, noise_zoom * 4, 0.0, 0.0, noise_octaves, 0.0, 1.0)

        libtcod.heightmap_multiply_hm(hm1, hm2, elevation)

        libtcod.heightmap_normalize(elevation, mi=0.0, ma=max_elevation)
        libtcod.heightmap_normalize(rainfall, mi=0.0, ma=400)

        rainfall_v_2d = numpy.ones((100, 100)) * rainfall_variation
        rainfall_v_2d = rainfall_v_2d.transpose()
        rainfall = rainfall * rainfall_v_2d
        temperature[elevation >= mountain_cutoff] -= 10
        temperature[elevation >= plain_cutoff] -= 5
        temperature = temperature + temp_rand_variation

        fg_color[elevation >= mountain_cutoff], glyphs[elevation >= mountain_cutoff] = (128, 128, 128), (30, 30)
        fg_color[elevation < mountain_cutoff], glyphs[elevation < mountain_cutoff] = (160, 82, 45), (239, 110)
        fg_color[elevation < plain_cutoff], glyphs[elevation < plain_cutoff] = (0, 128, 0), (252, ord('.'))
        fg_color[elevation < water_cutoff], glyphs[elevation < water_cutoff] = (0, 0, 200), (247, 247)

        water = elevation < water_cutoff
        hills = elevation > plain_cutoff
        mountains = elevation > mountain_cutoff

        # Tundra
        tundra_rainfall = rainfall >= 0
        tundra_temp = temperature <= 0
        tundra = tundra_rainfall & tundra_temp & ~water & ~hills & ~mountains
        tundra_hills = tundra_rainfall & tundra_temp & ~water & hills & ~mountains
        fg_color[tundra], glyphs[tundra] = (115, 255, 255), (249, 250)
        fg_color[tundra_hills], glyphs[tundra_hills] = (115, 255, 255), (239, 110)

        # Taiga
        taiga_rainfall = rainfall >= 100
        taiga_temp = temperature >= 0
        taiga = taiga_rainfall & taiga_temp & ~water & ~hills & ~mountains
        taiga_hills = taiga_rainfall & taiga_temp & ~water & hills & ~mountains
        fg_color[taiga], glyphs[taiga] = (0, 128, 0), (23, 24)
        fg_color[taiga_hills], glyphs[taiga_hills] = (0, 128, 0), (239, 24)

        # Shrubland
        shrub_rainfall = rainfall < 100
        shrub_temp = temperature > 0
        shrub = shrub_rainfall & shrub_temp & ~water & ~hills & ~mountains
        shrub_hills = shrub_rainfall & shrub_temp & ~water & hills & ~mountains
        fg_color[shrub], glyphs[shrub] = (191, 255, 0), (231, 34)
        fg_color[shrub_hills], glyphs[shrub_hills] = (191, 255, 0), (239, 34)

        # Temperate Grassland
        grassland_rainfall = rainfall > 100
        grassland_temp = temperature > 10
        grassland = grassland_rainfall & grassland_temp & ~water & ~hills & ~mountains
        grassland_hills = grassland_rainfall & grassland_temp & ~water & hills & ~mountains
        fg_color[grassland], glyphs[grassland] = (127, 255, 0), (252, 34)
        fg_color[grassland_hills], glyphs[grassland_hills] = (127, 255, 0), (239, 34)

        # Temperate Broadleaf Forest
        temp_broad_rainfall = rainfall > 200
        temp_broad_temp = temperature > 10
        temp_broad = temp_broad_rainfall & temp_broad_temp & ~water & ~hills & ~mountains
        temp_broad_hills = temp_broad_rainfall & temp_broad_temp & ~water & hills & ~mountains
        fg_color[temp_broad], glyphs[temp_broad] = (0, 200, 0), (5, 6)
        fg_color[temp_broad_hills], glyphs[temp_broad_hills] = (0, 200, 0), (239, 6)

        # Temperate Rainforest
        temp_rainforest_rainfall = rainfall > 300
        temp_rainforest_temp = temperature > 10
        temp_rainforest = temp_rainforest_rainfall & temp_rainforest_temp & ~water & ~hills & ~mountains
        temp_rainforest_hills = temp_rainforest_rainfall & temp_rainforest_temp & ~water & hills & ~mountains
        fg_color[temp_rainforest], glyphs[temp_rainforest] = (0, 200, 0), (6, 226)
        fg_color[temp_rainforest_hills], glyphs[temp_rainforest_hills] = (0, 200, 0), (239, 226)

        # Desert
        desert_rainfall = rainfall <= 10
        desert_temp = temperature > 20
        desert = desert_rainfall & desert_temp & ~water & ~hills & ~mountains
        desert_hills = desert_rainfall & desert_temp & ~water & hills & ~mountains
        fg_color[desert], glyphs[desert] = (255, 255, 0), (126, 247)
        fg_color[desert_hills], glyphs[desert_hills] = (191, 143, 0), (86, 251)

        # Savanna
        savanna_rainfall = rainfall > 10
        savanna_temp = temperature > 20
        savanna = savanna_rainfall & savanna_temp & ~water & ~hills & ~mountains
        savanna_hills = savanna_rainfall & savanna_temp & ~water & hills & ~mountains
        fg_color[savanna], glyphs[savanna] = (255, 255, 115), (252, 34)
        fg_color[savanna_hills], glyphs[savanna_hills] = (255, 255, 115), (239, 34)

        # Tropical Seasonal Forest
        trop_seasonal_rainfall = rainfall > 200
        trop_seasonal_temp = temperature > 20
        trop_seasonal = trop_seasonal_rainfall & trop_seasonal_temp & ~water & ~hills & ~mountains
        trop_seasonal_hills = trop_seasonal_rainfall & trop_seasonal_temp & ~water & hills & ~mountains
        fg_color[trop_seasonal], glyphs[trop_seasonal] = (0, 100, 0), (5, 6)
        fg_color[trop_seasonal_hills], glyphs[trop_seasonal_hills] = (0, 100, 0), (239, 6)

        # Tropical Rainforest
        rainforest_rainfall = rainfall > 300
        rainforest_temp = temperature > 20
        rainforest = rainforest_rainfall & rainforest_temp & ~water & ~hills & ~mountains
        rainforest_hills = rainforest_rainfall & rainforest_temp & ~water & hills & ~mountains
        fg_color[rainforest], glyphs[rainforest] = (0, 100, 0), (6, 226)
        fg_color[rainforest_hills], glyphs[rainforest_hills] = (0, 100, 0), (239, 226)

        glyphs[temperature <= -8] = (178, 219)
        fg_color[temperature <= -8] = (0, 255, 255)
        fg_color[elevation == 255] = (0, 255, 255)

        glyph_choice = numpy.where(chance, glyphs[..., 1], glyphs[..., 0])

        self.elevation_map = elevation
        self.fg_color = fg_color
        self.glyph = glyph_choice
        self.temperature_map = temperature
        self.rainfall_map = rainfall


class LocalMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.glyph = None
        self.fg_color = None
        self.bg_color = None

    def make_local_map(self, biome):
        # if biome == 'forest' or whatever
        glyph = numpy.ndarray((self.width, self.height), dtype=numpy.intc)
        fg_color = numpy.ndarray((self.width, self.height, 3))
        bg_color = numpy.ndarray((self.width, self.height, 3))
        trees1 = numpy.random.randint(2, size=(self.width, self.height))
        trees2 = numpy.random.randint(2, size=(self.width, self.height))
        trees3 = numpy.random.randint(2, size=(self.width, self.height))
        trees = trees1 & trees2 & trees3

        bg_color[:] = (0, 64, 0)
        fg_color[:] = (0, 128, 0)
        glyph[:] = 34

        glyph[trees == 1] = 79
        fg_color[trees == 1] = (189, 119, 69)

        self.glyph = glyph
        self.fg_color = fg_color
        self.bg_color = bg_color

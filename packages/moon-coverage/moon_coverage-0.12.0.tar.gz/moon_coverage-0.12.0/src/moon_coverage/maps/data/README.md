Background maps
===============

> __Warning__: For ESA/JUICE instruments,
> the longitudes are defined eastward from (0° to 360° to the East).
> This definition is not consistent with the IAU report (2018)
> and the NAIF-SPICE planetographic coordinate system (defined
> westward for prograde bodies).


Ganymede
--------
* __Mean radius__: 2631.2 km

![Kersten et al. 2021 - PSS](Ganymede.jpg)

* __Source__: [Kersten et al. 2021 - PSS / DLR](https://doi.org/10.1016/j.pss.2021.105310)
* __Original image size__: 46,080 × 23,039 pixels
* __Instrument__: Voyager ISS / Galileo SSI
* __Equatorial resolution__: 360 m / pixel


Callisto
--------
* __Mean radius__: 2410.3 km

![USGS/ESA Callisto 1 km mosaic](Callisto.jpg)

* __Source__: [USGS/ESA](https://www.cosmos.esa.int/web/juice/reference-maps-ganymede-europa-callisto-)
* __Original image size__: 15,138 × 7,569 pixels
* __Instrument__: Voyager ISS / Galileo SSI
* __Equatorial resolution__: 1 km / pixel


Europa
------
* __Mean radius__: 1560.8 km

![NASA/JPL/Björn Jónsson 500 m mosaic](Europa.jpg)

* __Source__: [NASA/JPL/Björn Jónsson](https://www.planetary.org/space-images/color-global-map-of-europa)
* __Original image size__: 20,000 × 10,000 pixels
* __Instrument__: Voyager ISS / Galileo SSI
* __Equatorial resolution__: 490 m / pixel

_Note:_ The area without data were masked based on the [previously
published USGS map](https://astrogeology.usgs.gov/search/map/Europa/Voyager-Galileo/Europa_Voyager_GalileoSSI_global_mosaic_500m) for Europa.


Io
--
* __Mean radius__: 1821.5 km

![USGS/ESA 1 km mosaic](Io.jpg)

* __Source__: [USGS](https://astrogeology.usgs.gov/search/map/Io/Voyager-Galileo/Io_GalileoSSI-Voyager_Global_Mosaic_ClrMerge_1km)
* __Original image size__: 11,445 ×  5,723 pixels
* __Instrument__: Voyager ISS / Galileo SSI
* __Equatorial resolution__: 1 km / pixel


Jupiter
-------
* __Mean radius__: 69,911.3 km

![JPL PIA07782 20 km mosaic](Jupiter.jpg)

* __Source__: [JPL PIA07782](https://photojournal.jpl.nasa.gov/tiff/PIA07782.tif)
* __Original image size__: 3,601 ×  1,801 pixels
* __Instrument__: Cassini ISS
* __Equatorial resolution__: 122 km / pixel


Earth
-----
* __Mean radius__: 6371.0 km

![July, Blue Marble Next Generation w/ Topography and Bathymetry](Earth.jpg)

* __Source__: [NASA](https://visibleearth.nasa.gov/images/73751/july-blue-marble-next-generation-w-topography-and-bathymetry)
* __Original image size__: 86,400 ×  43,200 pixels
* __Instrument__: Terra MODIS
* __Equatorial resolution__: 463 m / pixel


Moon
----
* __Mean radius__: 1737.4 km

![USGS 100 m mosaic](Moon.jpg)

* __Source__: [USGS](https://planetarymaps.usgs.gov/mosaic/Lunar_LRO_LROC-WAC_Mosaic_global_100m_June2013.tif)
* __Original image size__: 109,164 ×  54,582 pixels
* __Instrument__: LRO WAC
* __Equatorial resolution__: 100 m / pixel


Venus
-----
* __Mean radius__: 6051.8 km

![USGS 4.6 km mosaic](Venus.jpg)

* __Source__: [USGS](https://planetarymaps.usgs.gov/mosaic/Venus_Magellan_C3-MDIR_Colorized_Global_Mosaic_4641m.tif)
* __Original image size__: 8,192 ×  4,096 pixels
* __Instrument__: C3-MDIR Synthetic Color Mosaic
* __Equatorial resolution__: 4.6 km / pixel


Mercury
-------
* __Mean radius__: 2,439.7 km

![USGS 4.6 km mosaic](Mercury.jpg)

* __Source__: [USGS](https://planetarymaps.usgs.gov/mosaic/Mercury_MESSENGER_MDIS_Basemap_LOI_Mosaic_Global_166m.tif)
* __Original image size__: 92,160 × 46,080 pixels
* __Instrument__: Messenger WAC/NAC at 750 nm
* __Equatorial resolution__: 166 m / pixel


All the maps are center at 180° and the mean radius is calculated
based on `pck00010.tpc` kernel.


How to (re)-generate these maps and the maps assets
---------------------------------------------------
```python
from moon_coverage.maps import Map

m = Map('Ganymede_Voyager_GalileoSSI_global_mosaic_1km.tif', size=(1024, 2048))

# Save resized image
m.img.save('Ganymede.jpg')

# Create documentation thumbnail with map grid
m.map(fout='Ganymede.jpg')
```

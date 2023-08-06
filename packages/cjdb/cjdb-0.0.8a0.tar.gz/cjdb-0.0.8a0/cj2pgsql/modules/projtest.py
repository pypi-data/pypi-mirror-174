from pyproj import CRS, Transformer, datadir
from pyproj.transformer import TransformerGroup

x = [78811.60599536133, 79477.03299731445]
y = [449466.85900830076, 450116.310000885]
z = [-4.353396892547607, 22.3062801361084]

srid_from = 7415
srid_to = 4979
source_proj = CRS.from_epsg(srid_from)
target_proj = CRS.from_epsg(srid_to)

group = TransformerGroup(source_proj, target_proj)

# resp = requests.get("https://cdn.proj.org/nl_nsgi_nlgeo2018.tif", allow_redirects=True)

transformer = Transformer.from_crs(source_proj, target_proj, always_xy=True)

reprojected_xyz = transformer.transform(x, y, z)
print("before: ", [x, y, z])
print("after: ", reprojected_xyz)
print(datadir.get_data_dir())

# transformer_3d = Transformer.from_crs(
#     CRS("EPSG:4326").to_3d(),
#     CRS("EPSG:2056").to_3d(),
#     always_xy=True
#     )
# print(transformer_3d.transform(8.37909, 47.01987, 1000))


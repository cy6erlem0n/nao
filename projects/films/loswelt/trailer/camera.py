import bpy
import math

# Очистка сцены
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Шаг 1: Создание кривой
bpy.ops.curve.primitive_bezier_curve_add()
curve = bpy.context.object
curve.name = "FlightPath"
curve.data.dimensions = '3D'

# Настраиваем точки кривой
splines = curve.data.splines[0]
points = splines.bezier_points

# Добавляем точки кривой
while len(points) < 3:
    splines.bezier_points.add(1)

# Устанавливаем координаты точек кривой
points[0].co = (-10, -10, 10)
points[1].co = (0, 0, 20)
points[2].co = (10, 10, 5)

# Устанавливаем автоматические ручки для плавности кривой
for point in points:
    point.handle_left_type = point.handle_right_type = 'AUTO'

# Шаг 2: Создание пустышки для движения по кривой
bpy.ops.object.empty_add(type='PLAIN_AXES')
empty = bpy.context.object
empty.name = "PathFollower"

# Ограничение на следование пути
path_constraint = empty.constraints.new(type='FOLLOW_PATH')
path_constraint.target = curve
path_constraint.use_curve_follow = True  # Следуем за кривой
path_constraint.use_fixed_location = True

# Шаг 3: Создание камеры и привязка к пустышке
bpy.ops.object.camera_add(location=(0, 0, 0))
camera = bpy.context.object
camera.name = "FlyingCamera"
camera.parent = empty  # Привязываем камеру к пустышке

# Настройка вращения камеры с ограничением
track_to = camera.constraints.new(type='TRACK_TO')
track_to.target = empty  # Камера будет ориентироваться на пустышку
track_to.track_axis = 'TRACK_NEGATIVE_Z'  # Направление вперёд по оси -Z
track_to.up_axis = 'UP_Y'                 # Верх камеры по оси Y

# Настройка анимации
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 250

path_constraint.offset_factor = 0.0  # Начальная позиция
path_constraint.keyframe_insert(data_path="offset_factor", frame=1)

path_constraint.offset_factor = 1.0  # Конечная позиция
path_constraint.keyframe_insert(data_path="offset_factor", frame=250)

# Шаг 4: Добавление тестовой карты
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))
plane = bpy.context.object
plane.name = "Map"

# Обновляем сцену
bpy.context.scene.frame_current = 1
bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

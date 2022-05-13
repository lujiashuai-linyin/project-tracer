import base
from tracer.models import SceneInfo

# scene_id_list = []
# scene_id_query = SceneInfo.objects.values("scene_id.txt").distinct().order_by("scene_id.txt")
#
# print(scene_id_query)
# for item in scene_id_query:
#     scene_id_list.append(item["scene_id.txt"])
# with open("scene_id_list.txt", "a") as f:
#     f.write(str(scene_id_list))


with open("scene_id.txt", "r") as f:
    scene_id_list = list(f.readlines())
# print(scene_id_list)
scene_id = []
for i in scene_id_list:
    b = i.replace("\n","")
    scene_id.append(b)
# print(scene_id)

test_path_list = SceneInfo.objects.filter(scene_id__in=scene_id_list).values_list("test_path","scene_id")
print(test_path_list)

with open("result_list.txt", "a") as fp:
    for i in test_path_list:
        scene_path = i.scene_path
        scene_id = i.scene_id
        fp.write(str(scene_path,))

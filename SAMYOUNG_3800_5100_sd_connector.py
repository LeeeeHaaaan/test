import os

from modules import manager
from modules import interface
from modules.GPS_SAMYOUNG.Navis3800_5100 import SAMYOUNG_Navis3800_5100_coastline_parser as getCoastline
from modules.GPS_SAMYOUNG.Navis3800_5100 import SAMYOUNG_Navis3800_5100_track_parser as getTrack
from modules.GPS_SAMYOUNG.Navis3800_5100 import SAMYOUNG_Navis3800_5100_waypoint_parser as getWaypoint
from modules.GPS_SAMYOUNG.Navis3800_5100 import SAMYOUNG_Navis3800_5100_mark_parser as getMark

class SAMYOUNG_3800_5100_sd_connector(interface.ModuleConnector):
    # NAME 은 python 파일 이름과 동일.
    NAME = "SAMYOUNG_3800_5100_sd_connector"
    DESCRIPTION = "Module for SAMYOUNG_3800_5100_sd_(Coastline, Track, Waypoint, Mark)"

    _plugin_classes = {}

    def __init__(self):
        super(SAMYOUNG_3800_5100_sd_connector, self).__init__()

    def Connect(self, par_id, configuration, source_path_spec, knowledge_base):
        this_file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep + 'schema' + os.sep + "schema_Samyoung" + os.sep

        # yaml 파일 이름
        yaml_list = [
            this_file_path + "lv1_3800_5100_coastline.yaml",
            this_file_path + "lv1_3800_5100_track.yaml",
            this_file_path + "lv1_3800_5100_waypoint.yaml",
            this_file_path + "lv1_3800_5100_mark.yaml"]

        # yaml 파일에서 명시한 Table 이름
        table_list = [
            "lv1_3800_5100_coastline",
            "lv1_3800_5100_track",
            "lv1_3800_5100_waypoint",
            "lv1_3800_5100_mark"]

        if not self.check_table_from_yaml(configuration, yaml_list, table_list):
            return False

        output_path = configuration.root_tmp_path + os.sep + configuration.case_id + os.sep + \
                      configuration.evidence_id + os.sep + par_id

        query = f"SELECT name, parent_path FROM file_info WHERE par_id='{par_id}' and name REGEXP '.[0-9]{{4}}.DAT' and name not REGEXP '-slack';"
        file_path_list = configuration.cursor.execute_query_mul(query)

        for file_path in file_path_list:
            name, path = file_path

            if 'L' == name[0] or 'M' == name[0] or 'T' == name[0] or 'W' == name[0]:
                extract_path = path[path.find('/'):] +'/'+ name
                self.ExtractTargetFileToPath(source_path_spec=source_path_spec,
                                            configuration=configuration,
                                            file_path= extract_path,
                                            output_path=output_path)

        try:
            info = [par_id, configuration.case_id, configuration.evidence_id]
            file_list = os.listdir(output_path)

            for file in file_list:
                file_path = output_path + os.sep + file
                if 'L' == file[0]:
                    getCoastlineData = list()
                    coastlineData = getCoastline.coastline(file_path)
                    for c in coastlineData:
                        getCoastlineData.append((info[0], info[1], info[2], c[0], c[1], c[2], c[3]))
                    query = f"INSERT INTO lv1_3800_5100_coastline values (%s, %s, %s, %s, %s, %s, %s)"
                    configuration.cursor.bulk_execute(query, getCoastlineData)

                elif 'M' == file[0]:
                    getMarkData = list()
                    markData = getMark.sd_mark(file_path)
                    for c in markData:
                        getMarkData.append((info[0], info[1], info[2], c[0], c[1], c[2], c[3]))
                    query = f"INSERT INTO lv1_3800_5100_mark values (%s, %s, %s, %s, %s, %s, %s)"
                    configuration.cursor.bulk_execute(query, getMarkData)

                elif 'T' == file[0]:
                    getTrackData = list()
                    trackData = getTrack.track(file_path)
                    for c in trackData:
                        getTrackData.append((info[0], info[1], info[2], c[0], c[1], c[2], c[3]))
                    query = f"INSERT INTO lv1_3800_5100_track values (%s, %s, %s, %s, %s, %s, %s)"
                    configuration.cursor.bulk_execute(query, getTrackData)

                elif 'W' == file[0]:
                    getWaypointData = list()
                    waypointData = getWaypoint.waypoint(file_path)
                    for c in waypointData:
                        getWaypointData.append((info[0], info[1], info[2], c[0], c[1], c[2], c[3], c[4]))
                    query = f"INSERT INTO lv1_3800_5100_waypoint values (%s, %s, %s, %s, %s, %s, %s, %s)"
                    configuration.cursor.bulk_execute(query, getWaypointData)


        except Exception as e:
            print(e)
            return False

manager.ModulesManager.RegisterModule(SAMYOUNG_3800_5100_sd_connector)
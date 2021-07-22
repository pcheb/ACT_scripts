import numpy as np
import csv
import math
import logging
import os


def import_model(exportfile):

    imodel = model("test")
    f = open(exportfile, 'r')
    csvreader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)

    for row in csvreader:
        if row[0] == "Body":
            imodel.add_body(row[1], row[2], row[3], row[4], np.array([row[5:8]]))
        elif row[0] == "NamedSelection":
            imodel.add_named_selection(row[1], row[2], row[3:])
        elif row[0] == "Material":
            imodel.add_material(row[1], row[2], row[3:])
        elif row[0] == "Joint":
            imodel.add_joint(row[1], row[2], row[3], row[4:])
        elif row[0] == "MeshControl":
            imodel.add_mesh_control(row[1], row[2], row[3:])
    f.seek(0)

    for row in csvreader:
        if row[0] == "Face":
            imodel.bodies[row[2]].add_face(row[1], row[2], row[3], np.array([row[4:7]]), np.subtract(np.array([row[4:7]]), imodel.bodies[row[2]].centroid))
        elif row[0] == "Edge":
            imodel.bodies[row[2]].add_edge(row[1], row[2], row[3], np.array([row[4:7]]), np.subtract(np.array([row[4:7]]), imodel.bodies[row[2]].centroid))
        elif row[0] == "Vertex":
            imodel.bodies[row[2]].add_vertex(row[1], row[2], row[3], np.array([row[4:7]]), np.subtract(np.array([row[4:7]]), imodel.bodies[row[2]].centroid))
    return imodel


def filter_entities(model1):
    target_entities = []
    for i in model1.named_selections:
        if ("Bonded" in i) and ("Compartment" in i):
            pass
        else:
            ins = model1.named_selections[i]
            target_entities += ins.entities

    for i in model1.joints:
        ins = model1.joints[i]
        if ins.origin:
            target_entities += ins.origin
        if ins.primary_axis:
            target_entities += ins.primary_axis
        if ins.secondary_axis:
            target_entities += ins.secondary_axis

    for i in model1.mesh_controls:
        ins = model1.mesh_controls[i]
        target_entities += ins.entities

    return np.array(target_entities)


def compare_models(model1, model2, stol, dtol):
    id_dict = {}
    target_entities = filter_entities(model1)
    for bid1 in model1.bodies:
        ibody = model1.bodies[bid1]
        if not ibody.suppressed:
            flag = False
            for i in range(5):
                if flag:
                    break
                for bid2 in model2.bodies:
                    jbody = model2.bodies[bid2]
                    if not jbody.suppressed:
                        if math.isclose(ibody.size, jbody.size, rel_tol=stol*4**i):
                            if np.allclose(ibody.centroid, jbody.centroid, rtol=0, atol=dtol*4**i):
                                flag = True
                                foundbody = jbody
                                logger.info("Found body: " + ibody.name + ":" + jbody.name + ":" + str(stol*4**i) + ":" + str(dtol*4**i))
                                break
            if not flag:
                itol = 0.25
                jtol = 5
                for bid2 in model2.bodies:
                    jbody = model2.bodies[bid2]
                    if not jbody.suppressed:
                        if ibody.name == jbody.name:
                            if abs(ibody.size - jbody.size) < itol * max(ibody.size, jbody.size):
                                check_centroid = np.absolute(ibody.centroid - jbody.centroid)
                                if np.all(np.less(check_centroid, np.full(3,jtol))):
                                    #itol = abs(ibody.size - jbody.size)/max(ibody.size, jbody.size)
                                    jtol = np.max(check_centroid)
                                    flag = True
                                    foundbody = jbody
                                    logger.info("Found body: " + ibody.name + ":" + jbody.name)

            if flag:
                id_dict[ibody.id] = int(foundbody.id)
                for fid1 in ibody.faces:
                    iface = ibody.faces[fid1]
                    if iface.id in target_entities:
                        flag = False
                        for i in range(6):
                            if flag:
                                break
                            for fid2 in foundbody.faces:
                                jface = foundbody.faces[fid2]
                                if math.isclose(iface.size, jface.size, rel_tol=stol * (4 ** i)):
                                    if np.allclose(iface.centroid, jface.centroid, rtol=0, atol=dtol * (4 ** i)):
                                        if np.inner(iface.vector,jface.vector) > -0.000000001:
                                            flag = True
                                            id_dict[fid1] = int(fid2)
                                            break
                        if not flag:
                            logger.info("Failed to find face: " + ibody.name + ":" + str(iface.id))


                for fid1 in ibody.edges:
                    iedge = ibody.edges[fid1]
                    if iedge.id in target_entities:
                        flag = False
                        for i in range(6):
                            if flag:
                                break
                            for fid2 in foundbody.edges:
                                jedge = foundbody.edges[fid2]
                                if math.isclose(iedge.size, jedge.size, rel_tol=stol * (4 ** i)):
                                    if np.allclose(iedge.centroid, jedge.centroid, rtol=0, atol=dtol * (4 ** i)):
                                        if np.inner(iedge.vector,jedge.vector) > -0.000000001:
                                            flag = True
                                            id_dict[fid1] = int(fid2)
                                            break
                        if not flag:
                            logger.info("Failed to find edge: " + ibody.name + ":" + str(iedge.id))


                for fid1 in ibody.vertices:
                    ivert = ibody.vertices[fid1]
                    if ivert.id in target_entities:
                        flag = False
                        for i in range(6):
                            if flag:
                                break
                            for fid2 in foundbody.vertices:
                                jvert = foundbody.vertices[fid2]
                                if math.isclose(ivert.size, jvert.size, rel_tol=stol * (4 ** i)):
                                    if np.allclose(ivert.centroid, jvert.centroid, rtol=0, atol=dtol * (4 ** i)):
                                        if np.inner(ivert.vector,jvert.vector) > -0.000000001:
                                            flag = True
                                            id_dict[fid1] = int(fid2)
                                            break
                        if not flag:
                            logger.info("Failed to find vertex: " + ibody.name + ":" + str(ivert.id))

            else:
                logger.info("Failed:" + ibody.name)

    return id_dict


def update_models(model1, model2, id_dict, exportfile):
    f = open(exportfile, 'w', newline='')
    csvwriter = csv.writer(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)

    for i in model1.named_selections:
        ins = model1.named_selections[i]

        new_list = []
        for entity in ins.entities:
            try:
                new_list.append(id_dict[entity])
            except:
                logger.info("Problem in named selection: " + ins.name)
        try:
            model2.named_selections[i].entities = np.array(new_list)
        except:
            model2.add_named_selection(0, i, np.array(new_list))

        csvwriter.writerow(["NamedSelection", i] + new_list)

    for i in model1.materials:
        ins = model1.materials[i]
        new_list = []
        for entity in ins.entities:
            try:
                new_list.append(id_dict[entity])
            except:
                logger.info("Problem in material: " + ins.name)
        try:
            model2.materials[i].entities = np.array(new_list)
        except:
            model2.add_material(0, i, np.array(new_list))

        csvwriter.writerow(["Material", i] + new_list)

    for i in model1.joints:
        ins = model1.joints[i]

        new_list = []
        if ins.origin:
            for entity in ins.origin:
                try:
                    new_list.append(id_dict[entity])
                except:
                    logger.info("Problem in joint: " + ins.name)

            try:
                model2.joints[i].origin = np.array(new_list)
            except:
                model2.add_joint(0, i, "Origin", np.array(new_list))
            csvwriter.writerow(["Joint", i, "Origin"] + new_list)

        new_list = []
        if ins.primary_axis:
            for entity in ins.primary_axis:
                try:
                    new_list.append(id_dict[entity])
                except:
                    logger.info("Problem in joint: " + ins.name)

            try:
                model2.joints[i].primary_axis = np.array(new_list)
            except:
                model2.add_joint(0, i, "PrimaryAxis", np.array(new_list))
            csvwriter.writerow(["Joint", i, "PrimaryAxis"] + new_list)

        new_list = []
        if ins.secondary_axis:
            for entity in ins.secondary_axis:
                try:
                    new_list.append(id_dict[entity])
                except:
                    logger.info("Problem in joint: " + ins.name)

            try:
                model2.joints[i].secondary_axis = np.array(new_list)
            except:
                model2.add_joint(0, i, "SecondaryAxis", np.array(new_list))
            csvwriter.writerow(["Joint", i, "SecondaryAxis"] + new_list)

    for i in model1.mesh_controls:
        ins = model1.mesh_controls[i]

        new_list = []
        for entity in ins.entities:
            try:
                new_list.append(id_dict[entity])
            except:
                logger.info("Problem in mesh control: " + ins.name)
        try:
            model2.mesh_controls[i].entities = np.array(new_list)
        except:
            model2.add_mesh_control(0, i, np.array(new_list))

        csvwriter.writerow(["MeshControl", i] + new_list)

    f.close()


class model():

    def __init__(self, name):
        self.name = name
        self.bodies = {}
        self.named_selections = {}
        self.materials = {}
        self.joints = {}
        self.mesh_controls = {}

    def add_body(self, eid, name, size, suppressed, centroid):
        self.bodies[eid] = Body(eid, name, size, suppressed, centroid)

    def add_named_selection(self, eid, name, entity_list):
        self.named_selections[name] = NamedSelection(eid, name, entity_list)

    def add_material(self, eid, name, entity_list):
        self.materials[name] = Material(eid, name, entity_list)

    def add_joint(self, eid, name, component, entity_list):
        if name not in self.joints:
            self.joints[name] = Joint(eid, name)
        self.joints[name].add_component(component, entity_list)

    def add_mesh_control(self, eid, name, entity_list):
        self.mesh_controls[name] = MeshControl(eid, name, entity_list)


class Body(model):

    def __init__(self, eid, name, size, suppressed, centroid):
        self.id = eid
        self.name = name.split("\\")[-1]
        self.size = size
        self.centroid = centroid
        self.faces = {}
        self.edges = {}
        self.vertices = {}
        if suppressed == "True":
            self.suppressed = True
        else:
            self.suppressed = False

    def add_face(self, eid, pid, size, centroid, vector):
        self.faces[eid] = Face(eid, pid, size, centroid, vector)

    def add_edge(self, eid, pid, size, centroid, vector):
        self.edges[eid] = Edge(eid, pid, size, centroid, vector)

    def add_vertex(self, eid, pid, size, centroid, vector):
        self.vertices[eid] = Vertex(eid, pid, size, centroid, vector)


class Face(Body):

    def __init__(self, eid, pid, size, centroid, vector):
        self.id = eid
        self.pid = pid
        self.size = size
        self.centroid = centroid
        self.vector = vector

class Edge(Body):

    def __init__(self, eid, pid, size, centroid, vector):
        self.id = eid
        self.pid = pid
        self.size = size
        self.centroid = centroid
        self.vector = vector


class Vertex(Body):

    def __init__(self, eid, pid, size, centroid, vector):
        self.id = eid
        self.pid = pid
        self.size = size
        self.centroid = centroid
        self.vector = vector


class NamedSelection(model):

    def __init__(self, eid, name, entity_list):
        self.id = eid
        self.name = name
        self.entities = entity_list


class Material(model):

    def __init__(self, eid, name, entity_list):
        self.id = eid
        self.name = name
        self.entities = entity_list


class Joint(model):

    def __init__(self, eid, name):
        self.id = eid
        self.name = name
        self.origin = None
        self.primary_axis = None
        self.secondary_axis = None

    def add_component(self, component, entity_list):
        if component == "Origin":
            self.origin = entity_list
        elif component == "PrimaryAxis":
            self.primary_axis = entity_list
        elif component == "SecondaryAxis":
            self.secondary_axis = entity_list


class MeshControl(model):

    def __init__(self, eid, name, entity_list):
        self.id = eid
        self.name = name
        self.entities = entity_list


def init_log(logger):
    if logger.handlers:
        logger.handlers[0].close()
        logger.handlers = []

    # logHandler = logging.FileHandler("status.log", mode='w')
    logHandler = logging.FileHandler(logFile, mode='w')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)


def close_log(logger):
    handlers = logger.handlers[:]
    for handler in handlers:
        handler.close()
        logger.removeHandler(handler)




if __name__ == "__main__":
    sourcemodel = r'C:\Users\akarabey\Desktop\ModelCompare\MechModelExport_Source.csv'  # Path to exported csv file
    updatedmodel = r'C:\Users\akarabey\Desktop\ModelCompare\MechModelExport_Target.csv'  # Path to exported csv file
    exportfile = r'C:\Users\akarabey\Desktop\ModelCompare\Mech_Updated_Source.csv'  # Path to exported csv file

    logFile = os.path.join(os.path.dirname(exportfile), 'Step2_Status.log')
    logger = logging.getLogger('StatusLog')
    init_log(logger)

    logger.info("Process Started!")

    model1 = import_model(sourcemodel)
    model2 = import_model(updatedmodel)

    id_dict = compare_models(model1,model2,0.00025,0.002)
    update_models(model1, model2, id_dict, exportfile)


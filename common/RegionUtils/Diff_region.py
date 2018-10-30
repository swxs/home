# -*- coding: utf-8 -*-
# @File    : Diff_region.py
# @AUTH    : swxs
# @Time    : 2018/8/30 17:59

import os
import settings
from api.utils.organization.region import Region
from api.utils.organization.region_type import RegionType
from common.RegionUtils import DataTree

DELETE = 1  # 老的节点被删除了
CHANGE = 2  # 老的节点属性发生了变化
APPEND = 3  # 新增加的节点
CHANGE_NAME = 4  # 老的节点名字发生了改变，(底层相同的code有两个不同的名字， 高层级相同的节点下属的children"<大致?>"相同)
CHANGE_PARENT = 5  # 老的节点父节点发生了改变


class NullNode():
    def __init__(self, name, layer, parent_name):
        self.name = None
        self.layer = layer
        self.parent_name = parent_name
        self.attrs = dict()
        self.children = dict()
        self.count = 0

    def __repr__(self):
        return f"Node: {self.name} layer: {self.layer}"


def diff(old_data_tree, new_data_tree):
    # region_tree = Region.get_region_tree(region)
    index = 0  # 当前节点的标志
    patches = {}  # 用来记录每个节点差异的对象
    return dfsWalk(old_data_tree.tree, new_data_tree.tree, index, patches)


def dfsWalk(oldNode, newNode, index, patches):
    '''
    对两棵树进行深度优先遍历,
    :param oldNode:
    :param newNode:
    :param index:
    :param patches:
    :return:
    '''
    if isinstance(newNode, NullNode):  # 节点被删除
        patches[index] = dict(TYPE=DELETE, old_node=oldNode, new_node=newNode)
    elif isinstance(oldNode, NullNode):  # 节点被添加
        patches[index] = dict(TYPE=APPEND, old_node=oldNode, new_node=newNode)
    else:  # 节点不变， 但可能属性有修改
        if (oldNode.layer == newNode.layer) and (oldNode.name == newNode.name):
            propsPatches = diffProps(oldNode, newNode)
            if propsPatches:
                patches[index] = dict(TYPE=CHANGE, old_node=oldNode, new_node=newNode)
    diffChildrenList(oldNode.children, newNode.children)
    diffChildren(oldNode, newNode, index, patches)
    return patches


def diffChildrenList(oldNode, newNode):
    for key, value in oldNode.items():
        if key not in newNode:
            newNode[key] = NullNode(value.name, value.layer, value.parent_name)

    for key, value in newNode.items():
        if key not in oldNode:
            oldNode[key] = NullNode(value.name, value.layer, value.parent_name)

    return oldNode, newNode


def diffProps(oldNode, newNode):
    propsPatches = dict()
    if oldNode.name != newNode.name:
        propsPatches["name"] = newNode.name
    if oldNode.attrs != newNode.attrs:
        propsPatches["attrs"] = newNode.attrs
    return propsPatches


def diffChildren(oldNode, newNode, index, patches):
    '''
    遍历子节点
    :param oldChildren:
    :param newChildren:
    :param index:
    :param patches:
    :return:
    '''
    leftNode = None
    currentNodeIndex = index
    for child_key, child in oldNode.children.items():
        newChild = newNode.children.get(child_key, None)
        if leftNode and leftNode.count:
            currentNodeIndex = currentNodeIndex + leftNode.count + 1
        else:
            currentNodeIndex = currentNodeIndex + 1
        dfsWalk(child, newChild, currentNodeIndex, patches)  # 深度遍历子节点
        oldNode.count += child.count + 1
        leftNode = child


def get_diff(old_data_tree, new_data_tree):
    patches = diff(old_data_tree, new_data_tree)
    change_dealer = dict()
    change_list = list()
    for key, value in patches.items():
        if value.get("TYPE") == DELETE:
            old_node = value.get('old_node')
            if not old_node.children:
                code = old_node.attrs.get('code')
                if code in change_dealer:
                    index, new_node = change_dealer[code]
                    change_dealer[code] = (index, None)
                    change_dealer[f"{code}_p"] = (key, None)
                    if old_node.name != new_node.name:
                        change_list.append(dict(TYPE=CHANGE_NAME, old_node=old_node, new_node=new_node))
                    if old_node.parent_name != new_node.parent_name:
                        change_list.append(dict(TYPE=CHANGE_PARENT, old_node=old_node, new_node=new_node))
                    propsPatches = diffProps(old_node, new_node)
                    if propsPatches:
                        change_list.append(dict(TYPE=CHANGE, old_node=old_node, new_node=new_node))
                else:
                    change_dealer[code] = (key, old_node)
                    # print(f"delete node - {value.get('old_node')}")
        if value.get("TYPE") == CHANGE:
            pass
            # print(f"changed node - {value.get('old_node')} to node - {value.get('new_node')}")
        if value.get("TYPE") == APPEND:
            new_node = value.get('new_node')
            if not new_node.children:
                code = new_node.attrs.get('code')
                if code in change_dealer:
                    index, old_node = change_dealer[code]
                    change_dealer[code] = (index, None)
                    change_dealer[f"{code}_p"] = (key, None)
                    if old_node.name != new_node.name:
                        change_list.append(dict(TYPE=CHANGE_NAME, old_node=old_node, new_node=new_node))
                    if old_node.parent_name != new_node.parent_name:
                        change_list.append(dict(TYPE=CHANGE_PARENT, old_node=old_node, new_node=new_node))
                    propsPatches = diffProps(old_node, new_node)
                    if propsPatches:
                        change_list.append(dict(TYPE=CHANGE, old_node=old_node, new_node=new_node))
                else:
                    change_dealer[code] = (key, new_node)
                    # print(f"append node - {value.get('new_node')}")

    for code, info_set in change_dealer.items():
        index, value = info_set
        if value is None:
            del patches[index]

    changes = dict(info=list(), msg=list())
    errors = dict(info=list(), msg=list())
    for key, value in patches.items():
        if value.get("TYPE") == DELETE:
            print(f"DELETE node - {value.get('old_node')}")
            errors["info"].append({"TYPE": DELETE, "NODE": value.get('old_node')})
            errors["msg"].append(f"无法删除层级[{value.get('old_node').layer}-{value.get('old_node').name}]")
        if value.get("TYPE") == APPEND:
            print(f"APPEND node - {value.get('new_node')}")
            changes["info"].append({"TYPE": APPEND, "NODE": value.get('new_node')})
            changes["msg"].append(f"新增层级[{value.get('new_node').layer}-{value.get('new_node').name}]")
        if value.get("TYPE") == CHANGE:
            print(f"CHANGED node - {value.get('old_node')} to node - {value.get('new_node')}")
            changes["info"].append({"TYPE": CHANGE, "NODE": value.get('old_node'), "TO": value.get('new_node')})
            changes["msg"].append(f"层级信息修改[{value.get('new_node').layer}-{value.get('new_node').name}]")
    for value in change_list:
        if value.get("TYPE") == CHANGE_NAME:
            print(f"CHANGE_NAME node - {value.get('old_node')} to node - {value.get('new_node')}")
            changes["info"].append({"TYPE": CHANGE_NAME, "NODE": value.get('old_node'), "TO": value.get('new_node')})
            changes["msg"].append(f"层级名修改[{value.get('old_node').layer}-{value.get('old_node').name}] -> [{value.get('new_node').layer}-{value.get('new_node').name}]")
        if value.get("TYPE") == CHANGE_PARENT:
            print(f"CHANGE_PARENT node - {value.get('old_node')} to node - {value.get('new_node')}")
            changes["info"].append({"TYPE": CHANGE_PARENT, "NODE": value.get('old_node'), "TO": value.get('new_node')})
            changes["msg"].append(f"层级信息修改[{value.get('new_node').layer}-{value.get('new_node').name}]")
    return changes, errors


def create_region(region_tree, project_id, company_id):
    current_region_type = None
    for region_type in region_tree.region_type_list:
        if current_region_type is None:
            parent_region_type_id = None
        else:
            parent_region_type_id = current_region_type.id
        current_region_type = RegionType.create(
            display_name=region_type.display_name,
            parent_id=parent_region_type_id,
            project_id=project_id,
            company_id=company_id
        )

    current_region = None
    for node in region_tree:
        region_type = RegionType.get_region_type_by_display_name_project_id(node.layer, project_id)
        if current_region is None:
            parent_id = None
        else:
            parent_region = Region.select(name=node.parent_name, ttype=region_type.parent_id, project_id=project_id)
            parent_id = parent_region.id

        code = node.attrs.get('code', None)
        if code:
            code = str(code)
        current_region = Region.create(
            name=node.name,
            email=node.attrs.get('email', None),
            phone=node.attrs.get('phone', None),
            code=code,
            custom_attr=node.attrs.get('custom_attr'),
            ttype=region_type.id,
            parent_id=parent_id,
            project_id=project_id,
            company_id=company_id,
        )


def patch(changes, project_id, company_id):
    for change in changes:
        if change["TYPE"] == APPEND:
            node = change["NODE"]
            region_type = RegionType.get_region_type_by_display_name_project_id(node.layer, project_id)
            parent_region = Region.get_region_by_name_ttype_project_id(node.parent_name, region_type.parent_id, project_id)
            Region.create(
                name=node.name,
                email=node.attrs.get('email', None),
                phone=node.attrs.get('phone', None),
                code=node.attrs["code"],
                ttype=region_type.id,
                parent_id=parent_region.id,
                project_id=project_id,
                company_id=company_id,
            )
        elif change["TYPE"] == CHANGE:
            node = change["TO"]
            region_type = RegionType.get_region_type_by_display_name_project_id(node.layer, project_id)
            region = Region.select(name=node.name, ttype=region_type.id, project_id=project_id)
            region.update(
                email=node.attrs.get('email', None),
                phone=node.attrs.get('phone', None),
                custom_attr=node.attrs.get('custom_attr', {}),
            )
        elif change["TYPE"] == CHANGE_NAME:
            node = change["NODE"]
            region_type = RegionType.get_region_type_by_display_name_project_id(node.layer, project_id)
            region = Region.select(name=node.name, ttype=region_type.id, project_id=project_id)

            new_node = change["TO"]
            region.update(
                name=new_node.name,
            )
        elif change["TYPE"] == CHANGE_PARENT:
            node = change["NODE"]
            region_type = RegionType.get_region_type_by_display_name_project_id(node.layer, project_id)
            region = Region.select(name=node.name, ttype=region_type.id, project_id=project_id)

            new_node = change["TO"]
            new_parent_region = Region.get_region_by_name_ttype_project_id(new_node.parent_name, region_type.parent_id, project_id)

            region.update(
                parent_id=new_parent_region.id,
            )


if __name__ == "__main__":
    filename_1 = os.path.join(settings.REGION_FILE_PATH, "old_region.xlsx")
    filename_2 = os.path.join(settings.REGION_FILE_PATH, "old_region - 副本.xlsx")

    old_data_tree = DataTree.DataTree(filename=filename_1)
    new_data_tree = DataTree.DataTree(filename=filename_2)

    patches = get_diff(old_data_tree, new_data_tree)

# -*- coding: utf-8 -*-
# @File    : DataTree.py
# @Time    : 2018/3/21 10:43

import os
import datetime
import pandas as pd
from collections import OrderedDict, defaultdict
import settings
from api.utils.organization.region import Region
from api.utils.organization.region_type import RegionType
from common.RegionUtils.InitInfo import InitInfo
from common.RegionUtils import NotExistDealerInfoException, MultiDealerInfoException


class Node(object):
    def __init__(self, name=None, layer=None, parent_name=None, attrs=None, children=None):
        self.name = name
        self.layer = layer
        self.parent_name = parent_name
        self.attrs = dict() if attrs is None else attrs
        self.children = dict() if children is None else children
        self.count = 0

    def __repr__(self):
        return f"Node: {self.name} layer: {self.layer}"


class TypeNode(object):
    def __init__(self, display_name=None):
        self.display_name = display_name

    def __repr__(self):
        return f"TypeNode: {self.display_name}"


class DataTree(object):
    def __init__(self, filename=None):
        self.filename = filename
        self.errors = list()
        self.init()

    def init(self):
        try:
            self.df = pd.read_excel(self.filename).fillna(method='pad')
        except Exception:
            # 校验文件类型
            self.errors.append(f"文件类型或格式不正确")
            return
        layer_list = self.df.columns.tolist()
        if len(layer_list) < 2:
            self.errors.append(f"层级不能过少")
            return
        if len(set(layer_list)) != len(layer_list):
            self.errors.append(f"不能存在相同的层级名称")
            return
        self.root_layer = layer_list[0]
        self.layer_list = layer_list[1:]
        self.region_type_list = []
        self.get_region_type()
        self.node_dict = OrderedDict()
        self.tree = None
        self.dealer_node = dict()
        self.create_tree()
        if self.errors:
            return
        try:
            self.initinfo = InitInfo(filename=self.filename, layer_list=layer_list)
        except MultiDealerInfoException as e:
            self.errors.append(f"不能存在相同的层级信息: {e.multiple_list}")
            return
        except NotExistDealerInfoException:
            self.errors.append(f"必须存在最低层级的信息表")
            return
        except NotExistDealerCodeInfoException:
            self.errors.append(f"必须存在最低层级的编号信息")
            return
        self.contain_info()

    def __iter__(self):
        return iter(self.node_dict.values())

    def get_region_type(self):
        self.region_type_list.append(TypeNode(self.root_layer))
        for layer in self.layer_list:
            self.region_type_list.append(TypeNode(layer))

    def create_tree(self):
        self.tree = Node(
            name=self.df.iloc[0][self.root_layer],
            layer=self.root_layer,
            parent_name=None,
            attrs=dict(custom_attr=dict(), code=None, email=None, phone=None),
            children=dict()
        )
        self._add_node_map(self.df.iloc[0][self.root_layer], self.root_layer, self.tree)

        for index, series in self.df.iterrows():
            parent_node = self.tree
            for layer in self.layer_list:
                name = series[layer]
                node = parent_node.children.get(name)
                if not node:
                    if self._get_node(name, layer):
                        self.errors.append(f"层级[{parent_node.layer}-{parent_node.name}]下存在错误的层级[{layer}-{name}]")
                    node = Node(
                        name=name,
                        layer=layer,
                        parent_name=parent_node.name,
                        attrs=dict(custom_attr=dict(), code=None, email=None, phone=None),
                        children=dict()
                    )
                    if layer == self.layer_list[-1]:
                        self.dealer_node[(name, layer)] = node
                    parent_node.children.update({name: node})
                    self._add_node_map(name, layer, node)
                parent_node = node

    def contain_info(self):
        code_list = list()
        for info in self.initinfo:
            try:
                node = self.node_dict[(info.get('name'), info.get('layer'))]
            except:
                self.errors.append(f"层级[{info.get('layer')}-{info.get('name')}]不在结构表中， 无法设置层级信息")
                continue
            if node is None:
                pass  # 多了信息
            for attr, value in info.items():
                if attr in ["code"]:
                    node.attrs[attr] = str(value)
                elif attr in ["name", "layer"]:
                    pass
                elif attr in ["email", "phone"]:
                    if value is None:
                        node.attrs[attr] = None
                    else:
                        node.attrs[attr] = str(value)
                else:
                    node.attrs["custom_attr"][attr] = value

            if info.get('layer') == self.layer_list[-1]:
                if "code" not in node.attrs:
                    self.errors.append(f"最低层级[{node.layer}-{node.name}]必须存在【code】信息")
                if (node.attrs["code"] in code_list):
                    self.errors.append(f"两个最低层级不能有相同的【code】信息 - {node.attrs['code']}")
                code_list.append(node.attrs["code"])
        if len(code_list) < len(list(self.dealer_node.keys())):
            self.errors.append(f"存在最低层级缺失【code】信息")

    def _add_node_map(self, name, layer, node):
        self.node_dict.update({(name, layer): node})

    def _get_node(self, name, layer):
        return self.node_dict.get((name, layer))

    def _is_leaf_node(self, name, layer):
        node = self._get_node(name, layer)
        return node is not None and node.children == {}

    def get_tree_chain(self, name, layer):
        node_list = []
        while True:
            current_node = self._get_node(name, layer)
            if current_node:
                node_list.append(current_node)
                parent_name = current_node.parent_name
                if parent_name is None:
                    break
                name = parent_name
            else:
                break
        node_list.reverse()
        return node_list


class DataTreeFromMongo(object):
    def __init__(self, project_id):
        self.project_id = project_id
        self.region = Region.get_first_region_by_project_id(self.project_id)
        self.tree = None
        self.all_layer_list = self.get_layer_list()
        self.root_layer = self.all_layer_list[0]
        self.layer_list = self.all_layer_list[1:]
        self.dealer_node = dict()
        self.node_dict = OrderedDict()
        self.create_tree()

    def __iter__(self):
        return iter(self.node_dict.values())

    def get_layer_list(self):
        region_type_list = RegionType.get_region_type_list_by_project_id(self.project_id)
        return [region_type.display_name for region_type in region_type_list]

    def _add_region(self, region_id):
        region = Region.get_region_by_region_id(region_id)
        region_type = RegionType.get_region_type_by_id(region.ttype)
        if region.parent_id is None:
            parent_name = None
        else:
            parent_region = Region.get_region_by_region_id(region.parent_id)
            parent_name = parent_region.name
        node = Node(
            name=region.name,
            layer=region_type.display_name,
            parent_name=parent_name,
            attrs=dict(custom_attr=region.custom_attr, code=region.code, email=region.email, phone=region.phone),
            children=dict()
        )
        self._add_node_map(region.name, region_type.display_name, node)
        return node, region

    def _add_node_map(self, name, layer, node):
        self.node_dict.update({(name, layer): node})

    def create_tree(self):
        def add_node(region):
            node, region = self._add_region(region.id)

            if node.layer == self.layer_list[-1]:
                self.dealer_node[(node.name, node.layer)] = node

            for children_region in Region.get_region_list_by_parent_region_id(region.oid):
                children_node = add_node(children_region)
                node.children[children_node.name] = children_node
            return node

        self.tree = add_node(self.region)

    def convert_to_file(self):
        data = defaultdict(list)
        info_data_dict = dict()

        def _add_info(node):
            if node.layer not in info_data_dict:
                info_data_dict[node.layer] = defaultdict(list)
            data[node.layer].append(node.name)
            if node.name not in info_data_dict[node.layer]["name"]:
                info_data_dict[node.layer]["name"].append(node.name)
                if node.layer == self.layer_list[-1]:
                    info_data_dict[node.layer]["code"].append(node.attrs["code"])
                info_data_dict[node.layer]["email"].append(node.attrs["email"])
                info_data_dict[node.layer]["phone"].append(node.attrs["phone"])

        for (name, layer), node in self.dealer_node.items():
            current_node = node
            while current_node:
                _add_info(current_node)
                index = self.all_layer_list.index(current_node.layer)
                if index == 0:
                    break
                current_layer = self.all_layer_list[index - 1]
                if current_node.parent_name is None:
                    break
                current_node = self._get_node(current_node.parent_name, current_layer)

        filepath = os.path.join(settings.REGION_FILE_PATH, f"{self.project_id}_{datetime.datetime.now():%Y%m%d%H%M%S}.xlsx")

        with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
            pd.DataFrame(data).to_excel(writer, sheet_name="首页", index=False, columns=self.all_layer_list)
            for layer in self.all_layer_list:
                if layer == self.layer_list[-1]:
                    pd.DataFrame(info_data_dict[layer]).to_excel(writer, sheet_name=layer, index=False, header=["名称", "门店编码", "邮箱", "联系方式"], columns=["name", "code", "email", "phone"])
                else:
                    pd.DataFrame(info_data_dict[layer]).to_excel(writer, sheet_name=layer, index=False, header=["名称", "邮箱", "联系方式"], columns=["name", "email", "phone"])
            writer.save()
        return filepath

    def _get_node(self, name, layer):
        return self.node_dict.get((name, layer))

    def _is_leaf_node(self, name, layer):
        node = self._get_node(name, layer)
        return node is not None and node.children == {}


if __name__ == "__main__":
    region = Region.get_region_by_region_id("5b99caa6c332011cf8744750")
    d = DataTreeFromMongo(region)
    print(d)

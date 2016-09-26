# ***** BEGIN GPL LICENSE BLOCK *****
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****

# <pep8 compliant>

bl_info = {
    "name": "Reference Library",
    "author": "Inês Almeida, Francesco Siddi",
    "version": (0, 1, 0),
    "blender": (2, 78, 0),
    "location": "View3D > Tool Shelf (T)",
    "description": "todo",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/"
                "Scripts/System/-todo-create-new-documentation-page!",
    "category": "System",
}

import os
import json

import bpy
from bpy.types import (
    Operator,
    Menu,
    Panel,
    UIList,
    PropertyGroup,
)
from bpy.props import (
    IntProperty,
    StringProperty,
    EnumProperty,
    CollectionProperty,
    PointerProperty,
)


# load single json library file
asset_categories = {}
with open(os.path.join(os.path.dirname(__file__), "lib.json")) as data_file:
    asset_categories = json.load(data_file)


# Data Structure ##############################################################

class AssetItem(PropertyGroup):
    name = StringProperty(
        name="",
        description="",
    )
    # type = enum?


class AssetCollection(PropertyGroup):
    name = StringProperty(
        name="Asset Collection Name",
        description="",
    )
    active_asset = IntProperty(
        name="",
        description="",
    )
    assets = CollectionProperty(
        name="",
        description="",
        type=AssetItem,
    )


# Operators ###################################################################

class ASSET_OT_ref_library_reload_from_json(Operator):
    bl_idname = "wm.reflib_reload_from_json"
    bl_label = "Reload from JSON"
    bl_description = ""
    bl_options = {'UNDO', 'REGISTER'}

    @classmethod
    def poll(self, context):
        return True

    def execute(self, context):
        wm = context.window_manager
        wm.reflib_cols.clear()
        for col_name in asset_categories:
            asset_collection_prop = wm.reflib_cols.add()
            asset_collection_prop.name = col_name
            for asset_name, asset_def in asset_categories[col_name].items():
                asset_prop = asset_collection_prop.assets.add()
                asset_prop.name = asset_name
                # TODO to be continued
        # todo verify, clear, frees nested, default value for asset active?
        return {'FINISHED'}


class ASSET_OT_ref_library_assetlist_add(Operator):
    bl_idname = "wm.reflib_assetlist_add"
    bl_label = "Add Asset"
    bl_description = "Add a new asset to the selected collection"
    bl_options = {'UNDO', 'REGISTER'}

    def execute(self, context):
        # todo
        return {'FINISHED'}

class ASSET_OT_ref_library_assetlist_del(Operator):
    bl_idname = "wm.reflib_assetlist_del"
    bl_label = "Delete Asset"
    bl_description = "Delete the selected asset"
    bl_options = {'UNDO', 'REGISTER'}

    def execute(self, context):
        # todo
        return {'FINISHED'}

# Panel #######################################################################

class ASSET_UL_collection_assets(UIList):
    def draw_item(self, context, layout, data, set, icon, active_data, active_propname, index):
        layout.prop(set, "name", text="", icon='QUESTION', emboss=False)


class ASSET_PT_ref_library(Panel):
    bl_label = 'Reference Library'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Ref Library'

    @classmethod
    def poll(cls, context):
        # restrict availability?
        return True #(context.mode == 'OBJECT')

    def draw(self, context):
        wm = context.window_manager

        layout = self.layout

        layout.operator("wm.reflib_reload_from_json", icon="FILE_REFRESH")

        # Category selector

        row = layout.row(align=True)
        row.prop_search(
            wm, "reflib_active_col",# Currently active
            wm, "reflib_cols",      # Collection to search
            text="", icon="QUESTION"# UI icon and label
        )
        row.operator("render.preset_add", text="", icon='OUTLINER_DATA_FONT')
        row.operator("render.preset_add", text="", icon='ZOOMIN')
        row.operator("render.preset_add", text="", icon='ZOOMOUT')

        # UI List with the assets of the selected category

        row = layout.row()
        if (wm.reflib_active_col):
            asset_collection = wm.reflib_cols[wm.reflib_active_col]
            row.template_list(
               "ASSET_UL_collection_assets", "", # type and unique id
                asset_collection, "assets",      # pointer to the CollectionProperty
                asset_collection, "active_asset",# pointer to the active identifier
                rows=4,
            )
            # add/remove/specials UI list Menu
            col = row.column(align=True)
            col.operator("wm.reflib_assetlist_add", icon='ZOOMIN', text="")
            col.operator("wm.reflib_assetlist_del", icon='ZOOMOUT', text="")
            #col.menu("ASSET_MT_reflib_assetlist_specials", icon='DOWNARROW_HLT', text="")
        else:
            row.enabled = False
            row.label("No Asset Collection Selected")



# Registry ####################################################################

def register():

    bpy.utils.register_module(__name__)

    bpy.types.WindowManager.reflib_cols = CollectionProperty(
        name="Reference Library Add-on ColProperties",
        description="Properties and data used by the Reference Library Add-on",
        type=AssetCollection,
    )

    bpy.types.WindowManager.reflib_active_col = StringProperty(
        name="",
        description="",
    )
    # could be pointer instead of string?
    #PointerProperty(type=AssetCollection, options={'EDITABLE'}) # needs PROP_EDITABLE but it's not exposed yet?
    # Sev pointed to:
    # https://www.blender.org/api/blender_python_api_current/bpy.types.Property.html#bpy.types.Property.is_readonly


def unregister():

    del bpy.types.WindowManager.reflib_active_col
    del bpy.types.WindowManager.reflib_cols

    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
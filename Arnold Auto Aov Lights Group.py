import maya.cmds as cmds



# ------------------------

# Created by Pramod G

# Version: 1.0

# ArtStation: https://www.artstation.com/pramod_pro

# LinkedIn: https://www.linkedin.com/in/pramod-g-38064a53/

# ------------------------



# Global counter to maintain group index between runs

aov_group_index = [0]



# ------------------------

# Assign AOV Groups Function

# ------------------------



def assign_aov_light_groups_with_prefix(prefix="multiLight", only_selected=False, filter_arnold=True, filter_standard=True):

    arnold_lights = ['aiAreaLight', 'aiSkyDomeLight', 'aiPhotometricLight', 'aiMeshLight', 'aiLight']

    standard_lights = ['pointLight', 'directionalLight', 'spotLight', 'areaLight', 'volumeLight']



    all_lights = []

    if only_selected:

        all_lights = cmds.ls(selection=True, transforms=True)

    else:

        if filter_arnold:

            for light_type in arnold_lights:

                all_lights += cmds.listRelatives(cmds.ls(type=light_type), parent=True) or []

        if filter_standard:

            for light_type in standard_lights:

                all_lights += cmds.listRelatives(cmds.ls(type=light_type), parent=True) or []



    if not all_lights:

        cmds.warning("No lights found based on current filters.")

        cmds.confirmDialog(title='No Lights', message='No lights found based on current filters.', button=['OK'])

        return



    all_lights = list(set(all_lights))

    all_lights.sort()



    cmds.undoInfo(openChunk=True)



    if cmds.window("progressWin", exists=True):

        cmds.deleteUI("progressWin")

    cmds.window("progressWin", title="Assigning AOVs...", widthHeight=(300, 50))

    cmds.columnLayout()

    progress_control = cmds.progressBar(maxValue=len(all_lights), width=280)

    cmds.showWindow("progressWin")



    if only_selected:

        aov_name = f"{prefix}{str(aov_group_index[0]).zfill(2)}"

        aov_group_index[0] += 1

        for light in all_lights:

            shape = cmds.listRelatives(light, shapes=True)

            if shape:

                shape = shape[0]

                if not cmds.attributeQuery("aiAov", node=shape, exists=True):

                    cmds.addAttr(shape, longName="aiAov", dataType="string")

                cmds.setAttr(f"{shape}.aiAov", aov_name, type="string")

            cmds.progressBar(progress_control, edit=True, step=1)

    else:

        for i, light in enumerate(all_lights):

            aov_name = f"{prefix}{str(i).zfill(2)}"

            shape = cmds.listRelatives(light, shapes=True)

            if shape:

                shape = shape[0]

                if not cmds.attributeQuery("aiAov", node=shape, exists=True):

                    cmds.addAttr(shape, longName="aiAov", dataType="string")

                cmds.setAttr(f"{shape}.aiAov", aov_name, type="string")

            cmds.progressBar(progress_control, edit=True, step=1)



    cmds.deleteUI("progressWin")

    cmds.undoInfo(closeChunk=True)



    cmds.confirmDialog(

        title='Success',

        message=f'{len(all_lights)} lights assigned AOV groups.',

        button=['OK']

    )



# ------------------------

# UI Creation Function

# ------------------------



def create_arnold_auto_light_group_pro_ui():

    window_name = "arnoldAutoLightGroupProWin"

    if cmds.window(window_name, exists=True):

        cmds.deleteUI(window_name)



    cmds.window(window_name, title="Arnold Auto Light Group Naming Pro", widthHeight=(420, 420), sizeable=False, backgroundColor=(0.16, 0.16, 0.16))

    cmds.columnLayout(adjustableColumn=True, rowSpacing=10)



    # Header

    cmds.text(label="Arnold Auto Light Group Naming Pro", align="center", height=40, font="boldLabelFont", backgroundColor=(0.2, 0.2, 0.2))



    # Creator & Links

    cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, 400)], columnSpacing=[(1, 10)])

    cmds.text(label="Created by: Pramod G", align="left", backgroundColor=(0.2, 0.2, 0.2))

    cmds.textField(text="https://www.artstation.com/pramod_pro", editable=False, backgroundColor=(0.3, 0.3, 0.3))

    cmds.textField(text="https://www.linkedin.com/in/pramod-g-38064a53/", editable=False, backgroundColor=(0.3, 0.3, 0.3))

    cmds.text(label="Version: 1.0", align="left", backgroundColor=(0.2, 0.2, 0.2))

    cmds.setParent('..')



    # Scene Light Info

    cmds.frameLayout(label="Scene Light Info", collapsable=True, bgc=(0.25, 0.25, 0.25))

    cmds.columnLayout(adjustableColumn=True)

    cmds.text('lightCountLabel', label="Counting...", align="center", height=20)

    cmds.setParent('..')

    cmds.setParent('..')



    # Options

    cmds.frameLayout(label="Options", collapsable=True, bgc=(0.3, 0.3, 0.3))

    cmds.columnLayout(adjustableColumn=True, rowSpacing=5)

    cmds.textFieldGrp('prefixField', label='Light Group Prefix:', text='multiLight', backgroundColor=(0.2, 0.2, 0.2))

    cmds.checkBoxGrp('filterLights', numberOfCheckBoxes=2, label='Light Types:', 

                     labelArray2=['Arnold Lights', 'Standard Lights'], value1=True, value2=True)

    cmds.checkBox('selectedOnly', label="Only Selected Lights (Grouped together)", value=False)

    cmds.separator(height=10, style='in')

    cmds.text(label="Tip: When using selected lights, each click assigns\na new group number like multiLight00, 01, etc.", align='center', height=40, backgroundColor=(0.25, 0.25, 0.25))

    cmds.setParent('..')

    cmds.setParent('..')



    # Actions

    cmds.frameLayout(label="Actions", collapsable=True, bgc=(0.35, 0.35, 0.35))

    cmds.columnLayout(adjustableColumn=True, rowSpacing=8)

    cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, 200), (2, 200)], columnSpacing=[(1, 5), (2, 5)])

    cmds.button(label="Assign AOV Groups", command=lambda x: run_assignment(), backgroundColor=(0.3, 0.5, 0.4), height=40)

    cmds.button(label="Refresh Light Count", command=lambda x: update_light_count(), backgroundColor=(0.4, 0.4, 0.6), height=40)

    cmds.setParent('..')

    cmds.setParent('..')



    # Close Button

    cmds.button(label="Close", command=lambda *_: cmds.deleteUI(window_name), backgroundColor=(0.5, 0.2, 0.2), height=40)



    cmds.showWindow(window_name)

    update_light_count()



# ------------------------

# Run Assignment

# ------------------------



def run_assignment():

    prefix = cmds.textFieldGrp('prefixField', query=True, text=True)

    filter_values = cmds.checkBoxGrp('filterLights', query=True, valueArray2=True)

    only_selected = cmds.checkBox('selectedOnly', query=True, value=True)



    assign_aov_light_groups_with_prefix(

        prefix=prefix,

        only_selected=only_selected,

        filter_arnold=filter_values[0],

        filter_standard=filter_values[1]

    )

    update_light_count()



# ------------------------

# Update Light Count

# ------------------------



def update_light_count():

    arnold_lights = ['aiAreaLight', 'aiSkyDomeLight', 'aiPhotometricLight', 'aiMeshLight', 'aiLight']

    standard_lights = ['pointLight', 'directionalLight', 'spotLight', 'areaLight', 'volumeLight']

    all_lights = []

    for light_type in arnold_lights + standard_lights:

        all_lights += cmds.listRelatives(cmds.ls(type=light_type), parent=True) or []

    unique_lights = list(set(all_lights))

    cmds.text('lightCountLabel', edit=True, label=f"{len(unique_lights)} lights found.")



# ------------------------

# Launch UI

# ------------------------



create_arnold_auto_light_group_pro_ui()

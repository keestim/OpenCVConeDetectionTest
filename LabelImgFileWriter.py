import os

def exportFile(file_path, valid_hull_data_list, frame_metadata):
    print("Exporting File for: " + str(file_path))
    print(file_path.split("."))

    output_file = file_path
    output_file = output_file.replace(file_path.split(".")[-1], "") + "xml"

    with open(output_file, "w+") as xml_file:
        xml_file.write("<annotation>" + '\n')

        parent_folder = file_path.split("/")[-2]
        xml_file.write("    <folder>" + parent_folder + "</folder>" + '\n')
        
        filename = file_path.split("/")[-1]
        xml_file.write("    <filename>" + filename +"</filename>" + '\n')
        
        xml_file.write("    <path>" + file_path + "</path>" + '\n')
        
        xml_file.write("    <source>" + '\n')
        xml_file.write("        <database>Unknown</database>" + '\n')
        xml_file.write("    </source>" + '\n')

        xml_file.write("    <size>" + '\n')
        xml_file.write("        <width>" + str(frame_metadata["width"]) + "</width>" + '\n')
        xml_file.write("        <height>" + str(frame_metadata["height"]) + "</height>" + '\n')
        xml_file.write("        <depth>" + str(frame_metadata["channels"]) + "</depth>" + '\n')
        xml_file.write("    </size>" + '\n')
            
        for hull_data in valid_hull_data_list:
            xml_file.write("    <object>" + '\n')
            xml_file.write("        <name>cone</name>" + '\n')
            xml_file.write("        <pose>Unspecified</pose>" + '\n')

            xml_file.write("        <truncated>0</truncated>" + '\n')
            xml_file.write("        <difficult>0</difficult>" + '\n')


            xml_file.write("        <bndbox>" + '\n')
            xml_file.write("            <xmin>" + str(hull_data.getX()) + "</xmin>" + '\n')
            xml_file.write("            <ymin>" + str(hull_data.getY()) + "</ymin>" + '\n')
            xml_file.write("            <xmax>" + str(hull_data.getX() + hull_data.getWidth()) + "</xmax>" + '\n')
            xml_file.write("            <ymax>" + str(hull_data.getY() + hull_data.getHeight()) + "</ymax>" + '\n')

            xml_file.write("        </bndbox>" + '\n')

            xml_file.write("    </object>" + '\n')

        xml_file.write("    <segmented>0</segmented>" + '\n')
        
        xml_file.write("</annotation>" + '\n')

        print("File complete")
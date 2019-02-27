# LabelBox Annotation Guide:

## 1. Create new project:
1. After successful sign-up/sign-in under the project tab, click on new project.
1. Give a name to the project.
1. Under `Attach Dataset` section, choose the `upload new dataset` to upload the dataset.
1. Then give a name to the dataset.
1. Under `Customize your labeling interface` section, choose the `SELECT EXISTING` and select `Image Labeling`.

## 2. Configure Interface:
1. Delete all the existing object by clicking on the delete icon of the object on the side panel.
1. Now click on `Add Object` , give name as `line-border` and select `line` as annotation method.
1. Again click on `Add Object`, give name as `side-text` and select `Polygon` as annotation method.
1. Delete all the classification under the `Classifications` section on the side panel.
1. Now click on confrim.
1. Then click on the `COMPLELTE SETUP`. 
1. Finally click on `Start Labeling` to start the Labeling/Annotation process.

## 3. Annotaion/Labeling Procedure:

### line-border:
1. Select `line-border` annotation method and start labeling as polylines separating various text lines.
1. Annotation guide:
    - Zoom in the image for better labeling.
    - Start from left to right.
    - The starting and ending point of polyline (line-border) should not touch the border of Pecha.
    - Select a point just near the text without touching them [Tips: Zoom-in for better visual] except for the place where top and bottom characters are touched, select an appropriate point can separate out the two characters.
    
### Side-text:
1. Select `line-border` annotation method and start labeling as polygon to surround the side text.
1. Annotation guide:
    - Zoom in the image for better labeling.
    - Construct a polygon that can perfectly surround the side text.
    
## 4. Export the label: 
1. Click on the home button at top of the side panel.
1. Click the `Export` tab, select `Export Type` as `JSON` and `Label Format` as `XY` and set `Generate Mask` ON.
1. Finally click on `GENERATE EXPORT`. 
1. To download the label file, Click on the `Tasks` as top-right and click on the download icon.

# CAD enabled brain tumor segmentation tool

Annotater tool for Brain Tumor which creates the initial mask using deep learning and provides 
tool to work with on the mask after initial mask using Plotly and dash.

It's supposed to help with the work of radiologists to reduce the error and reduce repetive work.


### Four Main Components:
- `Model`: Holds details regarding the model that was trained and other details. Model is written in pytorch(UNET) and used figshare dataset.
- `segment_server`: Flask server that serves the inference model using REST api
- `vectorization_server`: NodeJs-Express server that converts Raster images to Vector Image svg path. These svg path are the masks that can can overlaid on the orginal tumor for annotation purpose
- `annotation_client`: Dash app that provides the front-end to work with the segmentation server and allows for manual annoation after automatic annoation annotation is done by model.




#### Plan of Action:
<img src="./assets/planofaction.jpeg " alt="drawing"/>
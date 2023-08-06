function merge(main, secondary, deeper) {
    let primary = deeper ? structuredClone(main) : main;
    for (let sKey in secondary) {
        if (!primary[sKey]) primary[sKey] = secondary[sKey];
        else {
            if (typeof secondary === "object") {
                merge(primary[sKey], secondary[sKey], deeper);
            } else {
                if ([undefined, null, ""].indexOf(primary[sKey]) >= 0) primary[sKey] = secondary[sKey];
            }
        }
    }
    return primary;
}

obj1 = { value: [{ "id": "Model Training", 
"struct": [{ "key": "Epoch", "component": "ProgressElement", "data": { "current": 1, "max": 1 } },
 { "key": "Batch Progress", "component": "ProgressElement", "data": { "current": 131, "max": 307 } },
  { "key": "Training Loss", "component": "ChartElement", "labels": { "label_x": "", "label_y": "" }, "data": { "x": [], "y": [] } },
   { "key": "Logs", "component": "LogElement", "data": ["Loading settings from /dls/science/users/jig77871/projects/volume-segmantics/volseg-settings/2d_model_train_settings.yaml", "Calculating mean of data...", "Mean value: 126.89677798748016", "Number of classes in segmentation dataset: 2", "These classes are: [  0 255]", "Fixing label classes.", "Slicing data volume and saving slices to disk", "Slicing label volume and saving slices to disk", "Free GPU memory is 4.93 GB. Batch size will be 2.", "Using DiceLoss", "Using MeanIoU", "Setting up the model on device 0.", "Sending the U-Net model to device 0", "Freezing model with 24430242 trainable parameters, 24430242 total parameters.", "Model has 3340898 trainable parameters, 24430242 total parameters.", "Trainer created.", "Finding learning rate for model.", "Training for 1 epochs to create a learning rate plot."] }, { "key": "Sample Images", "component": "GalleryElement", "data": [] }], "active": true }] }

obj2 = { value: [{"id": "Model Training", "struct": [{"key": "Epoch", "component": "ProgressElement", "data": {"current": 1, "max": 1}}, {"key": "Batch Progress", "component": "ProgressElement", "data": {"current": 138, "max": 307}}, {"key": "Training Loss", "component": "ChartElement", "labels": {"label_x": "", "label_y": ""}, "data": {"x": [], "y": []}}, {"key": "Logs", "component": "LogElement", "data": ["Loading settings from /dls/science/users/jig77871/projects/volume-segmantics/volseg-settings/2d_model_train_settings.yaml", "Calculating mean of data...", "Mean value: 126.89677798748016", "Number of classes in segmentation dataset: 2", "These classes are: [  0 255]", "Fixing label classes.", "Slicing data volume and saving slices to disk", "Slicing label volume and saving slices to disk", "Free GPU memory is 4.93 GB. Batch size will be 2.", "Using DiceLoss", "Using MeanIoU", "Setting up the model on device 0.", "Sending the U-Net model to device 0", "Freezing model with 24430242 trainable parameters, 24430242 total parameters.", "Model has 3340898 trainable parameters, 24430242 total parameters.", "Trainer created.", "Finding learning rate for model.", "Training for 1 epochs to create a learning rate plot."]}, {"key": "Sample Images", "component": "GalleryElement", "data": []}], "active": true}]}

console.log(merge(obj1,obj2).value.struct)
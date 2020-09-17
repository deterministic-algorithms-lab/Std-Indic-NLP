# Adding Another NMT dataset 


The code must take at least one argument ```--data_path```  and 2 flags ```--merge```, ```--delete_old```.

If the ```--merge``` flag is provided, the code should append to the existing dataset provided. If not provided, the code should make new dataset in the standard format, in the location specified by ```--data_path```.

If the ```--delete_old``` flag is provided, only one copy of data must be there. That is, data from previous steps of pipeline are deleted, as we move ahead.

Also, add a section corresponding to your dataset in the ```README.md``` file of the ```NMT/``` folder. The section must have the link to dataset and/or its description. And also include example commands, if you decided to include arguments other than those given in the **Template** below.

## Template 

See ```template.py```.

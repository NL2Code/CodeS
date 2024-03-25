# whereami

Uses WiFi signals and machine learning (sklearn's RandomForest) to predict where you are. Even works for small distances like 2-10 meters.

Your computer will known whether you are on Couch #1 or Couch #2.

### Usage

```bash
# in your bedroom, takes a sample
whereami learn -l bedroom

# in your kitchen, takes a sample
whereami learn -l kitchen

# get a list of already learned locations
whereami locations

# cross-validated accuracy on historic data
whereami crossval
# 0.99319

# use in other applications, e.g. by piping the most likely answer:
whereami predict | say
# Computer Voice says: "bedroom"

# probabilities per class
whereami predict_proba
# {"bedroom": 0.99, "kitchen": 0.01}
```

If you want to delete some of the last lines, or the data in general, visit your `$USER/.whereami` folder.

### Python

Any of the functionality is available in python as well. Generally speaking, commands can be imported:

```python
from whereami import learn
from whereami import get_pipeline
from whereami import predict, predict_proba, crossval, locations
```
===================
Engine
===================

A Utility Library that assists in Geospatial Machine Learning Experiment Tracking.

Installation
------------

```pip install granular-engine```


Usage
-----

>>> from engine import Engine
>>>
>>> # Make a config.yaml with GeoEngine projectId and exportId and other necessary details
>>> engine = Engine("config.yaml")
>>>
>>> for epoch in enumerate(epochs):
>>>   # train 
>>>   # eval
>>>   engine.log(step=epoch, train_loss=train_loss, val_loss=val_loss)
>>>
>>> engine.done()


License
-------
GPLv3

Documentation
-------------

View documentation `here <https://engine.granular.ai/>`_

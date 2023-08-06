class RecModel(TheseusLayer):
    def __init__(self, **config):
        super().__init__()
        backbone_config = config["Backbone"]
        backbone_name = backbone_config.pop("name")
        self.backbone = eval(backbone_name)(**backbone_config)
        if "BackboneStopLayer" in config:
            backbone_stop_layer = config["BackboneStopLayer"]["name"]
            self.backbone.stop_after(backbone_stop_layer)
        self.head = nn.Linear(1024, 4)

    def forward(self, x):
        out = dict()
        x = self.backbone(x)
        x = x["avg_pool"].flatten(start_axis=1, stop_axis=-1)
        x = self.head(x)
        return x
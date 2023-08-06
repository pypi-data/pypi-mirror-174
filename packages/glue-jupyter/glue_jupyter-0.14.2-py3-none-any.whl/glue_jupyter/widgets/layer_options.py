import ipyvuetify as v
from glue.core import Subset

__all__ = ['LayerOptionsWidget']


import traitlets
import ipywidgets as widgets
from glue.core import message as msg
from glue.core.hub import HubListener
from glue.utils import avoid_circular

from ..vuetify_helpers import WidgetCache


class LayerOptionsWidget(v.VuetifyTemplate, HubListener):
    """
    A widget that contains a way to select layers, and will automatically show
    the options for the selected layer.
    """

    template_file = (__file__, 'layeroptions.vue')
    layers = traitlets.List().tag(sync=True, **widgets.widget_serialization)
    selected = traitlets.Int(0).tag(sync=True)
    color_menu_open = traitlets.Bool(False).tag(sync=True)

    def __init__(self, viewer):
        super().__init__()
        self.viewer = viewer

        self.widgetCache = WidgetCache()
        self.observe(self._update_glue_state_from_layers, 'layers')

        self.current_layers_data = None

        self.viewer.session.hub.subscribe(self, msg.DataUpdateMessage,
                                          handler=self._on_data_or_subset_update)
        self.viewer.session.hub.subscribe(self, msg.SubsetUpdateMessage,
                                          handler=self._on_data_or_subset_update)

        # The first call below looks for changes in self.viewer.layers and
        # the second call looks for changes in self.viewer.state.layers. The
        # second one is needed to watch for changes in e.g. layer visibility,
        # the first one is needed because the callback function needs access
        # to the layer artist and in some cases the new layer artist hasn't been
        # created yet even if state.layers is up-to-date.
        self.viewer._layer_artist_container.on_changed(self._update_layers_from_glue_state)
        self.viewer.state.add_callback('layers', self._update_layers_from_glue_state)
        self._update_layers_from_glue_state()

    def layer_data(self, layer_artist):
        if isinstance(layer_artist.state.layer, Subset):
            label = layer_artist.layer.data.label + ':' + layer_artist.state.layer.label
        else:
            label = layer_artist.state.layer.label

        return {
            'color': getattr(layer_artist.state, 'color', ''),
            'label': label,
            'visible': layer_artist.state.visible,
        }

    def layer_to_dict(self, layer_artist, index):
        def make_layer_panel():
            widget_cls = self.viewer._layer_style_widget_cls
            if isinstance(widget_cls, dict):
                return widget_cls[type(layer_artist)](layer_artist.state)
            else:
                return widget_cls(layer_artist.state)

        data = self.layer_data(layer_artist)
        data.update({
            'index': index,
            'layer_panel': self.widgetCache.get_or_create(layer_artist, make_layer_panel)
        })
        return data

    @avoid_circular
    def _update_layers_from_glue_state(self, *args):

        new_layers_data = [self.layer_data(layer) for layer in self.viewer.layers]

        # During the creation of the new widgets, layers can change again, causing a
        # recursive loop. Short circuit this by checking if the content of the layers has
        # actually changed.
        if self.current_layers_data == new_layers_data:
            return

        self.current_layers_data = new_layers_data

        self.layers = [self.layer_to_dict(layer_artist, i) for i, layer_artist in
                       enumerate(self.viewer.layers)]

    def _on_data_or_subset_update(self, msg):
        if msg.attribute in ('label', 'style'):
            self._update_layers_from_glue_state()

    @avoid_circular
    def _update_glue_state_from_layers(self, *args):
        for layer_data, layer in zip(self.layers, self.viewer.layers):
            layer.state.visible = layer_data['visible']
            layer.state.color = layer_data['color']

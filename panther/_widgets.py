from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
import panther


class _CanvasWidget(Widget):
    """
    This represents the Canvas, everything is drawn on it
    """
    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down, on_key_up=self._on_keyboard_up)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down, on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_up(self, keyboard, keycode):
        panther.events.trigger("keyup", keyboard, keycode)

        return True

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        panther.events.trigger("keydown", keyboard, keycode, text, modifiers)

        return True  # keep the app open, even if ESC is pressed

    def clear(self):
        with self.canvas:
            self.canvas.clear()

    def tick(self):
        """
        this is called every tick, clear the canvas
        :return: None
        """
        self.clear()

    def draw(self, obj):
        """
        Draw something on the canvas
        :param obj: kivy.graphics.<something> object
        :return: None
        """
        self.canvas.add(obj)

    def draws(self, drawables):
        """
        Draw a lot of things on the canvas
        :param drawables: list<Drawable>
        :return: None
        """
        for item in drawables:
            self.canvas.add(item)

    def ask_to_update(self):
        self.canvas.ask_update()

    def on_touch_down(self, touch):
        panther.events.trigger("touchdown", touch)

    def on_touch_up(self, touch):
        panther.events.trigger("touchup", touch)

    def on_touch_move(self, touch):
        panther.events.trigger("touchdrag", touch)


class _PantherApp(App):
    """
    This is a kivy.App
    it runs in a separate Thread
    """
    def on_stop(self):
        panther.events.execute("quit")

    def on_start(self):
        panther.events.execute("load")

    def build(self):
        self.title = panther.conf.title

        return panther.canvas

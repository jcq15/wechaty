from features.feature_manager import ReflectiveManager
from local_libs.weather_forecaster import WeatherForecaster


class WeatherManager(ReflectiveManager):
    def __init__(self):
        super().__init__()
        self.weather_forecaster = WeatherForecaster()

    def reflective_handle(self, data) -> list:
        args, _ = self.preprocess(data)

        if not args or len(args) < 2:
            return self.make_null_response()
        else:
            if args[0] == '天气':
                city = args[1]
                msg = self.weather_forecaster.get_weather(city)
                return self.reply_text(msg, data, with_mention=True)
            else:
                return self.make_null_response()



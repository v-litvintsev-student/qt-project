import sys

from PyQt5 import uic
from PyQt5.QtCore import QPoint, QRect, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow

from utils import *


class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_PATH, self)

        self.initialize_app()

    def handle_city_field_changed(self):
        self.is_submitted = False

    def initialize_app(self):
        self.favorites_collection = connect_to_db()
        self.favorites = [*self.favorites_collection.find()]

        self.cityField.setText(INITIAL_CITY)
        self.handle_submit()

        self.is_submitted = True
        self.favorites_shift = 0

        self.set_visibility_variables()
        self.set_handlers()
        self.set_favorites()

    def handle_favorites_up(self):
        if (self.favorites_shift):
            self.favorites_shift -= 1

            self.set_favorites()

    def handle_favorites_down(self):
        if (self.favorites_shift < len(self.favorites) - 1):
            self.favorites_shift += 1

            self.set_favorites()

    def set_visibility_variables(self):
        self.hidden_geometry = QRect(QPoint(0, 0), QSize(0, 0))
        self.favoriteItemGeometry0 = self.favoritesItem0.geometry()
        self.favoriteItemGeometry1 = self.favoritesItem1.geometry()
        self.favoriteItemGeometry2 = self.favoritesItem2.geometry()
        self.favoriteItemDeleteGeometry0 = self.favoritesItemDelete0.geometry()
        self.favoriteItemDeleteGeometry1 = self.favoritesItemDelete1.geometry()
        self.favoriteItemDeleteGeometry2 = self.favoritesItemDelete2.geometry()

    def set_favorites(self):
        def handle_favorite_click(value: str):
            self.cityField.setText(value)
            self.handle_submit()

        def handle_favorite_delete_click(value: str):
            self.favorites_collection.find_one_and_delete({'value': value})
            self.favorites = [*self.favorites_collection.find()]

            self.set_favorites()

        visible_favorites = self.favorites[self.favorites_shift:self.favorites_shift + 3]

        if (len(visible_favorites) >= 1):
            self.favoritesItem0.setText(visible_favorites[0]['value'])
            self.favoritesItem0.setGeometry(self.favoriteItemGeometry0)
            self.favoritesItemDelete0.setGeometry(
                self.favoriteItemDeleteGeometry0)

            self.favoritesItem0.disconnect()
            self.favoritesItemDelete0.disconnect()
            self.favoritesItem0.clicked.connect(
                lambda: handle_favorite_click(visible_favorites[0]['value']))
            self.favoritesItemDelete0.clicked.connect(
                lambda: handle_favorite_delete_click(visible_favorites[0]['value']))
        else:
            self.favoritesItem0.setGeometry(self.hidden_geometry)
            self.favoritesItemDelete0.setGeometry(self.hidden_geometry)

        if (len(visible_favorites) >= 2):
            self.favoritesItem1.setText(visible_favorites[1]['value'])
            self.favoritesItem1.setGeometry(self.favoriteItemGeometry1)
            self.favoritesItemDelete1.setGeometry(
                self.favoriteItemDeleteGeometry1)

            self.favoritesItem1.disconnect()
            self.favoritesItemDelete1.disconnect()
            self.favoritesItem1.clicked.connect(
                lambda: handle_favorite_click(visible_favorites[1]['value']))
            self.favoritesItemDelete1.clicked.connect(
                lambda: handle_favorite_delete_click(visible_favorites[1]['value']))
        else:
            self.favoritesItem1.setGeometry(self.hidden_geometry)
            self.favoritesItemDelete1.setGeometry(self.hidden_geometry)

        if (len(visible_favorites) >= 3):
            self.favoritesItem2.setText(visible_favorites[2]['value'])
            self.favoritesItem2.setGeometry(self.favoriteItemGeometry2)
            self.favoritesItemDelete2.setGeometry(
                self.favoriteItemDeleteGeometry2)

            self.favoritesItem2.disconnect()
            self.favoritesItemDelete2.disconnect()
            self.favoritesItem2.clicked.connect(
                lambda: handle_favorite_click(visible_favorites[2]['value']))
            self.favoritesItemDelete2.clicked.connect(
                lambda: handle_favorite_delete_click(visible_favorites[2]['value']))
        else:
            self.favoritesItem2.setGeometry(self.hidden_geometry)
            self.favoritesItemDelete2.setGeometry(self.hidden_geometry)

    def set_handlers(self):
        self.submitButton.clicked.connect(self.handle_submit)
        self.addToFavorites.clicked.connect(self.add_to_favorites)
        self.cityField.textChanged.connect(self.handle_city_field_changed)

        self.favoritesUp.clicked.connect(self.handle_favorites_up)
        self.favoritesDown.clicked.connect(self.handle_favorites_down)

    def add_to_favorites(self):
        if (self.is_submitted):
            item = {'value': self.cityField.text()}
            condidate_item = self.favorites_collection.find_one(item)

            if (not condidate_item):
                self.favorites_collection.insert_one(item)
                self.favorites = [*self.favorites_collection.find()]

                self.set_favorites()

    def set_data(self):
        self.error.setText('')

        current = self.forecast_data['current']
        forecast = self.forecast_data['forecast']['forecastday']

        time = self.forecast_data['location']['localtime'].split()[1]

        self.time.setText(time)

        temperature = f'{current["temp_c"]}°C'
        description = current['condition']['text']
        feelsLike = f'{current["feelslike_c"]}°C'
        pressure = f'{current["pressure_mb"]}mb'
        humidity = f'{current["humidity"]}%'
        cloud = f'{current["cloud"]}'
        wind_speed = f'{current["wind_kph"]}kph'
        precipitation = f'{current["precip_mm"]}mm'
        gusts = f'{current["gust_kph"]}kph'

        self.temperature.setText(temperature)
        self.description.setText(description)
        self.feelsLike.setText(feelsLike)
        self.pressure.setText(pressure)
        self.humidity.setText(humidity)
        self.cloud.setText(cloud)
        self.windSpeed.setText(wind_speed)
        self.precipitation.setText(precipitation)
        self.gusts.setText(gusts)

        forecastDate0 = '.'.join(forecast[0]['date'].split('-')[1:])
        forecastTemperature0 = f'{forecast[0]["day"]["avgtemp_c"]}°C'
        forecastDescription0 = forecast[0]['day']['condition']['text']
        forecastChanceOfRain0 = f'{forecast[0]["day"]["daily_chance_of_rain"]}%'
        forecastChanceOfSnow0 = f'{forecast[0]["day"]["daily_chance_of_snow"]}%'

        self.forecastDate0.setText(forecastDate0)
        self.forecastTemperature0.setText(forecastTemperature0)
        self.forecastDescription0.setText(forecastDescription0)
        self.forecastChanceOfRain0.setText(forecastChanceOfRain0)
        self.forecastChanceOfSnow0.setText(forecastChanceOfSnow0)

        forecastDate1 = '.'.join(forecast[1]['date'].split('-')[1:])
        forecastTemperature1 = f'{forecast[1]["day"]["avgtemp_c"]}°C'
        forecastDescription1 = forecast[1]["day"]["condition"]["text"]
        forecastChanceOfRain1 = f'{forecast[1]["day"]["daily_chance_of_rain"]}%'
        forecastChanceOfSnow1 = f'{forecast[1]["day"]["daily_chance_of_snow"]}%'

        self.forecastDate1.setText(forecastDate1)
        self.forecastTemperature1.setText(forecastTemperature1)
        self.forecastDescription1.setText(forecastDescription1)
        self.forecastChanceOfRain1.setText(forecastChanceOfRain1)
        self.forecastChanceOfSnow1.setText(forecastChanceOfSnow1)

        forecastDate2 = '.'.join(forecast[2]['date'].split('-')[1:])
        forecastTemperature2 = f'{forecast[2]["day"]["avgtemp_c"]}°C'
        forecastDescription2 = forecast[2]["day"]["condition"]["text"]
        forecastChanceOfRain2 = f'{forecast[2]["day"]["daily_chance_of_rain"]}%'
        forecastChanceOfSnow2 = f'{forecast[2]["day"]["daily_chance_of_snow"]}%'

        self.forecastDate2.setText(forecastDate2)
        self.forecastTemperature2.setText(forecastTemperature2)
        self.forecastDescription2.setText(forecastDescription2)
        self.forecastChanceOfRain2.setText(forecastChanceOfRain2)
        self.forecastChanceOfSnow2.setText(forecastChanceOfSnow2)

    def handle_submit(self):
        city_name = self.cityField.text()

        self.forecast_data = fetch_forecast_data(city_name)

        if (self.forecast_data == ERROR_MESSAGE):
            return self.error.setText(ERROR_MESSAGE)

        self.set_data()
        self.is_submitted = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_widget = MainWidget()
    main_widget.show()

    app_execution = app.exec_()
    sys.exit(app_execution)

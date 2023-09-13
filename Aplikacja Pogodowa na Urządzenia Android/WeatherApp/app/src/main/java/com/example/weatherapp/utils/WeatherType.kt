package com.example.weatherapp.utils

import androidx.annotation.DrawableRes
import com.example.weatherapp.R

// Klasa abstrakcyjna opisująca różne typy pogody
sealed class WeatherType (
    val weatherType: String,
    @DrawableRes val iconRes: Int
) {
    object ClearSky : WeatherType(
        weatherType = "Słonecznie",
        iconRes = R.drawable.clear_sky
    )
    object PartlyCloudly : WeatherType(
        weatherType = "Pochmurnie",
        iconRes = R.drawable.partly_cloud
    )
    object Foggy : WeatherType(
        weatherType = "Mgła",
        iconRes = R.drawable.fog
    )
    object Drizzle : WeatherType(
        weatherType = "Mrzawka",
        iconRes = R.drawable.drizzle
    )
    object Rain : WeatherType(
        weatherType = "Deszcz",
        iconRes = R.drawable.rain
    )
    object Thunderstorm : WeatherType(
        weatherType = "Burza",
        iconRes = R.drawable.thunderstorm
    )
    object Snow : WeatherType(
        weatherType = "Śnieg",
        iconRes = R.drawable.snow
    )

    companion object {
        // Funkcja mapująca kody pogodowe na odpowiedni typ pogody
        fun weatherInterpretationCodes(code: Int) : WeatherType {
            return when(code) {
                0 -> ClearSky
                1, 2, 3 -> PartlyCloudly
                45, 48 -> Foggy
                51, 53, 55, 56, 57 -> Drizzle
                61, 63, 65, 66, 67, 80, 81, 82 -> Rain
                71, 73, 75, 77, 85, 86 -> Snow
                95, 96, 99 -> Thunderstorm
                else -> ClearSky // Domyślny typ pogody w przypadku braku dopasowania
            }
        }
    }
}

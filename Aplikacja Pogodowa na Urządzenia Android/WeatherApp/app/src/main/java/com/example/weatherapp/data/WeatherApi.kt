package com.example.weatherapp.data

import com.example.weatherapp.models.WeatherData
import retrofit2.http.GET
import retrofit2.Response

interface WeatherApi {
    // Endpoint do pobierania bieżącej pogody
    @GET("v1/forecast?latitude=52.4069&longitude=16.9299&daily=weathercode,temperature_2m_max,uv_index_max,precipitation_probability_max,windspeed_10m_max&timezone=Europe%2FBerlin")
    suspend fun getWeather(): Response<WeatherData>

    // Endpoint do pobierania prognozy pogody na kolejne dni
    @GET("v1/forecast?latitude=52.4069&longitude=16.9299&daily=weathercode,temperature_2m_max,uv_index_max,precipitation_probability_max,windspeed_10m_max&timezone=Europe%2FBerlin")
    suspend fun getWeatherNextDays(): Response<WeatherData>
}

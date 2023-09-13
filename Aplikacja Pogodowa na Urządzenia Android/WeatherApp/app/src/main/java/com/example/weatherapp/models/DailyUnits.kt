package com.example.weatherapp.models

data class DailyUnits(
    val precipitation_probability_max: String,
    val temperature_2m_max: String,
    val time: String,
    val uv_index_max: String,
    val weathercode: String,
    val windspeed_10m_max: String
)

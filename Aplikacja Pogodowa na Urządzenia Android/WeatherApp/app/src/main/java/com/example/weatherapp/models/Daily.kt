package com.example.weatherapp.models

// grupowanie parametrów pogodowych w jednym obiekcie
data class Daily(
//    prawd. opadów
    val precipitation_probability_max: List<Int>,
    val temperature_2m_max: List<Double>,
    val time: List<String>,
    val uv_index_max: List<Double>,
//    kody pogodowe
    val weathercode: List<Int>,
    val windspeed_10m_max: List<Double>
)

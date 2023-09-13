package com.example.weatherapp.data

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object RetrofitInstance {
    // Inicjalizacja instancji Retrofit, która umożliwia komunikację z API
    val api: WeatherApi by lazy {
        Retrofit.Builder()
            .baseUrl("https://api.open-meteo.com/") // Adres bazowy API
            .addConverterFactory(GsonConverterFactory.create()) // Konwerter do obsługi formatu JSON
            .build()
            .create(WeatherApi::class.java) // Tworzenie interfejsu API do wykonywania żądań
    }
}

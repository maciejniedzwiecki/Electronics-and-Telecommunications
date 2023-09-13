package com.example.weatherapp.fragments

import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.ProgressBar
import android.widget.TextView
import androidx.core.view.isVisible
import com.example.weatherapp.R
import com.example.weatherapp.data.RetrofitInstance
import retrofit2.HttpException

import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import com.example.weatherapp.TAG
import com.example.weatherapp.utils.WeatherType
import java.io.IOException

class HomeFragment : Fragment(R.layout.fragment_home) {

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Tworzenie widoku fragmentu
        val view = inflater.inflate(R.layout.fragment_home, container, false)

        // Inicjalizacja elementów interfejsu
        val textViewDate = view.findViewById<TextView>(R.id.textViewDate)
        val imageViewWeather = view.findViewById<ImageView>(R.id.imageViewWeather)
        val textViewWeatherDesc = view.findViewById<TextView>(R.id.textViewWeatherDesc)
        val textViewWeatherTemp = view.findViewById<TextView>(R.id.textViewWeatherTemp)
        val textViewRainProbability = view.findViewById<TextView>(R.id.textViewRainProbability)
        val textViewUvIndex = view.findViewById<TextView>(R.id.textViewUvIndex)
        val textViewWindSpeed = view.findViewById<TextView>(R.id.textViewWindSpeed)

        val progressBar = view.findViewById<ProgressBar>(R.id.progressBarHome)

        // Rozpoczęcie operacji w tle (coroutines)
        lifecycleScope.launchWhenCreated {
            progressBar.isVisible = true
            try {
                // Wywołanie żądania API
                val response = RetrofitInstance.api.getWeather()
                if (response.isSuccessful && response.body() != null) {
                    // Przetworzenie i wyświetlenie danych o pogodzie
                    val weatherData = response.body()!!
                    textViewDate.text = weatherData.daily.time[0]
                    imageViewWeather.setImageResource(WeatherType.weatherInterpretationCodes(weatherData.daily.weathercode[0]).iconRes)
                    textViewWeatherDesc.text = WeatherType.weatherInterpretationCodes(weatherData.daily.weathercode[0]).weatherType
                    textViewWeatherTemp.text = weatherData.daily.temperature_2m_max[0].toString()
                    textViewRainProbability.text = weatherData.daily.precipitation_probability_max[0].toString()
                    textViewUvIndex.text = weatherData.daily.uv_index_max[0].toString()
                    textViewWindSpeed.text = weatherData.daily.windspeed_10m_max[0].toString()
                } else {
                    // Obsługa błędu odpowiedzi HTTP
                    Log.e(TAG, "Response error: ${response.code()}")
                }

                progressBar.isVisible = false

            } catch (e: IOException) {
                // Obsługa braku połączenia z internetem
                Log.e(TAG, "Brak połączenia z internetem: ${e.message}")
                progressBar.isVisible = false
            } catch (e: HttpException) {
                // Obsługa błędu HTTP
                Log.e(TAG, "HttpException error: ${e.message}")
                progressBar.isVisible = false
            } catch (e: Exception) {
                // Obsługa niespodziewanego błędu
                Log.e(TAG, "Niespodziewany error: ${e.message}")
                progressBar.isVisible = false
            }
        }

        return view
    }
}

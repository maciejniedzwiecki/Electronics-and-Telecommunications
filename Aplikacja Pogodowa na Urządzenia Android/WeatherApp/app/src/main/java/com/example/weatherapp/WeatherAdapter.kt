package com.example.weatherapp

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.AsyncListDiffer
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.RecyclerView
import com.example.weatherapp.databinding.ItemCalendarBinding
import com.example.weatherapp.models.WeatherData
import com.example.weatherapp.utils.WeatherType

class WeatherAdapter : RecyclerView.Adapter<WeatherAdapter.WeatherViewHolder>() {

    // Klasa reprezentująca pojedynczy element listy
    inner class WeatherViewHolder(val binding: ItemCalendarBinding) :
        RecyclerView.ViewHolder(binding.root)

    // Klasa do porównywania elementów na liście
    private val diffCallback = object : DiffUtil.ItemCallback<WeatherData>() {
        override fun areContentsTheSame(
            oldItem: WeatherData,
            newItem: WeatherData
        ): Boolean {
            return oldItem == newItem
        }

        override fun areItemsTheSame(
            oldItem: WeatherData,
            newItem: WeatherData
        ): Boolean {
            return oldItem == newItem
        }
    }

    // Inicjalizacja - zarządzanie różnicami w danych
    private val differ = AsyncListDiffer(
        this,
        diffCallback
    )

    // Ustawianie i pobieranie danych o pogodzie
    var weatherNextDays: List<WeatherData>
        get() = differ.currentList
        set(value) {
            differ.submitList(value)
        }

    // Tworzenie nowego WeatherViewHolder
    override fun onCreateViewHolder(
        parent: ViewGroup,
        viewType: Int
    ): WeatherViewHolder {
        return WeatherViewHolder(
            ItemCalendarBinding.inflate(
                LayoutInflater.from(parent.context),
                parent,
                false
            )
        )
    }

    // Pobieranie liczby elementów na liście
    override fun getItemCount() = weatherNextDays.size

    // Wypełnianie danych w pojedynczym elemencie listy
    override fun onBindViewHolder(
        holder: WeatherViewHolder,
        position: Int
    ) {
        // Pobieranie informacji o pogodzie i przypisywanie ich do widoków
        holder.binding.apply {
            val weather = weatherNextDays[position]
            itemCalendarImage.setImageResource(
                WeatherType.weatherInterpretationCodes(weather.daily.weathercode[position]).iconRes
            )
            itemCalendarDescription.text =
                WeatherType.weatherInterpretationCodes(weather.daily.weathercode[position]).weatherType
            itemCalendarWeatherTemp.text = weather.daily.temperature_2m_max[position].toString()
            itemCalendarDate.text = weather.daily.time[position]
            itemCalendarRainProbability.text =
                weather.daily.precipitation_probability_max[position].toString()
            itemCalendarUvIndex.text = weather.daily.uv_index_max[position].toString()
            itemCalendarWindSpeed.text = weather.daily.windspeed_10m_max[position].toString()
        }
    }
}

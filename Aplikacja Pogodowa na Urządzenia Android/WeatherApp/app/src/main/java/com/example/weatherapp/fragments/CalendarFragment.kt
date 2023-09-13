package com.example.weatherapp.fragments

import android.app.DatePickerDialog
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.weatherapp.R
import com.example.weatherapp.WeatherAdapter
import com.example.weatherapp.data.RetrofitInstance
import com.example.weatherapp.databinding.FragmentCalendarBinding
import com.example.weatherapp.models.WeatherData
import retrofit2.HttpException

import androidx.core.view.isVisible
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import com.example.weatherapp.TAG
import kotlinx.coroutines.launch
import java.io.IOException
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Locale

class CalendarFragment : Fragment(R.layout.fragment_calendar) {

    // Inicjalizacja zmiennych
    private lateinit var binding: FragmentCalendarBinding
    private lateinit var date: String
    private lateinit var minDateFromApi: String
    private lateinit var maxDateFromApi: String
    private lateinit var weatherAdapter: WeatherAdapter

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inicjalizacja widoku za pomocą bindingu
        binding = FragmentCalendarBinding.inflate(layoutInflater)

        // Inicjalizacja RecyclerView, przycisku kalendarza i pobranie danych pogodowych
        setupRecyclerView()
        setupCalendarButton()
        fetchWeatherData()

        return binding.root
    }

    private fun setupRecyclerView() {
        // Konfiguracja RecyclerView
        binding.recyclerViewDays.apply {
            weatherAdapter = WeatherAdapter()
            adapter = weatherAdapter
            layoutManager = LinearLayoutManager(requireContext())
        }
    }

    private fun setupCalendarButton() {
        // Obsługa przycisku kalendarza
        val showCalendarButton = binding.showCalendarButton
        showCalendarButton.setOnClickListener {
            showCalendarDialog()
        }
    }

    private fun showCalendarDialog() {
        // Wyświetlenie kalendarza i wybór daty
        val calendar = Calendar.getInstance()
        val datePickerDialog = DatePickerDialog(requireContext(), { _, year, month, day ->
            val selectedDate = Calendar.getInstance()
            selectedDate.set(year, month, day)
            val dateFormat = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())
            date = dateFormat.format(selectedDate.time)
            fetchWeatherData()
        },
            calendar.get(Calendar.YEAR),
            calendar.get(Calendar.MONTH),
            calendar.get(Calendar.DAY_OF_MONTH))

        val minDateCalendar = Calendar.getInstance()
        val maxDateCalendar = Calendar.getInstance()

        // Rozbicie dat z API na rok, miesiąc i dzień i ustawienie ich w kalendarzach
        val minDateSplit = minDateFromApi.split("-")
        val maxDateSplit = maxDateFromApi.split("-")

        minDateCalendar.set(minDateSplit[0].toInt(), (minDateSplit[1].toInt()) - 1, minDateSplit[2].toInt())
        maxDateCalendar.set(maxDateSplit[0].toInt(), (maxDateSplit[1].toInt()) - 1, maxDateSplit[2].toInt())

        // Ustawienie minimalnej i maksymalnej daty w datePickerDialog
        datePickerDialog.datePicker.minDate = minDateCalendar.timeInMillis
        datePickerDialog.datePicker.maxDate = maxDateCalendar.timeInMillis

        datePickerDialog.show()
    }

    private fun fetchWeatherData() {
        lifecycleScope.launch() {
            // Wyświetlenie paska postępu
            binding.progressBar.isVisible = true

            try {
                val response = RetrofitInstance.api.getWeatherNextDays()

                if (response.isSuccessful && response.body() != null) {
                    // Pobranie danych pogodowych z API
                    val weatherData = response.body()!!
                    minDateFromApi = weatherData.daily.time[0]
                    maxDateFromApi = weatherData.daily.time[6]

                    val listOfDays = mutableListOf<WeatherData>()
                    val dateFormat = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())
                    val currentDate = dateFormat.parse(minDateFromApi)!!
                    val selectedDate = dateFormat.parse(date)!!

                    // Pobranie danych pogodowych na kolejne dni do wybranej daty
                    while (currentDate <= selectedDate) {
                        listOfDays.add(weatherData)
                        val calendar = Calendar.getInstance()
                        calendar.time = currentDate
                        calendar.add(Calendar.DAY_OF_MONTH, 1)
                        currentDate.time = calendar.timeInMillis
                    }
                    weatherAdapter.weatherNextDays = listOfDays

                } else {
                    // Obsługa błędu odpowiedzi HTTP
                    Log.e(TAG, "Response error: ${response.code()}")
                }

                // Ukrycie paska postępu po zakończeniu pobierania danych
                binding.progressBar.isVisible = false

            } catch (e: IOException) {
                // Ukrycie paska postępu - błąd połączenia
                Log.e(TAG, "Brak połączenia z internetem: ${e.message}")
                binding.progressBar.isVisible = false
            } catch (e: HttpException) {
                // Ukrycie paska postępu - błąd HTTP
                Log.e(TAG, "HttpException error: ${e.message}")
                binding.progressBar.isVisible = false
            } catch (e: Exception) {
                // Ukrycie paska postępu - niespodziewany błąd
                Log.e(TAG, "Niespodziewany error: ${e.message}")
                binding.progressBar.isVisible = false
            }

        }
    }
}

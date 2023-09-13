package com.example.weatherapp

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import androidx.fragment.app.Fragment
import com.example.weatherapp.databinding.ActivityMainBinding
import com.example.weatherapp.fragments.CalendarFragment
import com.example.weatherapp.fragments.HomeFragment

// Stała do identyfikowania logów
const val TAG = "MainActivity"

class MainActivity : AppCompatActivity() {
    private lateinit var binding : ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Inicjalizacja i użycie bindingu do tworzenia widoku
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // Zamiana fragmentu podczas tworzenia aktywności
        replaceFragment(HomeFragment())

        // Obsługa wyboru elementu menu nawigacyjnego
        binding.bottomNavigationView.setOnItemSelectedListener {
            when(it.itemId){
                R.id.home -> replaceFragment(HomeFragment())
                R.id.calendar -> replaceFragment(CalendarFragment())
                else -> {

                }
            }
            true
        }
    }

    private fun replaceFragment(fragment : Fragment){
        val fragmentManager = supportFragmentManager
        val fragmentTransaction = fragmentManager.beginTransaction()

        // Zamiana fragmentu w kontenerze
        fragmentTransaction.replace(R.id.frame_layout, fragment)
        fragmentTransaction.commit()
    }
}

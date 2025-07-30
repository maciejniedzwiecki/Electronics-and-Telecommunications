import numpy as np
from matplotlib import pyplot as plt
import setup
import framegen
import modulation
import demodulation
import coder
import channel
import decoder

import tkinter as tk
import customtkinter

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#############################################################################################################################
# MAIN PROGRAM

def switch_case(button_id):

    # Perform code based on checkbox values
    if button_id == 1:
        errors = 0  # error counter
        iteration = 0  # iteration counter
        # array for modulated signal samples (to plot them)
        samples = np.zeros((setup.frame + 2,), dtype=np.complex128)

        while True:
            if (errors >= setup.error_limit) or (iteration >= setup.iter_limit):  # check end conditions
                print("Passed limit")
                print("Iterations: " + str(iteration))
                print("Errors: " + str(errors))
                if setup.plot_toggle:  # plot the last frame                    
                    
                    # Create a matplotlib figure
                    fig = Figure(figsize=(5, 4), dpi=120)

                    # Add the first subplot to the figure
                    plot1 = fig.add_subplot(1, 1, 1)
                    plot1.scatter(samples.real, samples.imag)
                    plot1.set_title("8-PSK Constellation (last frame)")
                    plot1.set_xlabel("Im")
                    plot1.set_ylabel("Re")
                    plot1.grid(True)

                    # Create a tkinter canvas and associate it with the figure
                    canvas = FigureCanvasTkAgg(fig, master=window)
                    canvas.draw()
                    canvas.get_tk_widget().grid(row=1, column=3, rowspan=12, padx=20)
                break

            frame = framegen.generate_frame()  # generate random frame
            # encode the frame using a [5, 7] conv. encoder
            frame_encoded = coder.encode_frame(frame)
            # array for distances of observations from constellation points
            soft_decisions = np.zeros((frame_encoded.size, 8))

            # if setup.gray_toggle: # gray coding
            #     for i in range(frame_encoded.size):
            #         samples[i] = modulation.modulate_8psk_gray(frame_encoded[i]) + channel.noise() # modulate the codeword and add noise
            #         soft_decisions[i] = demodulation.demodulate_8psk(samples[i]) # store distances from const. points
            #     frame_decoded = decoder.viterbi_gray(soft_decisions) # decode using viterbi
            # else: # no gray coding
            #     for i in range(frame_encoded.size):
            #         samples[i] = modulation.modulate_8psk(frame_encoded[i]) + channel.noise() # modulate the codeword and add noise
            #         soft_decisions[i] = demodulation.demodulate_8psk(samples[i]) # store distances from const. points
            #     frame_decoded = decoder.viterbi(soft_decisions) # decode using viterbi

            if setup.gray_toggle:  # gray coding
                samples = channel.noise(
                    modulation.modulate_8psk_gray(frame_encoded))
                soft_decisions = demodulation.demodulate_8psk(samples)
                frame_decoded = decoder.viterbi_gray(soft_decisions)
            else:
                samples = channel.noise(
                    modulation.modulate_8psk(frame_encoded))
                soft_decisions = demodulation.demodulate_8psk(samples)
                frame_decoded = decoder.viterbi(soft_decisions)

            for i in range(setup.frame):  # check decoded frame for errors
                if frame[i] != frame_decoded[i]:
                    errors += 1

            if setup.data_toggle:  # display some debug data
                print("Encoded: " + str(frame_encoded))
                print("Raw    : " + str(frame))
                print("Decoded: " + str(frame_decoded))
                print("Errors: " + str(errors))

            iteration += 1

    elif button_id == 2:
        snrdb = range(0, setup.snrdb_range)
        ber = np.zeros((setup.snrdb_range,))
        bits_per_frame = setup.frame * 2  # because every symbol has 2 bits
        for j in range(setup.snrdb_range):
            errors = 0  # error counter
            iteration = 0  # iteration counter
            # array for modulated signal samples (to plot them)
            samples = np.zeros((setup.frame + 2,), dtype=np.complex128)

            while True:
                if (iteration >= setup.iter_limit_ber):  # check end conditions
                    print("Passed limit")
                    print("Iterations: " + str(iteration))
                    print("Errors: " + str(errors))
                    ber[j] = errors/(bits_per_frame*iteration)
                    break

                frame = framegen.generate_frame()  # generate random frame
                # encode the frame using a [5, 7] conv. encoder
                frame_encoded = coder.encode_frame(frame)
                # array for distances of observations from constellation points
                soft_decisions = np.zeros((frame_encoded.size, 8))

                if setup.gray_toggle:  # gray coding
                    samples = channel.noise(
                        modulation.modulate_8psk_gray(frame_encoded), float(j))
                    soft_decisions = demodulation.demodulate_8psk(samples)
                    frame_decoded = decoder.viterbi_gray(soft_decisions)
                else:
                    samples = channel.noise(
                        modulation.modulate_8psk(frame_encoded), float(j))
                    soft_decisions = demodulation.demodulate_8psk(samples)
                    frame_decoded = decoder.viterbi(soft_decisions)

                for i in range(setup.frame):  # check decoded frame for errors
                    if frame[i] != frame_decoded[i]:
                        errors += 1

                if setup.data_toggle:  # display some debug data
                    print("Encoded: " + str(frame_encoded))
                    print("Raw    : " + str(frame))
                    print("Decoded: " + str(frame_decoded))
                    print("Errors: " + str(errors))

                iteration += 1
        

        # Create a matplotlib figure
        fig = Figure(figsize=(5, 4), dpi=120)

        # Add the second subplot to the figure
        plot2 = fig.add_subplot(1, 1, 1)
        plot2.plot(snrdb, ber, 'o-', label='practical')
        plot2.set_title("8-PSK Modulation BER vs SNR")
        plot2.set_xlabel('SNR [dB]')
        plot2.set_ylabel('BER')
        plot2.set_yscale("log")
        plot2.grid(True)

        # Create a tkinter canvas and associate it with the figure
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=3, rowspan=12, padx=20)
        
    
    
#############################################################################################################################
# Window and titles styles

# Create the Tkinter window
window = customtkinter.CTk()

# Size of the window using the geometry method
window.geometry("980x550")  # width x height
# window.attributes("-fullscreen", True)


customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")


customtkinter.CTkLabel(window, text="TCM Simulation", font=("Arial", 25), justify="center").grid(row=0, column=0, pady=15, columnspan=3)


#############################################################################################################################
# Sliders


# Real time preview value
def update_preview_labels(event):
    value_slider_power = slider_power.get()
    preview_slider_power.configure(text=f"{int(value_slider_power)}")

    value_slider_frame = slider_frame.get()
    preview_slider_frame.configure(text=f"{int(value_slider_frame)}")

    value_slider_iter_limit = slider_iter_limit.get()
    preview_slider_iter_limit.configure(text=f"{int(value_slider_iter_limit)}")

    value_slider_iter_limit_ber = slider_iter_limit_ber.get()
    preview_iter_limit_ber.configure(text=f"{int(value_slider_iter_limit_ber)}")

    value_slider_snrdb_range = slider_snrdb_range.get()
    preview_snrdb_range.configure(text=f"{int(value_slider_snrdb_range)}")

    value_slider_error_limit = slider_error_limit.get()
    preview_error_limit.configure(text=f"{int(value_slider_error_limit)}")

    value_slider_snr = slider_snr.get()
    preview_slider_snr.configure(text=f"{int(value_slider_snr)}")
    


# Create DoubleVars to store slider values
slider_value_power = customtkinter.IntVar(value=setup.power)
slider_value_frame = customtkinter.IntVar(value=setup.frame)
slider_value_iter_limit = customtkinter.IntVar(value=setup.iter_limit)
slider_value_iter_limit_ber = customtkinter.IntVar(value=setup.iter_limit_ber)
slider_value_snrdb_range = customtkinter.IntVar(value=setup.snrdb_range)
slider_value_error_limit = customtkinter.IntVar(value=setup.error_limit)
slider_value_snr = customtkinter.DoubleVar(value=setup.snr)

# Text informed about options
customtkinter.CTkLabel(window, text="Change the value of:", font=("Arial", 15), justify="center").grid(row=1, column=0, pady=10, columnspan=3)

# Create sliders
customtkinter.CTkLabel(window, text="Transmission power:", font=("Arial", 10), justify="center").grid(row=2, column=0, padx=20)
slider_power = customtkinter.CTkSlider(window, from_=0, to=10, variable=slider_value_power)
slider_power.grid(row=2, column=1)

preview_slider_power = customtkinter.CTkLabel(window, text= setup.power)
preview_slider_power.grid(row=2, column= 2)
slider_power.bind("<ButtonRelease-1>", update_preview_labels)


customtkinter.CTkLabel(window, text="Frame size:", font=("Arial", 10), justify="center").grid(row=3, column=0, padx=20)
slider_frame = customtkinter.CTkSlider(window, from_=1, to=256, variable=slider_value_frame)
slider_frame.grid(row=3, column=1)

preview_slider_frame = customtkinter.CTkLabel(window, text=setup.frame)
preview_slider_frame.grid(row=3, column= 2)
slider_frame.bind("<ButtonRelease-1>", update_preview_labels)



customtkinter.CTkLabel(window, text="Iteration limit:", font=("Arial", 10), justify="center").grid(row=4, column=0, padx=20)
slider_iter_limit = customtkinter.CTkSlider(window, from_=10, to=1000, variable=slider_value_iter_limit)
slider_iter_limit.grid(row=4, column=1)

preview_slider_iter_limit = customtkinter.CTkLabel(window, text=setup.iter_limit)
preview_slider_iter_limit.grid(row=4, column= 2)
slider_iter_limit.bind("<ButtonRelease-1>", update_preview_labels)



customtkinter.CTkLabel(window, text="Iteration limit (BER vs SNR):", font=("Arial", 10), justify="center").grid(row=5, column=0, padx=20)
slider_iter_limit_ber = customtkinter.CTkSlider(window, from_=10, to=500, variable=slider_value_iter_limit_ber)
slider_iter_limit_ber.grid(row=5, column=1)

preview_iter_limit_ber = customtkinter.CTkLabel(window, text=setup.iter_limit_ber)
preview_iter_limit_ber.grid(row=5, column= 2)
slider_iter_limit_ber.bind("<ButtonRelease-1>", update_preview_labels)



customtkinter.CTkLabel(window, text="SNR range (BER vs SNR):", font=("Arial", 10), justify="center").grid(row=6, column=0, padx=20)
slider_snrdb_range = customtkinter.CTkSlider(window, from_=0, to=20, variable=slider_value_snrdb_range)
slider_snrdb_range.grid(row=6, column=1)

preview_snrdb_range = customtkinter.CTkLabel(window, text=setup.snrdb_range)
preview_snrdb_range.grid(row=6, column= 2)
slider_snrdb_range.bind("<ButtonRelease-1>", update_preview_labels)



customtkinter.CTkLabel(window, text="Error limit:", font=("Arial", 10), justify="center").grid(row=7, column=0, padx=20)
slider_error_limit = customtkinter.CTkSlider(window, from_=1, to=100, variable=slider_value_error_limit)
slider_error_limit.grid(row=7, column=1)

preview_error_limit = customtkinter.CTkLabel(window, text=setup.error_limit)
preview_error_limit.grid(row=7, column= 2)
slider_error_limit.bind("<ButtonRelease-1>", update_preview_labels)



customtkinter.CTkLabel(window, text="SNR:", font=("Arial", 10)).grid(row=8, column=0, padx=20)
slider_snr = customtkinter.CTkSlider(window, from_=0, to=40, number_of_steps=80, variable=slider_value_snr)
slider_snr.grid(row=8, column=1)

preview_slider_snr = customtkinter.CTkLabel(window, text=setup.snr)
preview_slider_snr.grid(row=8, column= 2)
slider_snr.bind("<ButtonRelease-1>", update_preview_labels)



# Sliders as variables
def retrieve_slider_values():
    setup.power = slider_value_power.get()
    setup.frame = slider_value_frame.get()
    setup.iter_limit = slider_value_iter_limit.get()
    setup.iter_limit_ber = slider_value_iter_limit_ber.get()
    setup.snrdb_range = slider_value_snrdb_range.get()
    setup.error_limit = slider_value_error_limit.get()
    setup.snr = slider_value_snr.get()
    setup.gray_toggle = checkbox_var_gray.get()


# Create the first checkbox and associate the callback function
checkbox_var_gray = tk.BooleanVar()
checkbox_gray = customtkinter.CTkCheckBox(window, text='Gray', variable=checkbox_var_gray)
checkbox_gray.grid(row=9, column=0, pady=10, sticky="e")

# Create a button to store varaibles
button_variables = customtkinter.CTkButton(window, text="Set Values", command=retrieve_slider_values)
button_variables.grid(row=9, column=1, pady=10, columnspan=2)



#############################################################################################################################
# Simultaion choice

# Text informed about options
customtkinter.CTkLabel(window, text="Choose an option:", font=("Arial", 15), justify="center").grid(row=10, column=0, pady=10, columnspan=2)

# Create the first buttons
button1 = customtkinter.CTkButton(window, text="Simulate 8-PSK", command=lambda: switch_case(1))
button1.grid(row=11, column=0, padx=20, pady=10, columnspan=3)

button2 = customtkinter.CTkButton(window, text="BER vs SNR", command=lambda: switch_case(2))
button2.grid(row=12, column=0, padx=20, pady=10, columnspan=3)


# Start the Tkinter event loop
window.mainloop()
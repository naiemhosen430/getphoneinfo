import tkinter as tk
from tkinter import messagebox
import usb.core as ub  # Import usb.core as ub
import usb.util  # Import usb.util

import webbrowser

def get_device_info():
    try:
        # Find all USB devices
        devices = ub.find(find_all=True)

        # If no devices are found, show error message
        if not devices:
            messagebox.showerror("Error", "No USB devices found.")
            return None

        # Read device information for the first device found
        device = devices[0]
        manufacturer = usb.util.get_string(device, device.iManufacturer)  # Use ub.util.get_string()
        product = usb.util.get_string(device, device.iProduct)  # Use ub.util.get_string()
        serial = usb.util.get_string(device, device.iSerialNumber)  # Use ub.util.get_string()

        # Display device information
        info_label.config(text=f"Manufacturer: {manufacturer}\nProduct: {product}\nSerial: {serial}")
        goto_website_button.config(state=tk.NORMAL)

        return device
    except ub.NoBackendError as e:  # Catch NoBackendError
        messagebox.showerror("USB Error", str(e))
        return None

def handle_device_access():
    # Request permission to access device
    permission = messagebox.askyesno("Permission Required", "Do you grant permission to access your device?")
    if permission:
        device = get_device_info()
        if device is not None:
            goto_website_button.config(state=tk.NORMAL)
    else:
        messagebox.showinfo("Permission Denied", "Access to device denied.")

def goto_website():
    # Get device information
    device = get_device_info()
    if device is not None:
        # Open a website with device information embedded in the URL
        manufacturer = usb.util.get_string(device, device.iManufacturer)  # Use ub.util.get_string()
        product = usb.util.get_string(device, device.iProduct)  # Use ub.util.get_string()
        serial = usb.util.get_string(device, device.iSerialNumber)  # Use ub.util.get_string()

        url = f"https://applehealing.vercel.app/dashboard/addrecord/?manufacturer={manufacturer}&product={product}&serial={serial}"
        webbrowser.open_new(url)

def request_permission():
    handle_device_access()

# Create main window
root = tk.Tk()
root.title("Device Info App")

# Create widgets
info_label = tk.Label(root, text="Device information will be displayed here.")
get_info_button = tk.Button(root, text="Get Device Info", command=request_permission)
goto_website_button = tk.Button(root, text="Go to Website", command=goto_website, state=tk.DISABLED)

# Place widgets in the window
info_label.pack(pady=10)
get_info_button.pack(pady=5)
goto_website_button.pack(pady=5)

# Run the application
root.mainloop()

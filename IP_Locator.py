import requests
import folium
import webbrowser
from colorama import Fore, init

init(autoreset=True)


def get_ip_info(ip):
    url = f"https://ipinfo.io/{ip}/json"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            print(Fore.RED + f"Error: Unable to fetch data (Status code {response.status_code})")
            return None
        return response.json()
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Network error: {e}")
        return None


def display_info(data):
    print(Fore.CYAN + "\n=== IP Information ===\n")
    for key in ["ip", "city", "region", "country", "loc", "org"]:
        print(Fore.YELLOW + f"{key.capitalize():<10}: " + Fore.GREEN + f"{data.get(key, 'N/A')}")
    print("\n")


def create_map(location_string):
    try:
        lat, lon = map(float, location_string.split(","))
        ip_map = folium.Map(location=[lat, lon], zoom_start=10)
        folium.Marker([lat, lon], popup="IP Location", tooltip="Click me").add_to(ip_map)

        filename = "ip_location_map.html"
        ip_map.save(filename)

        webbrowser.open(filename)
        print(Fore.GREEN + "Map successfully generated and opened in your browser.")
    except:
        print(Fore.RED + "Could not generate map (invalid coordinates).")


def main():
    ip = input(Fore.CYAN + "Enter IP Address: ").strip()

    # ساده‌ترین چک فرمت IP
    if not ip or len(ip.split('.')) != 4:
        print(Fore.RED + "Invalid IP format. Example: 8.8.8.8")
        return

    data = get_ip_info(ip)
    if data:
        display_info(data)

        loc = data.get("loc")
        if loc:
            print(Fore.CYAN + "Generating map...")
            create_map(loc)
        else:
            print(Fore.RED + "Location data not available for this IP.")


if __name__ == "__main__":
    main()

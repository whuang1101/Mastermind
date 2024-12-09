import requests

def get_random_numbers(number_of_ints, min_guess,max_guess):

    """
    Can change the number of ints desired, the minimum number and the max_guess. If max guess over 10 need to refactor boundaries.
    """
    url = f'https://www.random.org/integers/?num={number_of_ints}&min={min_guess}&max={max_guess}&col=1&base=10&format=plain&rnd=new'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        new_numbers = list(map(int, response.text.split()))
        print(f"Generated Numbers: {new_numbers}")
        return new_numbers
    else:
        print(f"Error: Unable to fetch data. Response content: {response.text}")
        return None
import requests
def getRandomNumbers(number):
    url = f'https://www.random.org/integers/?num={number}&min=0&max=7&col=1&base=10&format=plain&rnd=new'
    response = requests.get(url)
    if response.status_code == 200:
        new_numbers = list(map(int, response.text.split()))
        return new_numbers
    else:
        return None

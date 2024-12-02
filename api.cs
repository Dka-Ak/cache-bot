using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;

namespace API
{
    public class Country
    {
        public string Name { get; set; }
        public string Capital { get; set; }
        public long Population { get; set; }
        public double Area { get; set; }
        public string Currency { get; set; }
    }

    public class Program
    {
        private static readonly HttpClient client = new HttpClient();

        public static async Task Main(string[] args)
        {
            string url = "https://restcountries.com/v3.1/all";
            List<Country> countries = await FetchCountriesAsync(url);
            
            foreach (var country in countries)
            {
                Console.WriteLine($"Name: {country.Name}, Capital: {country.Capital}, Population: {country.Population}, Area: {country.Area}, Currency: {country.Currency}");
            }
        }

        private static async Task<List<Country>> FetchCountriesAsync(string url)
        {
            List<Country> countries = new List<Country>();
            HttpResponseMessage response = await client.GetAsync(url);
            
            if (response.IsSuccessStatusCode)
            {
                string jsonString = await response.Content.ReadAsStringAsync();
                var jsonDoc = JsonDocument.Parse(jsonString);
                foreach (var element in jsonDoc.RootElement.EnumerateArray())
                {
                    Country country = new Country
                    {
                        Name = element.GetProperty("name").GetProperty("common").GetString(),
                        Capital = element.TryGetProperty("capital", out var capitalProp) && capitalProp.ValueKind == JsonValueKind.Array && capitalProp.GetArrayLength() > 0 ? capitalProp[0].GetString() : "N/A",
                        Population = element.GetProperty("population").GetInt64(),
                        Area = element.GetProperty("area").GetDouble(),
                        Currency = element.GetProperty("currencies").EnumerateObject().First().Value.GetProperty("name").GetString()
                    };
                    countries.Add(country);
                }
            }
            return countries;
        }
    }
}


